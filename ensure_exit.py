import os
import sys
import psutil
import threading

# Define the process name based on the OS
if os.name == "nt":  # Windows
    process_name = "tauri-python.exe"
else:  # Unix-like systems
    process_name = "tauri-python"


def get_process_id(process_name):
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        try:
            if process_name == proc.info["name"]:
                return proc.info["pid"]
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


parent_pid = os.getpid()


def check():
    if get_process_id(process_name) == False:
        print("exiting")
        psutil.Process(parent_pid).kill()


if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    set_interval(check, 10)
