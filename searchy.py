import os
import json
import configparser
import tkinter as tk
from tkinter import messagebox, PhotoImage

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Check if the necessary section and key exist in the config file
if 'Paths' in config and 'config_file' in config['Paths']:
    config_file_path = config['Paths']['config_file']
else:
    messagebox.showerror("Error", "The config.ini file is missing necessary sections.")
    exit()  # Exit if configuration file is incorrect

# Preset directory from the config file
PRESET_DIRECTORY = config_file_path  # Set the directory from config file

def search_and_open_file(directory, filename):
    filename = filename.lower()
    valid_extensions = ['.jpg', '.png']
    
    for root, _, files in os.walk(directory):
        for file in files:
            base_name, ext = os.path.splitext(file.lower())
            if base_name == filename and ext in valid_extensions:
                file_path = os.path.join(root, file)
                open_file(file_path)
                return
    messagebox.showerror("Error", translations[current_language]["file_not_found"])

def open_file(file_path):
    try:
        os.startfile(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Error opening file: {e}")

def search_file(event=None):
    directory = PRESET_DIRECTORY
    filename = entry_filename.get().strip()
    if filename:
        search_and_open_file(directory, filename)
    else:
        messagebox.showwarning("Warning", translations[current_language]["enter_code"])

def clear_entry():
    entry_filename.delete(0, tk.END)

def load_translations(file_name):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def change_language(lang):
    global current_language
    current_language = lang
    update_interface()

def update_interface():
    label_header.config(text=translations[current_language]["header"])
    label_code.config(text=translations[current_language]["code_label"])
    search_button.config(text=translations[current_language]["search"])
    clear_button.config(text=translations[current_language]["clear"])

# Load translations
translations = load_translations("translations.json")
current_language = "lt"  # Default language

# GUI Setup
root = tk.Tk()
root.title("Searchy")
root.configure(bg="white")

# Set window size and position
window_width, window_height = 650, 255
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
position_left = int((screen_width - window_width) / 2)
position_top = 0
root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
root.resizable(False, False)

menu_bar = tk.Menu(root)
language_menu = tk.Menu(menu_bar, tearoff=0)
language_menu.add_command(label="Lietuvių", command=lambda: change_language("lt"))
language_menu.add_command(label="Русский", command=lambda: change_language("ru"))
language_menu.add_command(label="English", command=lambda: change_language("en"))
menu_bar.add_cascade(label="*", menu=language_menu)
root.config(menu=menu_bar)

# Logo setup
script_directory = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(script_directory, "logo.png")
logo = PhotoImage(file=logo_path)
tk.Label(root, image=logo, bg="white").pack(anchor="nw")

# Header
label_header = tk.Label(root, text=translations[current_language]["header"], bg="white", font=("Arial", 15))
label_header.pack(pady=5)

# Search Bar
frame = tk.Frame(root, bg="white")
frame.pack(padx=15, pady=15)

label_code = tk.Label(frame, text=translations[current_language]["code_label"], bg="white", font=("Arial", 13))
label_code.grid(row=0, column=0, sticky="w")
entry_filename = tk.Entry(frame, width=40, font=("Arial", 15))
entry_filename.grid(row=0, column=1, padx=12, pady=5)
entry_filename.bind("<Return>", search_file)

frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)

# Buttons
clear_button = tk.Button(frame, text=translations[current_language]["clear"], command=clear_entry, font=("Arial", 12), bg="#BF0A30", fg="white", padx=10, pady=5)
clear_button.grid(row=1, column=2, columnspan=2, padx=5, pady=15, sticky="ew")

search_button = tk.Button(frame, text=translations[current_language]["search"], command=search_file, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=15, sticky="ew")

root.mainloop()
