import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

tasks=[]

# Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Save tasks to file
def save_tasks():
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Add new task
def add_task():
    task = entry.get()
    priority = priority_var.get()
    due = due_date.get_date().strftime("%Y-%m-%d")
    if task != "":
        tasks.append({"task": task, "done": False, "priority": priority, "due": due})
        update_listbox()
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Empty Task", "Please enter a task!")

# Delete selected task
def delete_task():
    try:
        selected = listbox.curselection()[0]
        tasks.pop(selected)
        update_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to delete!")

# Mark as done/undone
def mark_done():
    try:
        selected = listbox.curselection()[0]
        tasks[selected]["done"] = not tasks[selected]["done"]
        update_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to mark!")

# Clear all done tasks
def clear_completed():
    global tasks
    tasks = [t for t in tasks if not t['done']]
    update_listbox()
    save_tasks()

# Search filter
def search_tasks(*args):
    global tasks
    keyword = search_var.get().lower()
    listbox.delete(0, tk.END)
    for i, t in enumerate(tasks):
        if keyword in t["task"].lower():
            status = "✅" if t["done"] else "❌"
            listbox.insert(
                tk.END,
                f"{i+1}. {status} {t['task']} | {t.get('priority', 'Medium')} | Due: {t.get('due', 'No Date')}"
            )

# Update listbox
def update_listbox():
    listbox.delete(0, tk.END)
    for i, t in enumerate(tasks):
        status = "✅" if t["done"] else "❌"
        listbox.insert(
            tk.END,
            f"{i+1}. {status} {t['task']} | {t.get('priority', 'Medium')} | Due: {t.get('due', 'No Date')}"
        )

# GUI Setup
root = tk.Tk()
root.title("To-Do List - CodSoft Internship Project")
root.geometry("600x500")
root.resizable(False, False)

# Task Display - place first before search_var is used
listbox = tk.Listbox(root, width=80, height=15)
listbox.pack(pady=10)

# Search Box
search_var = tk.StringVar()
search_var.trace("w", search_tasks)
search_entry = tk.Entry(root, textvariable=search_var, width=40)
search_entry.pack(pady=5)
search_entry.insert(0, "Search task...")

# Frame for input & buttons
frame = tk.Frame(root)
frame.pack(pady=10)

# Task Entry
entry = tk.Entry(frame, width=30)
entry.grid(row=0, column=0, padx=5, pady=5)

priority_var = tk.StringVar()
priority_menu = tk.OptionMenu(frame, priority_var, "Low", "Medium", "High")
priority_menu.grid(row=0, column=1, padx=5)
priority_var.set("Medium")

due_date = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
due_date.grid(row=0, column=2, padx=5)

# Buttons
btn_add = tk.Button(frame, text="Add Task", width=12, command=add_task)
btn_add.grid(row=0, column=3, padx=5)

btn_done = tk.Button(frame, text="Mark Done", width=12, command=mark_done)
btn_done.grid(row=1, column=0, pady=5)

btn_delete = tk.Button(frame, text="Delete Task", width=12, command=delete_task)
btn_delete.grid(row=1, column=1, pady=5)

btn_clear = tk.Button(frame, text="Clear Completed", width=15, command=clear_completed)
btn_clear.grid(row=1, column=2, pady=5)

# Load existing tasks and display
tasks = load_tasks()
update_listbox()

root.mainloop()
