import datetime
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class TimeTrackerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Simple Time Tracker with History")
        self.geometry("300x300")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        self.timer_running = False
        self.elapsed_seconds = 0
        self.timer_job = None
        self.start_timestamp = None
        self.log_file_path = ""

        self._create_widgets()
        self._update_current_time()
        
        # Set initial button states
        self._update_button_states()

    def _create_widgets(self):
        # 1. Current Time Display
        self.time_label = ctk.CTkLabel(
            self,
            text="Current time: --:--:-- -- -- ---",
            font=ctk.CTkFont(family="Verdana", size=13, weight="bold"),
        )
        self.time_label.pack(anchor="w", padx=20, pady=(15, 5))

        # 2. Task Name Input
        self.task_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.task_frame.pack(fill="x", padx=20, pady=5)

        self.task_title_label = ctk.CTkLabel(
            self.task_frame,
            text="Task name:",
            font=ctk.CTkFont(family="Verdana", size=13),
        )
        self.task_title_label.pack(side="left", padx=(0, 10))

        self.task_entry = ctk.CTkEntry(
            self.task_frame,
            placeholder_text="Enter task description...",
            width=260,
            font=ctk.CTkFont(family="Verdana", size=12),
        )
        self.task_entry.pack(side="left")

        # 3. Time Spent Display
        self.spent_label = ctk.CTkLabel(
            self,
            text="Time spent: 00:00:00",
            font=ctk.CTkFont(family="Verdana", size=16, weight="bold"),
            text_color="#2ea043",
        )
        self.spent_label.pack(anchor="w", padx=20, pady=15)

        # 4. Action Buttons (Start, Pause, End)
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=20, pady=5)

        self.start_btn = ctk.CTkButton(
            self.btn_frame,
            text="Start",
            width=85,
            fg_color="#2ea043",
            hover_color="#238636",
            command=self.start_timer,
        )
        self.start_btn.pack(side="left", padx=(0, 8))

        self.pause_btn = ctk.CTkButton(
            self.btn_frame,
            text="Pause",
            width=85,
            fg_color="#d29922",
            hover_color="#bb8009",
            command=self.pause_timer,
        )
        self.pause_btn.pack(side="left", padx=8)

        self.end_btn = ctk.CTkButton(
            self.btn_frame,
            text="End",
            width=85,
            fg_color="#da3633",
            hover_color="#b62324",
            command=self.end_timer,
        )
        self.end_btn.pack(side="left", padx=(8, 0))

        # 5. File Selection Controls
        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.pack(fill="x", padx=20, pady=(15, 5))

        self.file_btn = ctk.CTkButton(
            self.file_frame,
            text="Select file",
            width=110,
            command=self.select_file,
        )
        self.file_btn.pack(side="left")

        self.file_path_label = ctk.CTkLabel(
            self.file_frame,
            text="No file selected",
            font=ctk.CTkFont(family="Verdana", size=11),
            text_color="#8b949e",
        )
        self.file_path_label.pack(side="left", padx=10)

        # 6. View History Button
        self.history_btn = ctk.CTkButton(
            self,
            text="View Log History",
            width=380,
            fg_color="#30363d",
            hover_color="#484f58",
            command=self.open_history_window,
        )
        self.history_btn.pack(padx=20, pady=(10, 15))

    def _update_button_states(self):
        """Manages button enable/disable states based on tracking status."""
        if self.timer_running:
            # Running: Disable Start, Enable Pause and End
            self.start_btn.configure(state="disabled")
            self.pause_btn.configure(state="normal")
            self.end_btn.configure(state="normal")
        else:
            # Paused or Stopped: Enable End if there is recorded time or activity
            self.start_btn.configure(state="normal")
            self.pause_btn.configure(state="disabled")
            # Keep End enabled if time has been tracked, otherwise disable if completely fresh
            if self.elapsed_seconds > 0:
                self.end_btn.configure(state="normal")
            else:
                self.end_btn.configure(state="disabled")

    # --- Live System Clock ---
    def _update_current_time(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M:%S %p %d-%b-%y")
        self.time_label.configure(text=f"Current time: {time_str}")
        self.after(1000, self._update_current_time)

    # --- Timer Operations ---
    def start_timer(self):
        if not self.timer_running:
            if self.elapsed_seconds == 0:
                self.start_timestamp = datetime.datetime.now()
            self.timer_running = True
            self._update_button_states()
            self._run_timer_tick()

    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            if self.timer_job:
                self.after_cancel(self.timer_job)
            self._update_button_states()

    def end_timer(self):
        if self.elapsed_seconds == 0 and not self.timer_running:
            return

        self.pause_timer()
        end_timestamp = datetime.datetime.now()

        if not self.start_timestamp:
            self.start_timestamp = end_timestamp - datetime.timedelta(
                seconds=self.elapsed_seconds
            )

        start_str = self.start_timestamp.strftime("%I:%M:%S %p %d-%b-%y")
        end_str = end_timestamp.strftime("%I:%M:%S %p %d-%b-%y")

        hours, remainder = divmod(self.elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        spent_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        task_name = self.task_entry.get().strip() or "Untitled Task"

        log_entry = (
            f"Task started: {start_str}\n"
            f"Task ended: {end_str}\n"
            f"Time spent:{spent_str}\n"
            f"Task name: {task_name}\n\n"
        )

        if not self.log_file_path:
            self.select_file()

        if self.log_file_path:
            try:
                with open(self.log_file_path, "a", encoding="utf-8") as f:
                    f.write(log_entry)
                messagebox.showinfo("Success", "Task log saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to write: {e}")

        self.reset_tracker()

    def _run_timer_tick(self):
        if self.timer_running:
            self.elapsed_seconds += 1
            hours, remainder = divmod(self.elapsed_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.spent_label.configure(
                text=f"Time spent: {hours:02d}:{minutes:02d}:{seconds:02d}"
            )
            self.timer_job = self.after(1000, self._run_timer_tick)

    def reset_tracker(self):
        self.elapsed_seconds = 0
        self.start_timestamp = None
        self.spent_label.configure(text="Time spent: 00:00:00")
        self.task_entry.delete(0, "end")
        self._update_button_states()

    def select_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Select Log Text File",
        )
        if file_path:
            self.log_file_path = file_path
            display_name = os.path.basename(file_path)
            self.file_path_label.configure(
                text=display_name, text_color="#ffffff"
            )

    def open_history_window(self):
        if not self.log_file_path or not os.path.exists(self.log_file_path):
            messagebox.showwarning(
                "Warning",
                "Please select a valid log file first using 'Select file'.",
            )
            return

        history_win = ctk.CTkToplevel(self)
        history_win.title("Task Log History")
        history_win.geometry("500x450")
        history_win.attributes("-topmost", True)

        title_lbl = ctk.CTkLabel(
            history_win,
            text=f"History from: {os.path.basename(self.log_file_path)}",
            font=ctk.CTkFont(family="Verdana", size=13, weight="bold"),
        )
        title_lbl.pack(anchor="w", padx=15, pady=(15, 5))

        log_textbox = ctk.CTkTextbox(
            history_win,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="none",
        )
        log_textbox.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        try:
            with open(self.log_file_path, "r", encoding="utf-8") as f:
                content = f.read()
                log_textbox.insert(
                    "1.0",
                    content
                    if content.strip()
                    else "Log file is currently empty.",
                )
        except Exception as e:
            log_textbox.insert("1.0", f"Error reading log file: {e}")

        log_textbox.configure(state="disabled")


if __name__ == "__main__":
    app = TimeTrackerApp()
    app.imagewin = None
    app.mainloop()