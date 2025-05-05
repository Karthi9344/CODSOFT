import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔢 GUI_Calculator")
        self.root.geometry("420x550")
        self.root.resizable(False, False)

        self.dark_mode = True
        self.themes = {
            "dark": {"bg": "#1e1e2f", "fg": "#ffffff", "btn": "#282c3f", "active": "#3c415c", "result": "#2e2e3e"},
            "light": {"bg": "#f4f4f4", "fg": "#000000", "btn": "#d0d0d0", "active": "#c0c0c0", "result": "#ffffff"}
        }

        self.expression = ""
        self.input_text = tk.StringVar()
        self.history = []

        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(expand=False, fill="both")

        self.entry = tk.Entry(self.top_frame, font=("Segoe UI", 22), textvariable=self.input_text, bd=0, justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, ipady=20, padx=10, pady=10, sticky="nsew")

        self.theme_button = tk.Button(self.top_frame, text="☀️/🌙", font=("Arial", 14), command=self.toggle_theme)
        self.theme_button.grid(row=0, column=4, padx=5, sticky="e")

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(expand=True, fill="both")

        buttons = [
            ['C', '(', ')', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '**']
        ]

        for r, row in enumerate(buttons):
            for c, btn in enumerate(row):
                tk.Button(self.button_frame, text=btn, font=("Segoe UI", 18),
                          command=lambda b=btn: self.on_button_click(b)).grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        for i in range(5):
            self.button_frame.rowconfigure(i, weight=1)
        for j in range(4):
            self.button_frame.columnconfigure(j, weight=1)

        self.history_frame = tk.Frame(self.root, height=120)
        self.history_frame.pack(fill="both")
        self.history_label = tk.Label(self.history_frame, text="History:", anchor='w', font=("Segoe UI", 12, "bold"))
        self.history_label.pack(anchor='w', padx=10, pady=2)
        self.history_listbox = tk.Listbox(self.history_frame, font=("Segoe UI", 12), height=5)
        self.history_listbox.pack(fill="both", padx=10, pady=(0, 10), expand=True)

    def on_button_click(self, button):
        if button == 'C':
            self.expression = ""
            self.input_text.set("")
        elif button == '=':
            try:
                result = str(eval(self.expression))
                self.input_text.set(result)
                self.history.append(f"{self.expression} = {result}")
                self.history_listbox.insert(tk.END, f"{self.expression} = {result}")
                self.expression = result  # enable chaining
            except Exception:
                messagebox.showerror("Error", "Invalid Expression")
                self.expression = ""
                self.input_text.set("")
        else:
            self.expression += str(button)
            self.input_text.set(self.expression)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes["dark"] if self.dark_mode else self.themes["light"]
        self.root.config(bg=theme["bg"])
        self.top_frame.config(bg=theme["bg"])
        self.entry.config(bg=theme["result"], fg=theme["fg"], insertbackground=theme["fg"])
        self.theme_button.config(bg=theme["btn"], fg=theme["fg"], activebackground=theme["active"])
        self.button_frame.config(bg=theme["bg"])
        self.history_frame.config(bg=theme["bg"])
        self.history_label.config(bg=theme["bg"], fg=theme["fg"])
        self.history_listbox.config(bg=theme["result"], fg=theme["fg"])

        for child in self.button_frame.winfo_children():
            child.config(bg=theme["btn"], fg=theme["fg"], activebackground=theme["active"])

if __name__ == "__main__":
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()
