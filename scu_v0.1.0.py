import os
import difflib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

def log_message(log_widget, message):
    """Log a message in the log widget."""
    if log_widget:
        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, message + "\n")
        log_widget.see(tk.END)  # Scroll to the latest message
        log_widget.config(state=tk.DISABLED)

def load_scripts(file_paths, log_widget):
    """Load the contents of the scripts based on selected file extension."""
    log_message(log_widget, "Loading scripts...")
    scripts = {}
    for path in file_paths:
        try:
            with open(path, 'r') as file:
                scripts[path] = file.readlines()
            log_message(log_widget, f"Loaded script: {path}")
        except Exception as e:
            error_message = f"Error reading {path}: {e}"
            print(error_message)
            log_message(log_widget, error_message)
    return scripts

def compare_scripts(script_contents, show_additions, show_removals, log_widget):
    """Compare each file to the previous one in the list."""
    log_message(log_widget, "Comparing scripts...")
    comparisons = {}
    script_names = list(script_contents.keys())
    
    # Loop to compare each file only to the one before it
    for i in range(1, len(script_names)):
        script1 = script_names[i - 1]
        script2 = script_names[i]
        diff = difflib.unified_diff(
            script_contents[script1],
            script_contents[script2],
            fromfile=script1,
            tofile=script2,
            lineterm=''
        )
        
        # Collect all lines in the diff that match the selected options
        filtered_diff = []
        for line in diff:
            if (line.startswith('+') and show_additions) or \
               (line.startswith('-') and show_removals) or \
               not line.startswith(('+', '-')):
                filtered_diff.append(line)
        
        # Only store comparisons if there are actual differences
        if filtered_diff:
            comparisons[(script1, script2)] = filtered_diff
            log_message(log_widget, f"Differences found between {script1} and {script2}.")
        else:
            log_message(log_widget, f"No differences found between {script1} and {script2}.")
    
    return comparisons


def show_differences(comparisons, show_additions, show_removals):
    """Display differences in a new window with an option to save as a .txt file."""
    if not comparisons:
        messagebox.showinfo("Result", "No differences found.")
        return
    
    # Create a new Toplevel window to show differences
    diff_window = tk.Toplevel()
    diff_window.title("Differences")

    # Text widget to display differences
    diff_text = tk.Text(diff_window, wrap=tk.WORD, width=80, height=25)
    diff_text.pack(padx=10, pady=10)

    # Define text color tags for different types of lines
    diff_text.tag_config("file_names", foreground="orange")
    diff_text.tag_config("addition", foreground="green")
    diff_text.tag_config("removal", foreground="red")

    # Format and display differences
    log_content = f"This log was generated at {datetime.now().strftime('%H:%M')} on {datetime.now().strftime('%d/%m/%Y')}\n"
    for (script1, script2), diff in comparisons.items():
        # Add file comparison header with color
        diff_text.insert(tk.END, f'\n"{script1}" was compared to "{script2}":\n', "file_names")
        log_content += f'\n"{script1}" was compared to "{script2}", the differences are as follows:\n'
        
        # Insert each line of the diff with appropriate label and color coding
        for line in diff:
            if line.startswith('+') and show_additions:
                labeled_line = f"+ {line[1:].strip()}"  # Prefix line with "+"
                diff_text.insert(tk.END, f"{labeled_line}\n", "addition")
                log_content += f"{labeled_line}\n"
            elif line.startswith('-') and show_removals:
                labeled_line = f"- {line[1:].strip()}"  # Prefix line with "-"
                diff_text.insert(tk.END, f"{labeled_line}\n", "removal")
                log_content += f"{labeled_line}\n"
            elif not line.startswith(('+', '-')):
                diff_text.insert(tk.END, f"{line}\n")
                log_content += f"{line}\n"

    # Disable editing of the text widget
    diff_text.config(state=tk.DISABLED)

    # Save log function
    def save_log():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(log_content)
            messagebox.showinfo("Saved", "Log saved successfully.")

    # Save button
    save_button = tk.Button(diff_window, text="Save Log", command=save_log)
    save_button.pack(pady=5)


def summarize_differences(comparisons, show_additions, show_removals, log_widget):
    """Summarize the differences found and open the display window."""
    log_message(log_widget, "Displaying differences...")
    show_differences(comparisons, show_additions, show_removals)

def compare_files_in_folder(folder_path, extension, show_additions, show_removals, log_widget):
    """Find files with specified extension in the folder and compare them."""
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Selected path is not a valid directory.")
        log_message(log_widget, "Invalid directory selected.")
        return
    
    # Get all files with the specified extension in the folder
    script_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(extension)]
    log_message(log_widget, f"Found {len(script_files)} {extension} files in the folder.")

    if len(script_files) < 2:
        messagebox.showinfo("Result", f"Need at least two {extension} files to compare.")
        log_message(log_widget, "Insufficient files for comparison. At least two files are required.")
        return

    # Load the scripts
    script_contents = load_scripts(script_files, log_widget)
    
    # Compare the scripts
    comparisons = compare_scripts(script_contents, show_additions, show_removals, log_widget)
    
    # Summarize the differences
    summarize_differences(comparisons, show_additions, show_removals, log_widget)

def select_folder(extension, show_additions, show_removals, log_widget):
    """Open a folder selection dialog and start the comparison."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        log_message(log_widget, f"Selected folder: {folder_path}")
        compare_files_in_folder(folder_path, extension, show_additions, show_removals, log_widget)

def toggle_checkboxes(additions_var, removals_var, both_var):
    """Toggle checkboxes based on selection logic."""
    if both_var.get():
        additions_var.set(True)
        removals_var.set(True)

def open_log_window():
    """Create a new window to display the live log output."""
    log_window = tk.Toplevel()
    log_window.title("Live Log Output")

    log_widget = tk.Text(log_window, width=60, height=20, state=tk.DISABLED, wrap=tk.WORD)
    log_widget.pack(padx=10, pady=10)

    return log_widget

def create_gui():
    """Create a GUI for folder selection with options for file extension and logging."""
    root = tk.Tk()
    root.title("Python Script Comparator Utility v0.1.0")

    label = tk.Label(root, text="Select a folder containing scripts:")
    label.pack(pady=10)

    # Dropdown for file extension selection
    extension_var = tk.StringVar(value=".py")
    extension_menu = ttk.Combobox(root, textvariable=extension_var, values=[".py", ".txt", ".md", ".html", ".js"])
    extension_menu.pack(pady=5)

    # Checkboxes for addition and removal options
    additions_var = tk.BooleanVar(value=True)
    removals_var = tk.BooleanVar(value=True)
    both_var = tk.BooleanVar(value=True)

    additions_check = tk.Checkbutton(root, text="Show Additions", variable=additions_var, 
                                     command=lambda: toggle_checkboxes(additions_var, removals_var, both_var))
    removals_check = tk.Checkbutton(root, text="Show Removals", variable=removals_var,
                                    command=lambda: toggle_checkboxes(additions_var, removals_var, both_var))
    both_check = tk.Checkbutton(root, text="Show Both", variable=both_var,
                                command=lambda: toggle_checkboxes(additions_var, removals_var, both_var))

    both_check.pack(anchor="w")
    additions_check.pack(anchor="w")
    removals_check.pack(anchor="w")

    # Log widget that is opened in a new window when "Show Output" is pressed
    log_widget = None
    def show_log_output():
        nonlocal log_widget
        if not log_widget or not log_widget.winfo_exists():
            log_widget = open_log_window()

    # Folder selection button
    select_button = tk.Button(root, text="Select Folder", command=lambda: select_folder(extension_var.get(), additions_var.get(), removals_var.get(), log_widget))
    select_button.pack(pady=20)

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

    # Show Output button to open log window
    show_output_button = tk.Button(root, text="Show Output", command=show_log_output)
    show_output_button.pack(pady=10)

    root.geometry("400x500")
    root.mainloop()

if __name__ == "__main__":
    create_gui()
