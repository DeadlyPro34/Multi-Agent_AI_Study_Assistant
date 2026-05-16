import threading
import uuid
from datetime import datetime

# 🔒 Thread-safe global tracker for background tasks
# Structure: task_id -> { status, type, topic, result, started_at, completed_at, notified }
_TASKS_LOCK = threading.Lock()
BACKGROUND_TASKS = {}

def start_background_task(task_type: str, topic: str, target_func, *args, **kwargs) -> str:
    """
    Spawns a new daemon thread to execute the specified function in the background without blocking Streamlit.
    Returns the unique task_id.
    """
    task_id = str(uuid.uuid4())
    
    with _TASKS_LOCK:
        BACKGROUND_TASKS[task_id] = {
            "status": "RUNNING",
            "type": task_type,
            "topic": topic,
            "result": None,
            "started_at": datetime.now(),
            "completed_at": None,
            "notified": False
        }
        
    def task_wrapper():
        import traceback
        log_file = "async_debug.log"
        
        def log(msg):
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().isoformat()}] [Task {task_id}] {msg}\n")

        log(f"STARTING background task of type '{task_type}' for topic '{topic}'")
        
        try:
            # Execute the blocking work
            log("Invoking target function...")
            result = target_func(*args, **kwargs)
            log("Target function execution COMPLETED successfully.")
            
            with _TASKS_LOCK:
                BACKGROUND_TASKS[task_id]["status"] = "COMPLETED"
                BACKGROUND_TASKS[task_id]["result"] = result
                BACKGROUND_TASKS[task_id]["completed_at"] = datetime.now()
                
            log("State committed to BACKGROUND_TASKS registry.")
        except Exception as e:
            tb = traceback.format_exc()
            log(f"ERROR: Target function raised exception: {str(e)}\n{tb}")
            
            with _TASKS_LOCK:
                BACKGROUND_TASKS[task_id]["status"] = "FAILED"
                BACKGROUND_TASKS[task_id]["result"] = str(e)
                BACKGROUND_TASKS[task_id]["completed_at"] = datetime.now()
            
            log("Failure state committed to BACKGROUND_TASKS.")

    # Create and start the daemon thread
    worker = threading.Thread(target=task_wrapper, daemon=True)
    worker.name = f"SynapseAI_Bg_{task_id}"
    worker.start()
    
    return task_id

def check_task_status(task_id: str):
    """Retrieves the current state of a background task."""
    with _TASKS_LOCK:
        return BACKGROUND_TASKS.get(task_id)

def drain_completed_tasks():
    """
    Extracts newly completed or failed tasks and compiles them into notification payloads.
    Marks extracted tasks as 'notified' to prevent double processing.
    """
    notifications_to_add = []
    
    with _TASKS_LOCK:
        for tid, data in BACKGROUND_TASKS.items():
            if data["status"] in ["COMPLETED", "FAILED"] and not data["notified"]:
                data["notified"] = True
                
                icon = "✅" if data["status"] == "COMPLETED" else "⚠️"
                completion_time = data["completed_at"].strftime("%I:%M %p") if data["completed_at"] else "Just now"
                
                summary_title = data["topic"] if data["topic"].strip() else "Material"
                status_msg = "finished generating!" if data["status"] == "COMPLETED" else "encountered an error."
                
                notifications_to_add.append({
                    "id": tid,
                    "type": data["type"],
                    "topic": summary_title,
                    "status": data["status"],
                    "message": f"{icon} {data['type'].title()} for '{summary_title}' {status_msg}",
                    "result": data["result"],
                    "timestamp": completion_time
                })
                
    return notifications_to_add
