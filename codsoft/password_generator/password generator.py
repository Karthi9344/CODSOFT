import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import string
import random
import pyperclip
import qrcode
from PIL import Image, ImageTk
import io
import datetime

# --- Password Strength Checker ---
def check_strength(password):
    length = len(password)
    upper = any(c.isupper() for c in password)
    lower = any(c.islower() for c in password)
    digit = any(c.isdigit() for c in password)
    symbol = any(c in string.punctuation for c in password)

    score = sum([upper, lower, digit, symbol])
    if length >= 12 and score == 4:
        return "Strong", "green"
    elif length >= 8 and score >= 3:
        return "Medium", "orange"
    else:
        return "Weak", "red"

# --- Generate Password ---
def generate_password():
    try:
        length = int(length_var.get())
        if length < 4:
            raise ValueError("Length must be at least 4")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid password length (min 4).")
        return

    use_upper = upper_var.get()
    use_digits = digit_var.get()
    use_symbols = symbol_var.get()
    avoid_ambiguous = avoid_var.get()

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_upper else ''
    digits = string.digits if use_digits else ''
    symbols = string.punctuation if use_symbols else ''

    all_chars = lower + upper + digits + symbols

    if avoid_ambiguous:
        ambiguous = 'O0Il1'
        all_chars = ''.join(c for c in all_chars if c not in ambiguous)

    if not all_chars:
        messagebox.showerror("Selection Error", "Please select at least one character set.")
        return

    password = random.choice(lower)
    if use_upper: password += random.choice(upper)
    if use_digits: password += random.choice(digits)
    if use_symbols: password += random.choice(symbols)

    while len(password) < length:
        password += random.choice(all_chars)

    password = ''.join(random.sample(password, len(password)))
    password_var.set(password)
    pyperclip.copy(password)

    # Strength Meter
    strength, color = check_strength(password)
    strength_label.config(text=f"Strength: {strength}", fg=color)

    # Save to file
    with open("passwords.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {password}\n")

# --- Show QR Code ---
def show_qr():
    password = password_var.get()
    if not password:
        messagebox.showwarning("No Password", "Generate a password first.")
        return
    img = qrcode.make(password)
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    bio.seek(0)
    qr_img = Image.open(bio)
    qr_img = qr_img.resize((200, 200))
    img_tk = ImageTk.PhotoImage(qr_img)
    qr_label.config(image=img_tk)
    qr_label.image = img_tk

# --- Password Validator ---
def validate_password():
    pwd = validate_entry.get()
    if not pwd:
        messagebox.showwarning("No Input", "Enter a password to validate.")
        return
    strength, color = check_strength(pwd)
    validate_result.config(text=f"Strength: {strength}", fg=color)

# --- GUI Setup ---
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("600x600")
root.resizable(False, False)

length_var = tk.StringVar(value='12')
password_var = tk.StringVar()

# --- Options Frame ---
frame = tk.Frame(root)
frame.pack(pady=10)

# Length
tk.Label(frame, text="Password Length:").grid(row=0, column=0, sticky='w')
tk.Entry(frame, textvariable=length_var, width=5).grid(row=0, column=1, sticky='w')

# Checkboxes
upper_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)
avoid_var = tk.BooleanVar()

tk.Checkbutton(frame, text="Include Uppercase", variable=upper_var).grid(row=1, column=0, sticky='w')
tk.Checkbutton(frame, text="Include Numbers", variable=digit_var).grid(row=2, column=0, sticky='w')
tk.Checkbutton(frame, text="Include Symbols", variable=symbol_var).grid(row=3, column=0, sticky='w')
tk.Checkbutton(frame, text="Avoid Ambiguous (O, 0, l, 1)", variable=avoid_var).grid(row=4, column=0, sticky='w', columnspan=2)

# Buttons
tk.Button(root, text="Generate Password", command=generate_password, width=20).pack(pady=5)
tk.Entry(root, textvariable=password_var, width=40, font=("Arial", 12)).pack(pady=5)
strength_label = tk.Label(root, text="Strength: ", font=("Arial", 10))
strength_label.pack()
tk.Button(root, text="Show QR Code", command=show_qr).pack(pady=5)
qr_label = tk.Label(root)
qr_label.pack()

# --- Password Validator ---
tk.Label(root, text="\nValidate Your Own Password:").pack()
validate_entry = tk.Entry(root, width=40)
validate_entry.pack(pady=2)
tk.Button(root, text="Check Strength", command=validate_password).pack()
validate_result = tk.Label(root, text="", font=("Arial", 10))
validate_result.pack()

root.mainloop()
