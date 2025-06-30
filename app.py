# Notepad-like Text Editor Application

import sys
import os
from tkinter import *
from tkinter import filedialog, messagebox

# Main window setup
root = Tk()
root.title("Untitled - Notepad")
root.geometry("800x600")

# Add a Text widget with scrollbars
text = Text(root, undo=True, wrap="word")
scroll = Scrollbar(root, command=text.yview)
text.configure(yscrollcommand=scroll.set)
text.pack(side=LEFT, fill=BOTH, expand=YES)
scroll.pack(side=RIGHT, fill=Y)

current_file = None

def new_file():
    global current_file
    if text.edit_modified():
        if not maybe_save():
            return
    text.delete("1.0", END)
    root.title("Untitled - Notepad")
    current_file = None

def open_file():
    global current_file
    if text.edit_modified():
        if not maybe_save():
            return
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            text.delete("1.0", END)
            text.insert("1.0", content)
        current_file = file_path
        root.title(f"{os.path.basename(file_path)} - Notepad")
        text.edit_modified(False)

def save_file():
    global current_file
    if current_file:
        with open(current_file, "w", encoding="utf-8") as file:
            file.write(text.get("1.0", END).rstrip())
        root.title(f"{os.path.basename(current_file)} - Notepad")
        text.edit_modified(False)
    else:
        save_as()

def save_as():
    global current_file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text.get("1.0", END).rstrip())
        current_file = file_path
        root.title(f"{os.path.basename(file_path)} - Notepad")
        text.edit_modified(False)

def exit_app():
    if text.edit_modified():
        if not maybe_save():
            return
    root.destroy()

def maybe_save():
    if messagebox.askyesnocancel("Notepad", "Do you want to save changes?"):
        save_file()
        return True
    elif messagebox.askyesnocancel("Notepad", "Do you want to save changes?") is None:
        return False
    return True

def about():
    messagebox.showinfo("About Notepad", "A simple Notepad clone in Python.")

# Menu bar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", accelerator="Ctrl+N", command=new_file)
filemenu.add_command(label="Open...", accelerator="Ctrl+O", command=open_file)
filemenu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
filemenu.add_command(label="Save As...", command=save_as)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About Notepad", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

# Keyboard shortcuts
root.bind("<Control-n>", lambda e: new_file())
root.bind("<Control-o>", lambda e: open_file())
root.bind("<Control-s>", lambda e: save_file())
root.protocol("WM_DELETE_WINDOW", exit_app)

# Main Start Loop
root.mainloop()

