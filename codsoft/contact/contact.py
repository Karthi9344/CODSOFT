import tkinter as tk
from tkinter import messagebox, ttk
import json
import re
import csv
import qrcode

# Load contacts from file
def load_contacts():
    try:
        with open("contacts.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save contacts to file
def save_contacts(contacts):
    with open("contacts.json", "w") as file:
        json.dump(contacts, file)

# Validate phone number
def validate_phone(phone):
    return re.match(r'^[0-9]{10}$', phone)

# Validate email
def validate_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

# Add contact
def add_contact():
    name = entry_name.get()
    number = entry_number.get()
    email = entry_email.get()
    address = entry_address.get()

    if name and number and email and address:
        if not validate_phone(number):
            messagebox.showerror("Error", "Invalid phone number!")
            return
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email!")
            return
        contacts[name] = {"number": number, "email": email, "address": address}
        save_contacts(contacts)
        messagebox.showinfo("Success", "Contact added!")
        clear_entries()
        view_contacts()
    else:
        messagebox.showerror("Error", "All fields are required!")

# View contacts
def view_contacts():
    for row in tree.get_children():
        tree.delete(row)
    for name, details in contacts.items():
        tree.insert("", tk.END, values=(name, details['number'], details['email'], details['address']))

# Search contact
def search_contact():
    search_name = entry_name.get().lower()
    filtered = {name: details for name, details in contacts.items() if search_name in name.lower()}

    if filtered:
        for row in tree.get_children():
            tree.delete(row)
        for name, details in filtered.items():
            tree.insert("", tk.END, values=(name, details['number'], details['email'], details['address']))
    else:
        messagebox.showerror("Error", "No contact found!")

# Update contact
def update_contact():
    name = entry_name.get()
    if name in contacts:
        number = entry_number.get()
        email = entry_email.get()
        address = entry_address.get()
        if not validate_phone(number):
            messagebox.showerror("Error", "Invalid phone number!")
            return
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email!")
            return
        contacts[name] = {"number": number, "email": email, "address": address}
        save_contacts(contacts)
        messagebox.showinfo("Success", "Contact updated!")
        clear_entries()
        view_contacts()
    else:
        messagebox.showerror("Error", "Contact not found!")

# Delete contact
def delete_contact():
    name = entry_name.get()
    if name in contacts:
        confirm = messagebox.askyesno("Confirm", f"Delete {name}?")
        if confirm:
            del contacts[name]
            save_contacts(contacts)
            messagebox.showinfo("Success", "Contact deleted!")
            clear_entries()
            view_contacts()
    else:
        messagebox.showerror("Error", "Contact not found!")

# Export contacts to CSV
def export_contacts():
    with open("contacts.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email", "Address"])
        for name, details in contacts.items():
            writer.writerow([name, details['number'], details['email'], details['address']])
    messagebox.showinfo("Success", "Exported to contacts.csv!")

# Generate QR Code for contact
def generate_qr():
    name_input = entry_name.get().lower()
    matched_name = None
    
    for name in contacts:
        if name_input in name.lower():
            matched_name = name
            break

    if matched_name:
        details = contacts[matched_name]
        qr_data = f"Name: {matched_name}\nPhone: {details['number']}\nEmail: {details['email']}\nAddress: {details['address']}"
        qr_img = qrcode.make(qr_data)
        qr_path = f"{matched_name}_contact_qr.png"
        qr_img.save(qr_path)
        messagebox.showinfo("Success", f"QR saved as {qr_path}")
    else:
        messagebox.showerror("Error", "Contact not found!")
        
# Clear entry fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_number.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)

# Password protection
def verify_password():
    password = "secret123"
    entered = entry_password.get()
    if entered == password:
        password_window.destroy()
        window.deiconify()
    else:
        messagebox.showerror("Error", "Incorrect password!")

# Main window
window = tk.Tk()
window.title("Contact Book")
window.geometry("700x500")
window.resizable(False, False)

# Password popup
password_window = tk.Toplevel(window)
password_window.title("Login")
password_window.geometry("300x150")
tk.Label(password_window, text="Enter Password:").grid(row=0, column=0, pady=10)
entry_password = tk.Entry(password_window, show="*")
entry_password.grid(row=0, column=1)
tk.Button(password_window, text="Login", command=verify_password).grid(row=1, column=0, columnspan=2, pady=10)
window.withdraw()

contacts = load_contacts()

# Entry fields
tk.Label(window, text="Name:").grid(row=0, column=0)
entry_name = tk.Entry(window)
entry_name.grid(row=0, column=1)

tk.Label(window, text="Phone:").grid(row=1, column=0)
entry_number = tk.Entry(window)
entry_number.grid(row=1, column=1)

tk.Label(window, text="Email:").grid(row=2, column=0)
entry_email = tk.Entry(window)
entry_email.grid(row=2, column=1)

tk.Label(window, text="Address:").grid(row=3, column=0)
entry_address = tk.Entry(window)
entry_address.grid(row=3, column=1)

# Buttons
tk.Button(window, text="Add", command=add_contact).grid(row=4, column=0, pady=5)
tk.Button(window, text="View", command=view_contacts).grid(row=4, column=1)
tk.Button(window, text="Search", command=search_contact).grid(row=5, column=0)
tk.Button(window, text="Update", command=update_contact).grid(row=5, column=1)
tk.Button(window, text="Delete", command=delete_contact).grid(row=6, column=0)
tk.Button(window, text="Export CSV", command=export_contacts).grid(row=6, column=1)
tk.Button(window, text="Generate QR", command=generate_qr).grid(row=7, column=0, columnspan=2, pady=5)

# Treeview to show contacts
tree = ttk.Treeview(window, columns=("Name", "Phone", "Email", "Address"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.heading("Address", text="Address")
tree.grid(row=8, column=0, columnspan=2, pady=10)

# Start app
window.mainloop()
