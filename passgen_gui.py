#!/usr/bin/env python3

# Import required libraries for GUI, randomness, and string handling
import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import re

# Generate a basic password using letters and digits
def generate_basic(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Generate a strong password using letters, digits, and punctuation
def generate_strong(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# Check password strength based on length and character variety
def check_strength(password):
    length = len(password)
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[^\w]', password))
    
    # score counts how many character types are present
    score = sum([has_lower, has_upper, has_digit, has_symbol])
    if length >= 12 and score == 4:
        return "Strong", "#28a745"      # green
    elif length >= 8 and score >= 3:
        return "Moderate", "#ffc107"    # yellow
    else:
        return "Weak", "#dc3545"        # red
        
# Main application class for the password generator GUI
class PasswordGeneratorApp:
    def __init__(self, root):
        
        # Store reference to main window, set title, size, and appearance
        self.root = root
        self.root.title("🔐 Password Generator")
        self.root.geometry("840x385")
        self.root.resizable(True, True)
        self.root.configure(bg="#1e1e1e")
        
        # Define variables for password length, type, result, and GUI style
        self.length_var = tk.IntVar(value=32)
        self.type_var = tk.StringVar(value="basic")
        self.password_var = tk.StringVar()

        self.set_dark_style()    # Set custom dark theme for widgets
        self.build_ui()    # Set custom dark theme for widgets
        
    # Configure custom ttk styles for dark mode and buttons
    def set_dark_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#1e1e1e", foreground="#ffffff", fieldbackground="#2e2e2e")

        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TProgressbar", troughcolor="#2e2e2e", background="#28a745", thickness=20)

        style.configure("TButton",
                        font=("Segoe UI", 10),
                        padding=6,
                        background="#690069",
                        foreground="#ffffff")
        style.map("TButton",
                  background=[('active', '#8a008a')],
                  foreground=[('active', '#ffffff')])

        style.configure("Hover.TButton",
                        background="#8a008a",
                        foreground="#ffffff")
        
    # Add mouse hover effect to buttons
    def add_hover_effect(self, widget):
        def on_enter(e):
            widget.configure(style="Hover.TButton")
        def on_leave(e):
            widget.configure(style="TButton")
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        
    # Add mouse hover effect with background change for radiobuttons
    def add_radio_hover_effect(self, widget):
        def on_enter(e):
            widget.configure(bg="#690069")
        def on_leave(e):
            widget.configure(bg="#1e1e1e")
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        
    # Build all UI components for password generator
    def build_ui(self):
        padding = {"padx": 10, "pady": 5}
        
        # Password length input
        ttk.Label(self.root, text="Password Length:").pack(**padding)
        length_spinbox = tk.Spinbox(self.root,
                           from_=4, to=100,
                           textvariable=self.length_var,
                           width=10,
                           bg="#BBBBBB",             # white background for input box
                           fg="#000000",              # black text for input
                           buttonbackground="#690069",  # purple arrows background
                           highlightthickness=0,
                           relief="flat",
                           font=("Segoe UI", 10))
        
        length_spinbox.pack()

        # Password type selection
        ttk.Label(self.root, text="Password Type:").pack(**padding)
        radio_frame = ttk.Frame(self.root)
        radio_frame.pack()
        
        # Basic password radio button
        basic_rb = tk.Radiobutton(radio_frame, text="Basic (A-Z, a-z, 0-9)",
                                  variable=self.type_var, value="basic",
                                  bg="#1e1e1e", fg="white", selectcolor="#690069",
                                  activebackground="#690069", activeforeground="white",
                                  font=("Segoe UI", 10), indicatoron=1,
                                  width=25,
                                  highlightthickness=0)
        basic_rb.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.add_radio_hover_effect(basic_rb)
        
        # Strong password radio button
        strong_rb = tk.Radiobutton(radio_frame, text="Strong (+ symbols)",
                                   variable=self.type_var, value="strong",
                                   bg="#1e1e1e", fg="white", selectcolor="#690069",
                                   activebackground="#690069", activeforeground="white",
                                   font=("Segoe UI", 10), indicatoron=1,
                                   width=25,
                                   highlightthickness=0)
        strong_rb.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.add_radio_hover_effect(strong_rb)
        
        # Generate password button
        generate_btn = ttk.Button(self.root, text="Generate Password", command=self.generate_password)
        generate_btn.pack(pady=10)
        self.add_hover_effect(generate_btn)
        
        # Output entry displaying the generated password
        self.output_entry = ttk.Entry(self.root, textvariable=self.password_var, width=50, justify="center", font=("Segoe UI", 10))
        self.output_entry.pack(pady=5)

        # Strength label
        self.strength_label = ttk.Label(self.root, text="Strength: N/A", font=("Segoe UI", 10))
        self.strength_label.pack(pady=(10, 2))

        # Progress bar
        self.strength_bar = ttk.Progressbar(self.root, length=300, mode='determinate', maximum=100)
        self.strength_bar.pack(pady=(0, 10))

        # Copy to clipboard button
        copy_btn = ttk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.pack()
        self.add_hover_effect(copy_btn)

    # Generate password and update GUI with result and strength
    def generate_password(self):
        try:
            length = self.length_var.get()
            if length <= 0:
                raise ValueError
            # Select password generation method based on radio button
            pw = generate_basic(length) if self.type_var.get() == "basic" else generate_strong(length)
            self.password_var.set(pw)
            self.update_strength_display(pw)
        except ValueError:
            # Show error if invalid length is entered
            messagebox.showerror("Invalid Input", "Please enter a valid length.")
            
    # Update the strength indicator bar and label style
    def update_strength_display(self, password):
        strength, color = check_strength(password)
        self.strength_label.config(text=f"Strength: {strength}", foreground=color)

        if strength == "Strong":
            self.strength_bar['value'] = 100
        elif strength == "Moderate":
            self.strength_bar['value'] = 60
        else:
            self.strength_bar['value'] = 30

        self.root.update_idletasks()
        
    # Copy password to clipboard and notify user
    def copy_to_clipboard(self):
        pw = self.password_var.get()
        if pw:
            self.root.clipboard_clear()
            self.root.clipboard_append(pw)
            messagebox.showinfo("Copied", "Password copied to clipboard!")

# Run the application when executed directly
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
