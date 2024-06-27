import tkinter as tk
from tkinter import ttk, messagebox
import requests
import time
import threading
from playsound import playsound
from datetime import datetime
import os

class InternetCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("InternetCheck")
        self.root.configure(bg="black")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_dir = "Logs"
        self.log_files = {
            "success": os.path.join(self.log_dir, f"{self.date_time_str}_internet_success.log"),
            "failure": os.path.join(self.log_dir, f"{self.date_time_str}_internet_failure.log")
        }

        self.init_logs()

        self.status_label = tk.Label(root, text="", font=("Helvetica", 24, "bold"), bg="black", fg="white")
        self.status_label.pack(pady=10)

        self.create_table()

        self.check_connection()

        self.alarm_shown = False

    def init_logs(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        with open(self.log_files["success"], 'w') as f:
            f.write(f"Program started at: {self.start_time}\n")
        with open(self.log_files["failure"], 'w') as f:
            f.write(f"Program started at: {self.start_time}\n")

    def create_table(self):
        self.table_frame = tk.Frame(self.root, bg="black")
        self.table_frame.pack(pady=20, fill="both", expand=True)

        # Creating styles for Treeview
        self.style = ttk.Style()
        self.style.configure("Treeview", background="black", foreground="white", fieldbackground="black")
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="black", foreground="white")
        self.style.map('Treeview.Heading', background=[('active', 'black')], foreground=[('active', 'white')])
        self.style.map('Treeview', background=[('selected', 'yellow')], foreground=[('selected', 'black')])

        # Creating Treeview widget
        self.treeview = ttk.Treeview(self.table_frame, columns=("Date Time", "Status"), show="headings", style="Treeview")
        self.treeview.heading("Date Time", text="Date Time")
        self.treeview.heading("Status", text="Status")

        # Tag configurations
        self.treeview.tag_configure("Success", background="green", foreground="black")
        self.treeview.tag_configure("Failure", background="red", foreground="black")

        self.scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scroll_y.set)

        self.treeview.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

    def update_table(self, date_time, status):
        if status == "Success":
            self.treeview.insert("", "end", values=(date_time, status), tags=("Success",))
        elif status == "Failure":
            self.treeview.insert("", "end", values=(date_time, status), tags=("Failure",))

        # Scroll to the bottom of the Treeview
        self.treeview.yview_moveto(1.0)

    def check_connection(self):
        def ping():
            while True:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    response = requests.get('https://www.google.com', timeout=5)
                    if response.status_code == 200:
                        self.update_status("Internet connection is successful", "green")
                        if self.last_status != "Success":
                            self.update_table(current_time, "Success")
                            self.log_event("success", current_time, "Internet connection is successful")
                            self.alarm_shown = False  # Reconnected, can show alarm again
                    else:
                        self.connection_lost(current_time)
                except requests.ConnectionError:
                    self.connection_lost(current_time)
                    self.update_status("INTERNET CONNECTION LOST!", "red")
                    if self.last_status != "Failure":
                        self.update_table(current_time, "Failure")
                        self.log_event("failure", current_time, "INTERNET CONNECTION LOST")
                        if not self.alarm_shown:
                            self.play_alarm()
                            self.alarm_shown = True
                time.sleep(5)

        self.ping_thread = threading.Thread(target=ping, daemon=True)
        self.ping_thread.start()

    def update_status(self, message, color):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_label.config(text=f"{message}\n{current_time}", fg=color)
        self.last_status = message.split()[0]

    def connection_lost(self, current_time):
        self.update_status("INTERNET CONNECTION LOST!", "red")
        self.log_event("failure", current_time, "INTERNET CONNECTION LOST")

    def play_alarm(self):
        if not hasattr(self, 'alarm_thread') or not self.alarm_thread.is_alive():
            def alarm():
                while not self.stop_alarm:
                    playsound("alarm.wav")

            self.stop_alarm = False
            self.alarm_thread = threading.Thread(target=alarm, daemon=True)
            self.alarm_thread.start()
            
            # Schedule showing messagebox after 100 ms
            self.root.after(100, lambda: messagebox.showwarning("Alarm", "INTERNET CONNECTION LOST!"))
            
            self.stop_alarm = True

    def log_event(self, log_type, current_time, message):
        with open(self.log_files[log_type], 'a') as f:
            f.write(f"{current_time}: {message}\n")

    def on_closing(self):
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for log_file in self.log_files.values():
            with open(log_file, 'a') as f:
                f.write(f"Program ended at: {end_time}\n")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InternetCheckApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
