import threading
from typing import Callable


def run_background_task(func: Callable, *args, **kwargs):
    """
    Lightweight background worker using threading.
    (No external queue dependency yet)
    """

    thread = threading.Thread(
        target=func,
        args=args,
        kwargs=kwargs,
        daemon=True,
    )

    thread.start()
    return thread