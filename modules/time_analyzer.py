import sqlite3
import time
from modules.cluster_activities import cluster_activities
import pandas as pd
import time
def categorize_time_usage():
    try:
        df = cluster_activities()
        if df.empty:
            return {"No Data": 0}  # Return default if no data
            
        categories = {
            "Social Media": ["chrome.exe", "msedge.exe", "firefox.exe","opera.exe"],
            "Productivity": ["code.exe", "pycharm.exe", "winword.exe"],
            "Entertainment": ["spotify.exe", "vlc.exe", "youtube.exe"],
            "Other": []
        }
        
        results = {}
        for app, group in df.groupby("app"):
            duration = len(group) * 5 / 60  # Convert to minutes
            category = next((cat for cat, apps in categories.items() 
                          if app.lower() in [a.lower() for a in apps]), "Other")
            results[category] = results.get(category, 0) + duration
            
        return results if results else {"No Activities": 0}
        
    except Exception as e:
        print(f"Error in categorize_time_usage: {e}")
        return {"Error": 0}