import csv
from analyzer.domain import TokenResult


def save_token_results_to_csv(results: list[TokenResult], csv_output_path: str) -> None:
    with open(csv_output_path, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Path", "Token", "Occurrences"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)
