# ⏱️ Simple Python Time Tracker

A lightweight, modern desktop time-tracking application built with Python and CustomTkinter. It features a sleek dark-mode interface, a floating always-on-top design, and automatic file logging to keep track of your daily tasks.

<img width="376" height="412" alt="Preview" src="https://github.com/user-attachments/assets/1920150e-e5dd-4188-b0a5-2454171825a7" />

---

## ✨ Features

* **Always-on-Top Window:** Floating UI design that stays visible over your workspace windows.
* **Live System Clock:** Real-time system time and date display updated every second.
* **Smart Timer Controls:** Upward-running timer with **Start**, **Pause**, and **End** controls. Features intelligent button state locking to prevent invalid user inputs during active tracking.
* **Task Description Input:** Easily label your tracked sessions with custom task names.
* **File-Based Logging:** Select any `.txt` file to automatically append formatted task logs containing start times, end times, total duration, and task names.
* **Built-In Log History Viewer:** Open a secondary modal window directly within the app to review past task records.

---

## 🚀 How to Run

### Option A: Run the Pre-Compiled `.exe` (Easiest)
1. Download the `time_tracker.exe` file.
2. Double-click the `.exe` to launch the application instantly—no Python installation required!

### Option B: Run from Source Code (Python)
If you want to run or modify the Python script directly, follow these steps:

1. **Clone or download** this repository to your computer.
2. **Install Python** (version 3.8 or newer) if you haven't already.
3. **Install dependencies** by opening your terminal or command prompt and running:
   ```bash
   pip install customtkinter
