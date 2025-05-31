import psutil
import time
import win32gui
import win32process  
from modules.data_handler import setup_database
from modules.data_handler import save_activity

def get_active_window():
    window = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(window)
    _, process_id = win32process.GetWindowThreadProcessId(window)
    process_name = psutil.Process(process_id).name()
    return {"timestamp": time.time(), "app": process_name, "title": title}

def track_activity(interval=5):
    setup_database()  # Initialize DB
    while True:
        activity = get_active_window()
        print(f"Currently using: {activity['app']} - {activity['title']}")
        save_activity(activity)
        time.sleep(interval)  # Check every 5 seconds

        