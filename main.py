import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import sys

# Adobe Apps List (exe names)
adobe_apps = {
    "Photoshop": "Photoshop.exe",
    "Illustrator": "Illustrator.exe",
    "InDesign": "InDesign.exe"
}



# Check if firewall rule exists
def rule_exists(name, direction):
    result = subprocess.run([
        "netsh", "advfirewall", "firewall", "show", "rule",
        f"name=Block {name} {direction}"
    ], capture_output=True, text=True, shell=True)
    return "No rules match" not in result.stdout

# Find Adobe apps in both 64-bit and 32-bit locations
def find_adobe_apps():
    program_dirs = [
        r"C:\Program Files\Adobe",
        r"C:\Program Files (x86)\Adobe"
    ]
    found_paths = {}

    for base_path in program_dirs:
        if not os.path.exists(base_path):
            continue
        for root, dirs, files in os.walk(base_path):
            for app_name, exe in adobe_apps.items():
                if exe in files and app_name not in found_paths:
                    found_paths[app_name] = os.path.join(root, exe)
    return found_paths

# Add firewall rules
def add_firewall_rule(name, exe_path):
    for direction in ["in", "out"]:
        rule_name = f"Block {name} {direction}"
        if not rule_exists(name, direction):
            subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}",
                f"dir={direction}",
                "action=block",
                f"program={exe_path}",
                "enable=yes",
                "profile=any"
            ], shell=True)

# Remove firewall rules
def remove_firewall_rule(name):
    for direction in ["in", "out"]:
        subprocess.run([
            "netsh", "advfirewall", "firewall", "delete", "rule",
            f"name=Block {name} {direction}"
        ], shell=True)

# Update app status labels
def update_status_labels():
    for app_name, label in status_labels.items():
        if rule_exists(app_name, "in") and rule_exists(app_name, "out"):
            label.config(text="Blocked", foreground="red")
        else:
            label.config(text="Allowed", foreground="green")

# Block internet for selected apps
def block_selected_apps():
    found_apps = find_adobe_apps()
    blocked = []
    for app_name, var in app_vars.items():
        if var.get():
            exe_path = found_apps.get(app_name)
            if exe_path:
                add_firewall_rule(app_name, exe_path)
                blocked.append(app_name)
            else:
                messagebox.showwarning("App Not Found", f"{app_name} not found in Adobe folders.")
    if blocked:
        messagebox.showinfo("Blocked", f"Internet blocked for: {', '.join(blocked)}")
    update_status_labels()

# Unblock internet for selected apps
def unblock_selected_apps():
    unblocked = []
    for app_name, var in app_vars.items():
        if var.get():
            remove_firewall_rule(app_name)
            unblocked.append(app_name)
    if unblocked:
        messagebox.showinfo("Unblocked", f"Internet unblocked for: {', '.join(unblocked)}")
    update_status_labels()
# ========== GUI ==========
root = tb.Window(themename="superhero")
root.title("AdobeShield - Adobe internet access blocker")

# Determine if we're in a PyInstaller bundle
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

icon_path = os.path.join(base_path, "logo.ico")

try:
    root.iconbitmap(icon_path)
    
except Exception as e:
    print(f"Icon load failed: {e}")

root.geometry("420x350")
root.resizable(False, False)

# Title
title = tb.Label(root, text="Manage Adobe App Internet Access", font=("Segoe UI", 14, "bold"))
title.pack(pady=15)

# Checkboxes and Status
app_vars = {}
status_labels = {}

for app in adobe_apps:
    frame = tb.Frame(root)
    frame.pack(fill="x", padx=30, pady=2)

    var = tk.BooleanVar()
    chk = tb.Checkbutton(frame, text=app, variable=var, bootstyle="primary")
    chk.pack(side="left")

    status = tb.Label(frame, text="Checking...", font=("Segoe UI", 9))
    status.pack(side="right")
    app_vars[app] = var
    status_labels[app] = status

# Buttons
btn_frame = tb.Frame(root)
btn_frame.pack(pady=20)

tb.Button(btn_frame, text="Block Internet", command=block_selected_apps,
          bootstyle="danger", width=18).pack(side="left", padx=10)

tb.Button(btn_frame, text="Allow Internet", command=unblock_selected_apps,
          bootstyle="success", width=18).pack(side="left", padx=10)

# Refresh Button
tb.Button(root, text="Refresh Status", command=update_status_labels,
          bootstyle="info", width=20).pack(pady=5)

# Footer
footer = tb.Label(root, text="Developed by Dark Venom", font=("Segoe UI", 8), anchor="center")
footer.pack(side="bottom", pady=5)

# Load initial status
update_status_labels()

root.mainloop()
