import os
import re
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from analyzer.domain import TokenResult
from utils.csv import save_token_results_to_csv

TOKEN_PATTERN = re.compile(r"<Tkn\d{3}[A-Z]{5}Tkn>")
MAX_WORKERS = mp.cpu_count()


def find_tokens_in_file(file_path: str, base_path: str) -> list[TokenResult]:
    print(f"Scanning {file_path}...")
    token_counts: dict[str, int] = {}

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            # Stream through the file line by line to avoid memory issues with large files
            for line in f:
                if "<Tkn" in line:  # fast pre-filter
                    matches = TOKEN_PATTERN.findall(line)
                    for token in matches:
                        token_counts[token] = token_counts.get(token, 0) + 1
    except Exception:  # Broad exception for testing purposes
        return []

    if not token_counts:
        return []

    relative_path = os.path.relpath(file_path, base_path)
    return [{"Path": relative_path, "Token": token, "Occurrences": count} for token, count in token_counts.items()]


def gather_all_file_paths(directory_path: str) -> list[str]:
    return [os.path.join(root, file) for root, _, files in os.walk(directory_path) for file in files]


def analyze_directory(directory_path: str) -> list[TokenResult]:
    file_paths = gather_all_file_paths(directory_path)
    print(f"Scanning {file_paths}...")
    if not file_paths:
        return []

    max_workers = min(MAX_WORKERS, len(file_paths))
    results: list[TokenResult] = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        bound_func = partial(find_tokens_in_file, base_path=directory_path)
        result_lists = executor.map(bound_func, file_paths)

    for r in result_lists:
        results.extend(r)

    results.sort(key=lambda x: (x["Path"], x["Occurrences"], x["Token"]))
    return results


def summarize_global_token_counts(results: list[TokenResult]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for result in results:
        token = result["Token"]
        count = result["Occurrences"]
        summary[token] = summary.get(token, 0) + count
    return summary


# Example usage
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_files_dir = os.path.join(current_dir, "test_files")
    start_time = time.time()

    results = analyze_directory(test_files_dir)
    summary = summarize_global_token_counts(results)

    elapsed = time.time() - start_time
    print(f"✅ Completed in {elapsed:.2f} seconds")
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    save_token_results_to_csv(results, os.path.join(current_dir, f"results/analysis_results_{timestamp}.csv"))
