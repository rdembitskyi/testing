from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, request, jsonify
from analyzer.file_scanner import analyze_directory, summarize_global_token_counts
from api.tasks import submit_analysis_task
from storage.in_memory_db import get_task_result
import os
import uuid
import tempfile

# executor to simulate async behavior in a synchronous context for testing purposes
executor = ThreadPoolExecutor(max_workers=4)

bp = Blueprint("sync", __name__)


@bp.route("/analyze_sync", methods=["POST"])
def analyze_sync():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.lower().endswith(".txt"):
        # Simple validation for file type
        # only for testing purposes
        return jsonify({"error": "Only .txt firmware archives are supported"}), 400

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, file.filename)
            file.save(file_path)

            # Run analysis
            analysis_results = analyze_directory(directory_path=temp_dir)
            token_summary = summarize_global_token_counts(results=analysis_results)

            return jsonify(token_summary)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/analyze_async", methods=["POST"])
def analyze_async():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.lower().endswith(".txt"):
        return jsonify({"error": "Only .txt firmware files are supported"}), 400

    try:
        task_id = str(uuid.uuid4())
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)

        executor.submit(submit_analysis_task, temp_dir=temp_dir, task_id=task_id)

        return jsonify({"task_id": task_id}), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/results/<task_id>", methods=["GET"])
def get_results(task_id: str):
    result = get_task_result(task_id)
    if result is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"status": "completed", "result": result})
