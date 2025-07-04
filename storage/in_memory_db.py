TASK_RESULTS = {}


def get_task_result(task_id: str) -> dict | None:
    return TASK_RESULTS.get(task_id)