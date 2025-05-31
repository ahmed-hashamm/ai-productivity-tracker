# from modules.activity_monitor import track_activity
# from modules.clustering_engine import cluster_activities
# import matplotlib.pyplot as plt
# track_activity()  # Press Ctrl+C to stop

# # Test clustering
# df = cluster_activities()
# print("\nClustering Results:")
# print(df[["app", "hour", "cluster"]].head())

# # Optional: Visualize clusters
# plt.scatter(df["hour"], df["cluster"])
# plt.xlabel("Hour of Day")
# plt.ylabel("Cluster")
# plt.title("Activity Clusters by Hour")
# plt.show()
# import tkinter as tk
# from tkinter import ttk
# from modules.activity_monitor import track_activity
# from modules.activity_monitor import get_active_window
# from modules.time_analyzer import categorize_time_usage
# from modules.feedback_system import generate_feedback
# import time
# from threading import Thread

# class ProductivityTrackerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("AI Productivity Tracker")
#         self.root.geometry("800x600")
#         self.setup_ui()
#         self.running = True
#         self.start_activity_monitor()
    
#     def setup_ui(self):
#         # Configure style
#         style = ttk.Style()
#         style.configure("TFrame", background="#f0f0f0")
#         style.configure("TLabel", background="#f0f0f0", font=('Helvetica', 10))
#         style.configure("Header.TLabel", font=('Helvetica', 12, 'bold'))
#         style.configure("TButton", font=('Helvetica', 10))
        
#         # Main container
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.pack(fill=tk.BOTH, expand=True)
        
#         # Activity Monitor Section
#         activity_frame = ttk.LabelFrame(main_frame, text="Current Activity", padding="10")
#         activity_frame.pack(fill=tk.X, pady=5)
        
#         self.current_app_label = ttk.Label(activity_frame, text="No active application detected")
#         self.current_app_label.pack()
        
#         # Time Analysis Section
#         analysis_frame = ttk.LabelFrame(main_frame, text="Time Analysis", padding="10")
#         analysis_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
#         self.time_usage_label = ttk.Label(analysis_frame, text="Collecting data...")
#         self.time_usage_label.pack()
        
#         # Create a treeview for detailed activity breakdown
#         self.tree = ttk.Treeview(analysis_frame, columns=('Category', 'Time'), show='headings')
#         self.tree.heading('Category', text='Category')
#         self.tree.heading('Time', text='Time (minutes)')
#         self.tree.pack(fill=tk.BOTH, expand=True)
        
#         # Feedback Section
#         feedback_frame = ttk.LabelFrame(main_frame, text="Productivity Feedback", padding="10")
#         feedback_frame.pack(fill=tk.BOTH, pady=5)
        
#         self.feedback_text = tk.Text(feedback_frame, height=5, wrap=tk.WORD, font=('Helvetica', 10))
#         self.feedback_text.pack(fill=tk.BOTH)
        
#         # Control buttons
#         button_frame = ttk.Frame(main_frame)
#         button_frame.pack(fill=tk.X, pady=5)
        
#         ttk.Button(button_frame, text="Refresh", command=self.update_data).pack(side=tk.LEFT, padx=5)
#         ttk.Button(button_frame, text="Exit", command=self.on_close).pack(side=tk.RIGHT, padx=5)
        
#         # Initial update
#         self.update_data()
    
#     def start_activity_monitor(self):
#         def monitor_loop():
#             while self.running:
#                 try:
#                     activity = get_active_window()
#                     self.root.after(0, self.update_current_activity, activity)
#                     time.sleep(5)  # Update every 5 seconds
#                 except Exception as e:
#                     print(f"Monitor error: {e}")
#                     time.sleep(10)
        
#         self.monitor_thread = Thread(target=monitor_loop, daemon=True)
#         self.monitor_thread.start()

#     def update_current_activity(self, activity):
#         app_name = activity['app'].replace('.exe', '').title()
#         self.current_app_label.config(
#             text=f"Current App: {app_name}\nWindow: {activity['title'][:50]}...",
#             font=('Helvetica', 10, 'bold')
#         )
    
#     def update_data(self):
#         try:
#             # Force UI update before processing
#             self.time_usage_label.config(text="Refreshing data...")
#             self.root.update_idletasks()
            
#             time_usage = categorize_time_usage()
#             feedback = generate_feedback(time_usage)
            
#             # Update time usage display
#             self.tree.delete(*self.tree.get_children())
#             for category, minutes in time_usage.items():
#                 self.tree.insert('', tk.END, values=(category, f"{minutes:.1f}"))
            
#             # Update feedback
#             self.feedback_text.config(state=tk.NORMAL)
#             self.feedback_text.delete(1.0, tk.END)
#             self.feedback_text.insert(tk.END, "\n".join(feedback))
#             self.feedback_text.config(state=tk.DISABLED)
            
#         except Exception as e:
#             error_msg = f"Refresh error: {str(e)}"
#             print(error_msg)
#             self.feedback_text.config(state=tk.NORMAL)
#             self.feedback_text.delete(1.0, tk.END)
#             self.feedback_text.insert(tk.END, error_msg)
#             self.feedback_text.config(state=tk.DISABLED)
           
    
#     def on_close(self):
#         self.running = False
#         self.root.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ProductivityTrackerApp(root)
#     root.protocol("WM_DELETE_WINDOW", app.on_close)
#     root.mainloop()

import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
import sqlite3
import pandas as pd
from modules.activity_monitor import get_active_window
from modules.time_analyzer import categorize_time_usage
from modules.feedback_system import generate_feedback

class ProductivityTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Productivity Tracker")
        self.root.geometry("800x600")
        self.setup_ui()
        self.running = True
        self.last_update = 0
        self.start_activity_monitor()
        self.update_data()  # Initial data load
    
    def setup_ui(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=('Helvetica', 10))
        style.configure("Header.TLabel", font=('Helvetica', 12, 'bold'))
        style.configure("TButton", font=('Helvetica', 10))
        style.configure("Treeview", font=('Helvetica', 9))
        style.configure("Treeview.Heading", font=('Helvetica', 9, 'bold'))
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Current Activity Section
        current_frame = ttk.LabelFrame(main_frame, text="Current Activity", padding="10")
        current_frame.pack(fill=tk.X, pady=5)
        
        self.current_app_var = tk.StringVar(value="No active application detected")
        self.current_app_label = ttk.Label(
            current_frame, 
            textvariable=self.current_app_var,
            font=('Helvetica', 10, 'bold'),
            foreground='blue'
        )
        self.current_app_label.pack()
        
        # Time Analysis Section
        analysis_frame = ttk.LabelFrame(main_frame, text="Time Analysis (Last 24 Hours)", padding="10")
        analysis_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview for time breakdown
        self.tree = ttk.Treeview(
            analysis_frame, 
            columns=('Category', 'Time'), 
            show='headings',
            height=5
        )
        self.tree.heading('Category', text='Category')
        self.tree.heading('Time', text='Time (minutes)')
        self.tree.column('Category', width=200, anchor='w')
        self.tree.column('Time', width=100, anchor='e')
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Feedback Section
        feedback_frame = ttk.LabelFrame(main_frame, text="Productivity Feedback", padding="10")
        feedback_frame.pack(fill=tk.BOTH, pady=5)
        
        self.feedback_text = tk.Text(
            feedback_frame, 
            height=5, 
            wrap=tk.WORD, 
            font=('Helvetica', 10),
            padx=5,
            pady=5
        )
        self.feedback_text.pack(fill=tk.BOTH)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(5,0))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            button_frame, 
            text="Refresh Data", 
            command=self.force_refresh
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="View Raw Data", 
            command=self.show_raw_data
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Exit", 
            command=self.on_close
        ).pack(side=tk.RIGHT, padx=5)
    
    def start_activity_monitor(self):
        """Start the background activity monitoring thread"""
        self.monitor_thread = Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.status_var.set("Monitoring started...")
    
    def _monitor_loop(self):
        """Background thread for monitoring active window"""
        while self.running:
            try:
                activity = get_active_window()
                self._save_activity(activity)
                self.root.after(0, self._update_current_activity, activity)
                
                # Auto-refresh every 5 minutes
                if time.time() - self.last_update > 300:
                    self.root.after(0, self.update_data)
                
                time.sleep(5)
            except Exception as e:
                print(f"Monitoring error: {e}")
                self.status_var.set(f"Error: {str(e)}")
                time.sleep(10)
    
    def _save_activity(self, activity):
        """Save activity to database"""
        try:
            conn = sqlite3.connect("data/productivity.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO activities (timestamp, app, title) VALUES (?, ?, ?)",
                (activity["timestamp"], activity["app"], activity["title"])
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database error: {e}")
    
    def _update_current_activity(self, activity):
        """Update the current activity display"""
        app_name = activity['app'].replace('.exe', '').title()
        window_title = activity['title'][:50] + ('...' if len(activity['title']) > 50 else '')
        self.current_app_var.set(f"Current App: {app_name}\nWindow: {window_title}")
    
    def force_refresh(self):
        """Force a complete data refresh"""
        self.status_var.set("Refreshing data...")
        self.update_data()
    
    def update_data(self):
        """Refresh all the data displays"""
        try:
            # Show loading state
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.tree.insert('', tk.END, values=("Loading data...", ""))
            self.feedback_text.config(state=tk.NORMAL)
            self.feedback_text.delete(1.0, tk.END)
            self.feedback_text.insert(tk.END, "Refreshing data...")
            self.feedback_text.config(state=tk.DISABLED)
            self.root.update_idletasks()
            
            # Force database connection close and reopen
            try:
                conn = sqlite3.connect("data/productivity.db")
                conn.close()
            except:
                pass
            
            # Get fresh data with timestamp
            start_time = time.time()
            time_usage = categorize_time_usage()
            feedback = generate_feedback(time_usage)
            processing_time = time.time() - start_time
            
            # Update time analysis treeview
            self.tree.delete(*self.tree.get_children())
            if not time_usage:
                self.tree.insert('', tk.END, values=("No activity data found", ""))
            else:
                for category, minutes in sorted(time_usage.items(), key=lambda x: x[1], reverse=True):
                    self.tree.insert('', tk.END, values=(category, f"{minutes:.1f}"))
            
            # Update feedback
            self.update_feedback_display(feedback)
            
            # Update status
            self.last_update = time.time()
            self.status_var.set(f"Last updated: {time.strftime('%H:%M:%S')} | Processed in {processing_time:.2f}s")
            
        except Exception as e:
            error_msg = f"Error refreshing data: {str(e)}"
            print(error_msg)
            self.status_var.set(error_msg)
            self.update_feedback_display([error_msg])
    
    def update_feedback_display(self, messages):
        """Update the feedback text widget"""
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        
        if messages:
            for msg in messages:
                self.feedback_text.insert(tk.END, msg + "\n")
                
                # Color coding
                if "⚠️" in msg:
                    self.feedback_text.tag_add('warning', tk.END + "-%dc" % (len(msg)+1), tk.END)
                    self.feedback_text.tag_config('warning', foreground='orange')
                elif "✅" in msg or "🚀" in msg:
                    self.feedback_text.tag_add('positive', tk.END + "-%dc" % (len(msg)+1), tk.END)
                    self.feedback_text.tag_config('positive', foreground='green')
        
        self.feedback_text.config(state=tk.DISABLED)
    
    def show_raw_data(self):
        """Display raw data in a new window"""
        try:
            conn = sqlite3.connect("data/productivity.db")
            df = pd.read_sql("SELECT * FROM activities ORDER BY timestamp DESC LIMIT 100", conn)
            conn.close()
            
            # Create new window
            data_window = tk.Toplevel(self.root)
            data_window.title("Raw Activity Data")
            data_window.geometry("1000x400")
            
            # Create text widget
            text_widget = tk.Text(data_window, wrap=tk.NONE)
            text_widget.pack(fill=tk.BOTH, expand=True)
            
            # Add data
            text_widget.insert(tk.END, df.to_string())
            text_widget.config(state=tk.DISABLED)
            
            # Add scrollbars
            y_scroll = ttk.Scrollbar(data_window, orient=tk.VERTICAL, command=text_widget.yview)
            x_scroll = ttk.Scrollbar(data_window, orient=tk.HORIZONTAL, command=text_widget.xview)
            text_widget.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
            y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            
        except Exception as e:
            self.status_var.set(f"Error showing data: {str(e)}")
    
    def on_close(self):
        """Clean up when closing the window"""
        self.running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=1)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductivityTrackerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()