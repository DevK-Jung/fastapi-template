from uuid import uuid4


def generate_run_id() -> str:
    return f"run-{uuid4()}"
