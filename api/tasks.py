from analyzer.file_scanner import analyze_directory, summarize_global_token_counts
import shutil
from storage.in_memory_db import TASK_RESULTS


def submit_analysis_task(temp_dir: str, task_id: str) -> None:
    try:
        results = analyze_directory(directory_path=temp_dir)
        summary = summarize_global_token_counts(results=results)
        TASK_RESULTS[task_id] = summary
    except Exception as e:
        # Store error in task results
        # use print instead of logging for simplicity
        print(f"Error processing task {task_id}: {e}")
        TASK_RESULTS[task_id] = {"error": str(e)}
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

