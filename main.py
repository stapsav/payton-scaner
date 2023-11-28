
Fool Price, [27.11.2023 22:09]
import os
import json
import tkinter as tk
from tkinter import filedialog

def find_additional_info(folder_path):
    info_files = ["UserInformation.txt", "SystemInformation.txt"]
    user_info = ""
    for file_name in info_files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    if "IP" in line or "Country" in line:
                        user_info += line.strip() + "\n"
    return user_info

def search_and_extract(file_path, search_str, log_file, found_pairs):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if search_str.lower() in line.lower():
                    print(f"Found search string in {file_path}")
                    user = extract_data(lines, i + 1, "Username:")
                    password = extract_data(lines, i + 2, "Password:")
                    info = line.strip()  # Сохраняем всю строку, где найдено совпадение
                    user_info = find_additional_info(os.path.dirname(file_path))  # Ищем дополнительную информацию
                    if user and password and (user, password) not in found_pairs:
                        found_pairs.add((user, password))
                        with open(log_file, 'a', encoding='utf-8') as log:
                            log_entry = f"------------------------------\n{info}\n{user_info}{user} : {password}\n"
                            log.write(log_entry)
                            print(f"Written to log: {log_entry}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def extract_data(lines, index, keyword):
    if index < len(lines):
        parts = lines[index].strip().split()
        if parts and parts[0].lower() == keyword.lower():
            return ' '.join(parts[1:])
    return None

def start_search():
    folders_to_search = folder_paths
    file_to_find = file_name_var.get()
    search_string = search_string_var.get()
    log_folder = log_folder_var.get()
    log_file = os.path.join(log_folder, "logs.txt")

    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    found_pairs = set()

    for folder_to_search in folders_to_search:
        for root, dirs, files in os.walk(folder_to_search):
            if file_to_find in files:
                file_path = os.path.join(root, file_to_find)
                search_and_extract(file_path, search_string, log_file, found_pairs)

    result_label.config(text='Search completed.')

def browse_folder(var=None):
    directory = filedialog.askdirectory()
    if directory:
        if var:
            var.set(directory)
        else:
            folder_paths.append(directory)
            folder_path_label.config(text='\n'.join(folder_paths))

def save_settings():
    settings = {
        "folder_paths": folder_paths,
        "file_name": file_name_var.get(),
        "search_string": search_string_var.get(),
        "log_folder": log_folder_var.get()
    }
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

def load_settings():
    try:
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                return settings
    except json.JSONDecodeError as e:
        print(f"Error reading settings file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return {}

# Создание главного окна
root = tk.Tk()
root.title("File Content Search and Log")

# Загрузка настроек
settings = load_settings()
folder_paths = settings.get("folder_paths", [])
file_name_var = tk.StringVar(value=settings.get("file_name", ""))
search_string_var = tk.StringVar(value=settings.get("search_string", ""))
log_folder_var = tk.StringVar(value=settings.get("log_folder", ""))

Fool Price, [27.11.2023 22:09]
# Создание и расположение виджетов
tk.Label(root, text="Search Folders:").grid(row=0, column=0, sticky="w")
folder_path_label = tk.Label(root, text="\n".join(folder_paths))
folder_path_label.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Add Folder...", command=lambda: browse_folder()).grid(row=0, column=2)

tk.Label(root, text="File Name:").grid(row=1, column=0, sticky="w")
file_name_entry = tk.Entry(root, textvariable=file_name_var, width=40)
file_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Search String:").grid(row=2, column=0, sticky="w")
search_string_entry = tk.Entry(root, textvariable=search_string_var, width=40)
search_string_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Log Folder:").grid(row=3, column=0, sticky="w")
log_folder_entry = tk.Entry(root, textvariable=log_folder_var, width=40)
log_folder_entry.grid(row=3, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=lambda: browse_folder(log_folder_var)).grid(row=3, column=2)

search_button = tk.Button(root, text="Start Search", command=start_search)
search_button.grid(row=4, column=1, padx=5, pady=5, sticky="e")

result_label = tk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

# Запуск главного цикла обработки событий
root.protocol("WM_DELETE_WINDOW", lambda: [save_settings(), root.destroy()])
root.mainloop()
