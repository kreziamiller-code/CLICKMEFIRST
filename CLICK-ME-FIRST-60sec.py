import tkinter as tk
from tkinter import messagebox
import urllib.request
import json
import webbrowser
import uuid
from pathlib import Path

SERVER = "https://activation-code.onrender.com"
APP_DIR = Path.home() / "AppData" / "Roaming" / "CLICK-ME-FIRST"
DEVICE_FILE = APP_DIR / "device.id"

def get_device_id():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    if DEVICE_FILE.exists():
        value = DEVICE_FILE.read_text(encoding="utf-8").strip()
        if value:
            return value
    value = str(uuid.uuid4())
    DEVICE_FILE.write_text(value, encoding="utf-8")
    return value

def post_json(path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        SERVER + path,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))

def activate():
    code = code_var.get().strip().upper()
    if not code:
        messagebox.showwarning("Activation", "Please enter your activation code.")
        return

    button.config(state="disabled", text="CHECKING...")
    status.set("Connecting to activation server...")
    status_label.config(fg="#fbbf24")

    try:
        result = post_json("/api/register", {
            "deviceId": get_device_id(),
            "code": code
        })

        if result.get("success") and result.get("status") == "approved":
            status.set("Activated")
            status_label.config(fg="#35d07f")
            messagebox.showinfo("CLICK-ME-FIRST", "Activation successful.")
        else:
            status.set("Activation failed")
            status_label.config(fg="#fb7185")
            messagebox.showerror(
                "Activation failed",
                result.get("error", "The activation code was not accepted.")
            )
    except Exception as exc:
        status.set("Connection error")
        status_label.config(fg="#fb7185")
        messagebox.showerror(
            "Connection error",
            "Could not connect to your activation server.\n\n" + str(exc)
        )
    finally:
        button.config(state="normal", text="ACTIVATE")

def open_server():
    webbrowser.open(SERVER)

root = tk.Tk()
root.title("CLICK-ME-FIRST")
root.geometry("440x350")
root.resizable(False, False)
root.configure(bg="#0d1020")

tk.Label(root, text="CLICK-ME-FIRST", font=("Segoe UI", 24, "bold"),
         fg="white", bg="#0d1020").pack(pady=(30, 2))

tk.Label(root, text="Powered by malupiton", font=("Segoe UI", 10, "bold"),
         fg="#a78bfa", bg="#0d1020").pack()

tk.Label(root, text="Activation Launcher", font=("Segoe UI", 10),
         fg="#9298b2", bg="#0d1020").pack(pady=(4, 22))

card = tk.Frame(root, bg="#171b2e", highlightthickness=1,
                highlightbackground="#2b3150")
card.pack(padx=25, fill="x")

tk.Label(card, text="Activation Code", font=("Segoe UI", 10, "bold"),
         fg="#d8dcf0", bg="#171b2e").pack(anchor="w", padx=18, pady=(18, 7))

code_var = tk.StringVar()
entry = tk.Entry(card, textvariable=code_var, font=("Consolas", 15, "bold"),
                 justify="center", bg="#0f1322", fg="white",
                 insertbackground="white", relief="flat")
entry.pack(padx=18, fill="x", ipady=10)
entry.focus()

status = tk.StringVar(value="Not activated")
status_label = tk.Label(card, textvariable=status,
                        font=("Segoe UI", 9, "bold"),
                        fg="#fbbf24", bg="#171b2e")
status_label.pack(pady=10)

button = tk.Button(card, text="ACTIVATE", command=activate,
                   font=("Segoe UI", 10, "bold"),
                   fg="white", bg="#6d5dfc",
                   activeforeground="white",
                   activebackground="#7c6cff",
                   relief="flat", cursor="hand2")
button.pack(padx=18, fill="x", ipady=8, pady=(0, 16))

tk.Button(root, text="Open My Activation Server", command=open_server,
          font=("Segoe UI", 9, "bold"),
          fg="#b8bde0", bg="#171b2e",
          activeforeground="white",
          activebackground="#222844",
          relief="flat", cursor="hand2").pack(pady=15)

tk.Label(root, text=SERVER, font=("Consolas", 8),
         fg="#5f667d", bg="#0d1020").pack(side="bottom", pady=10)

root.mainloop()
