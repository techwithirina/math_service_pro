# worker.py
import threading
import queue


# A global thread-safe queue to hold tasks
# A FIFO queue to which we’ll submit background work.
task_queue = queue.Queue()


# Waits for tasks forever, pulls them out, and runs the function.
def worker_loop():
    print("[Worker] Background worker started.")
    while True:
        task = task_queue.get()  # wait for a task
        if task is None:
            print("[Worker] Shutting down.")
            break  # gracefully shut down
        try:
            print(f"[Worker] Executing task: {task}")
            task["func"](*task["args"])  # call the function with arguments
        except Exception as e:
            print(f"[Worker] Error: {e}")
        finally:
            task_queue.task_done()  # mark task as done


# Spawns the background thread when the app starts.
def start_worker():
    worker_thread = threading.Thread(target=worker_loop, daemon=True)
    worker_thread.start()
