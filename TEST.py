import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from tkinter import ttk
import JSON
import SHARED_STATE
import ExtensionRunner
import subprocess
from datetime import datetime
import re

# Global variable to store file path
TreeToggled = False
Info = JSON.JsonGetInfo("Info.json")
ThemeMode = Info["THEME"]
file_path = Info["STD-Path"]
SystemThemeMode = None
selected_button = 0
delete_selected_button = 0
separatorColor = "#FFFFFF"
BINARY_FILE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.ico', '.svg', '.webp', '.heic', 
    '.psd', '.xcf',
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.aiff', '.alac', '.midi', '.kar',
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp', '.m2ts', '.mts', '.rm', '.vob',
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.dmg', 
    '.tar.gz', '.tgz', '.tar.bz2', '.tar.xz', '.lzma',
    '.exe', '.dll', '.bin', '.msi', '.bat', '.sh', '.app', '.deb', '.rpm', 
    '.cmd', '.run',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp', 
    '.pages', '.numbers', '.key',
    '.db', '.sqlite', '.mdb', '.accdb', 
    '.bak', '.dbf', '.ndf',
    '.sys', '.dat', '.cfg', 
    '.drv', '.inf',
    '.ttf', '.otf', '.woff', '.woff2', '.eot', 
    '.pfb', '.pfm',
    '.iso', '.img', '.vhd', '.vmdk', 
    '.bin', '.cue', '.nrg',
    '.stl', '.obj', '.fbx', '.3ds', '.dae', 
    '.blend', '.skp',
    '.dwg', '.dxf', '.step', '.iges',
    '.shp', '.kml', '.kmz',
    '.bak', '.bkp', '.backup',
    '.vdi', '.vhdx', '.ova', '.ovf',
    '.so', '.class', '.jar', '.o', '.a', '.lib'
}

Tab1_Path = file_path
Tab1_Content = ""
Tab2_Path = file_path
Tab2_Content = ""
Tab3_Path = file_path
Tab3_Content = ""
Tab4_Path = file_path
Tab4_Content = ""

if file_path == "":
    file_path = "Untitled.txt"
if file_path != "Untitled.txt":
    with open(file_path, 'r') as file:
            text = file.read()
    Tab1_Content = Tab2_Content = Tab3_Content = Tab4_Content = text

def toggle_tree(event):
    global TreeToggled
    TreeToggled = not TreeToggled
    print(TreeToggled)

def new_file():
    if messagebox.askokcancel("New", "Do you want to save changes?"):
        save_file()
    text_area.delete(1.0, tk.END)

def open_file():
    global file_path, Tab3_Path, Tab3_Content, Tab4_Path, Tab4_Content, Tab1_Path, Tab1_Content, Tab2_Path, Tab2_Content
    file_path = filedialog.askopenfilename()
    if file_path not in BINARY_FILE_EXTENSIONS:
        with open(file_path, 'r') as file:
            text = file.read()
        tab1val = text_tabs1.get()
        tab2val = text_tabs2.get()
        if tab1val == None:
            if tab2val == 3:
                Tab3_Path = file_path
                Tab3_Content = text
            else:
                Tab4_Path = file_path
                Tab4_Content = text
        else:
            if tab1val == 1:
                Tab1_Path = file_path
                Tab1_Content = text
            else:
                Tab2_Path = file_path
                Tab2_Content = text
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, text)
    Path_label.configure(text=file_path)

# Function to save the current file
def save_file():
    global file_path, Tab4_Path, Tab3_Path, Tab2_Path, Tab1_Path
    tab1val = text_tabs1.get()
    tab2val = text_tabs2.get()
    if tab1val == 1:
        file_path = Tab1_Path
    elif tab1val == 2:
        file_path = Tab2_Path
    elif tab2val == 3:
        file_path = Tab3_Path
    elif tab2val == 4:
        file_path = Tab4_Path
        
    if file_path == "" or file_path == "Untitled.txt":
        save_file_as()
    else:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, ctk.END))
    Path_label.configure(text=file_path)

# Function to save the file with a new name
def save_file_as():
    global file_path, Tab1_Path, Tab2_Path, Tab3_Path, Tab4_Path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text Files", "*.txt"), 
                                                        ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, ctk.END))
        file_path = file_path
    else:
        file_path = Info["STD-Path"]
    tab1val = text_tabs1.get()
    tab2val = text_tabs2.get()
    if tab1val == 1:
        Tab1_Path = file_path
    elif tab1val == 2:
        Tab2_Path = file_path
    elif tab2val == 3:
        Tab3_Path = file_path
    elif tab2val == 4:
        Tab4_Path = file_path
    Path_label.configure(text=file_path)

# Function to handle Ctrl+S for saving the file
def save_file_shortcut(event=None):
    save_file()

# Function to increase the font size
def increase_font(event):
    font_family, current_font_size = text_area.cget("font")
    new_font_size = current_font_size + 1
    new_font = (font_family, new_font_size)
    text_area.configure(font=new_font)

# Function to decrease the font size
def decrease_font(event):
    font_family, current_font_size = text_area.cget("font")
    if current_font_size > 5:
        new_font_size = current_font_size - 1
        new_font = (font_family, new_font_size)
        text_area.configure(font=new_font)
        
def get_cursor_position(text_widget):
    cursor_pos = text_widget.index(tk.INSERT)
    line, column = cursor_pos.split('.')
    return int(line), int(column)

def update_label_text(text_widget):
    cursor_line, cursor_column  = get_cursor_position(text_widget)
    LineCount_label.configure(text=f"  Ln: {cursor_line}, LnCol: {cursor_column}")
    # Schedule the next update after 100 milliseconds (adjust as needed)
    root.after(100, update_label_text, text_widget)

def on_cursor_move(event, text_widget):
    update_label_text(text_widget)

def modifyTheme(mode):
    """
    * Its Made For The Items That Are Visible In The Main App
    """
    global ThemeMode
    global separatorColor, time_label, BACKGROUND, text_tabs1, text_tabs2
    OriginalTheme = None
    if separatorColor == "#303a41": OriginalTheme = "Nitro"
    if mode == "System":
        mode = SystemThemeMode
    if mode == "Dark":
        ThemeMode = "Dark"
        separatorColor = "#414141"
        if OriginalTheme == "Nitro":
            messagebox.showinfo("Restart App", "Nitro Is A Custom Theme That Is Harder To Change Directly.\nRestart The App For The Changes To Take Effect!")
        
    elif mode == "Nitro":
        ThemeMode = "Nitro"
        separatorColor = "#303a41"
        messagebox.showinfo("Restart App", "Nitro Is A Custom Theme That Is Harder To Change Directly.\nRestart The App For The Changes To Take Effect!")
    else:
        ThemeMode = "Light"
        separatorColor = "#FFFFFF"
        if OriginalTheme == "Nitro":
            messagebox.showinfo("Restart App", "Nitro Is A Custom Theme That Is Harder To Change Directly.\nRestart The App For The Changes To Take Effect!")
    if mode != "Nitro":
        ctk.set_appearance_mode(mode)
    separator1.configure(bg=separatorColor)
    separator2.configure(bg=separatorColor)

    if ThemeMode == "Light": 
        btn_Settings.configure(fg_color="#C0C0C0", hover_color="#F5F5F5")
        btn_File.configure(fg_color="#C0C0C0", hover_color="#F5F5F5")
        btn_SearchExtensions.configure(fg_color="#C0C0C0", hover_color="#F5F5F5")
        btn_TaskNotes.configure(fg_color="#C0C0C0", hover_color="#F5F5F5")
        b_ChangeTheme.configure(fg_color="#C0C0C0", hover_color="#F5F5F5")
        b_ChangeDefaultPath.configure(fg_color="#C0C0C0", hover_color="#F5F5F5")
        btn_InstalledExtensions.configure(fg_color="#C0C0C0", hover_color="#F5F5F5")
        text_tabs1.configure(selected_color="#D2D0CB", selected_hover_color="#F5F5F5", fg_color="#C0C0C0", unselected_color="#C0C0C0")
        text_tabs2.configure(selected_color="#D2D0CB", selected_hover_color="#F5F5F5", fg_color="#C0C0C0", unselected_color="#C0C0C0")
        BACKGROUND.configure(bg="#E5E4E2")
    elif ThemeMode == "Nitro":
        btn_Settings.configure(fg_color="#29343b", hover_color="#283035")
        btn_File.configure(fg_color="#29343b", hover_color="#283035")
        btn_SearchExtensions.configure(fg_color="#29343b", hover_color="#283035")
        btn_TaskNotes.configure(fg_color="#29343b", hover_color="#283035")
        btn_InstalledExtensions.configure(fg_color="#29343b", hover_color="#283035")
        b_ChangeTheme.configure(fg_color="#29343b", hover_color="#283035")
        b_ChangeDefaultPath.configure(fg_color="#29343b", hover_color="#283035")
    else: 
        time_label.configure(background="#1B1B1B", fg="#C0C0C0")
        btn_Settings.configure(fg_color="#353839", hover_color="#2A3439")
        btn_File.configure(fg_color="#353839", hover_color="#2A3439")
        btn_SearchExtensions.configure(fg_color="#353839", hover_color="#2A3439")
        btn_InstalledExtensions.configure(fg_color="#353839", hover_color="#2A3439")
        btn_TaskNotes.configure(fg_color="#353839", hover_color="#2A3439")
        b_ChangeTheme.configure(fg_color="#353839", hover_color="#2A3439")
        b_ChangeDefaultPath.configure(fg_color="#353839", hover_color="#2A3439")
        text_tabs1.configure(selected_color="#424141", selected_hover_color="#353839", fg_color="#4C4C4C", unselected_color="#4C4C4C")
        text_tabs2.configure(selected_color="#424141", selected_hover_color="#353839", fg_color="#4C4C4C", unselected_color="#4C4C4C")
        BACKGROUND.configure(bg="#1B1B1B")
    child.destroy()
    Settingschild.destroy()
    Extensionschild.destroy()
    FileOptionschild.destroy()
    
def ChangeTheme():
    global child
    child = ctk.CTkToplevel(master=root)
    child.title("Change Theme")
    child.geometry("180x200")
    child.wm_iconbitmap(default="Img\\Nitrogen Window Icon.ico")
    child.transient(Settingschild)
    child.resizable(False, False)
    BACKGROUND = tk.Frame(child, bg="#1B1B1B")
    BACKGROUND.pack(expand=True, fill="both")
    b_System = ctk.CTkButton(BACKGROUND, command=lambda: modifyTheme("System"), text="Change To 'System'")
    b_Dark = ctk.CTkButton(BACKGROUND, command=lambda: modifyTheme("Dark"), text="Change To 'Dark'")
    b_Light = ctk.CTkButton(BACKGROUND, command=lambda: modifyTheme("Light"), text="Change To 'Light'")
    b_Nitro = ctk.CTkButton(BACKGROUND, command=lambda: modifyTheme("Nitro"), text="Change To 'Nitro'")
    b_System.pack(pady=10)
    b_Dark.pack(pady=10)
    b_Light.pack(pady=10)
    b_Nitro.pack(pady=10)
    if ThemeMode == "Light": 
        b_System.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        b_Dark.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        b_Light.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        b_Nitro.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        BACKGROUND.configure(bg="#E5E4E2")
    elif ThemeMode == "Nitro": 
        b_System.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        b_Dark.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        b_Light.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        b_Nitro.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        BACKGROUND.configure(bg="#1b252c")
    else:
        b_System.configure(fg_color="#353839", hover_color="#2A3439")
        b_Dark.configure(fg_color="#353839", hover_color="#2A3439")
        b_Light.configure(fg_color="#353839", hover_color="#2A3439")
        b_Nitro.configure(fg_color="#353839", hover_color="#2A3439")
        BACKGROUND.configure(bg="#1B1B1B")

def insert_tab(event):
    text_area.insert(tk.INSERT, "    ")  # Insert 4 spaces
    return "break"

def OpenSettings():
    global Settingschild, time_label, BACKGROUND, b_ChangeTheme, b_ChangeDefaultPath
    Settingschild = ctk.CTkToplevel(master=root)
    Settingschild.title("Settings")
    Settingschild.geometry("1000x600")
    Settingschild.transient(root)
    BACKGROUND = tk.Frame(Settingschild, bg="#1B1B1B")
    BACKGROUND.pack(expand=True, fill="both")
    # Create a frame to hold the labels
    label_frame = tk.Frame(BACKGROUND, bg="#1B1B1B")
    label_frame.pack(pady=20, fill='x')

    # Create the labels
    time_label = tk.Label(label_frame, text="", font=("Helvetica", 48), bg="#1B1B1B", fg="white")
    time_label.pack(side="right", padx=20)

    Settings_image_label = ctk.CTkLabel(label_frame, text='', image=PngIcon_Settings_Big)
    Settings_image_label.pack(side="left", padx=10)

    Settings_label = tk.Label(label_frame, text="Settings", font=("Helvetica", 48), bg="#1B1B1B", fg="white")
    Settings_label.pack(side="left", padx=(0,20), pady=5)
    
    b_ChangeTheme = ctk.CTkButton(BACKGROUND, command=ChangeTheme, text="Change Theme       ", font=("Helvetica", 17), image=PngIcon_PaintBrush, height=15)
    b_ChangeTheme.pack(anchor='nw', padx=25, pady=(0,25))
    b_ChangeDefaultPath = ctk.CTkButton(BACKGROUND, command=select_file_path, text="Change Default Path", font=("Helvetica", 17), image=PngIcon_ChangePath, height=30)
    b_ChangeDefaultPath.pack(anchor='nw', padx=25, pady=(0,25))
    b_ResetDefaultPath = ctk.CTkButton(BACKGROUND, command=reset_file_path, text="Reset Default Path   ", font=("Helvetica", 17), image=PngIcon_ChangePath, height=30)
    b_ResetDefaultPath.pack(anchor='nw', padx=25, pady=(0,25))
    if ThemeMode == "Light": 
        b_ChangeTheme.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        b_ChangeDefaultPath.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        b_ResetDefaultPath.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        time_label.configure(background="#E5E4E2", fg="#C0C0C0")
        Settings_label.configure(background="#C0C0C0", fg="#E5E4E2")
        label_frame.configure(bg="#C0C0C0")
        text_tabs1.configure(selected_color="#D2D0CB", selected_hover_color="#F5F5F5", fg_color="#C0C0C0", unselected_color="#C0C0C0")
        text_tabs2.configure(selected_color="#D2D0CB", selected_hover_color="#F5F5F5", fg_color="#C0C0C0", unselected_color="#C0C0C0")
        BACKGROUND.configure(bg="#E5E4E2")
    elif ThemeMode == "Nitro": 
        b_ChangeTheme.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        b_ChangeDefaultPath.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        b_ResetDefaultPath.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        time_label.configure(background="#1b252c", fg="#9faeb9")
        Settings_label.configure(background="#313c43", fg="#9faeb9")
        label_frame.configure(bg="#313c43")
        text_tabs1.configure(selected_color="#303a41", selected_hover_color="#212f39", fg_color="#364148", unselected_color="#364148", unselected_hover_color="#29343b", text_color="#9faeb9")
        text_tabs2.configure(selected_color="#303a41", selected_hover_color="#212f39", fg_color="#364148", unselected_color="#364148", unselected_hover_color="#29343b", text_color="#9faeb9")
        BACKGROUND.configure(bg="#1b252c")
    else: 
        b_ChangeTheme.configure(fg_color="#353839", hover_color="#2A3439")
        b_ChangeDefaultPath.configure(fg_color="#353839", hover_color="#2A3439")
        b_ResetDefaultPath.configure(fg_color="#353839", hover_color="#2A3439")
        time_label.configure(background="#1B1B1B", fg="#C0C0C0")
        Settings_label.configure(background="#353839", fg="#C0C0C0")
        label_frame.configure(bg="#353839")
        text_tabs1.configure(selected_color="#424141", selected_hover_color="#353839", fg_color="#4C4C4C", unselected_color="#4C4C4C")
        text_tabs2.configure(selected_color="#424141", selected_hover_color="#353839", fg_color="#4C4C4C", unselected_color="#4C4C4C")
        BACKGROUND.configure(bg="#1B1B1B")
    update_time()
    
def OpenExtensions():
    global Extensionschild, time_label, BACKGROUND
    Extensionschild = ctk.CTkToplevel(master=root)
    Extensionschild.title("Search Extensions")
    Extensionschild.geometry("1000x600")
    Extensionschild.transient(root)
    BACKGROUND = tk.Frame(Extensionschild, bg="#1B1B1B")
    BACKGROUND.pack(expand=True, fill="both")
    time_label = tk.Label(BACKGROUND, text="", font=("Helvetica", 48), bg="#1B1B1B", fg="white")
    time_label.pack(padx=20, pady=20)
    update_time()
    
def OpenTerminal():
    subprocess.Popen('powershell.exe', cwd='C:\\')
    
def update_time():
    current_time = datetime.now().strftime('%H:%M:%S')
    time_label.configure(text=current_time)
    root.after(1000, update_time)  # Update time every second (1000 milliseconds)
    
def select_file_path() -> str:
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path not in BINARY_FILE_EXTENSIONS:
        print("[+] Chose A File Path")
        Info["STD-Path"] = file_path
        messagebox.showinfo("Restart App", "Restart The App For The Changes To Take Effect!")
    else:
        print("[-] Could Not Choose A File Path")
        
def reset_file_path():
    global file_path
    if file_path != "Untitled.txt":
        file_path = "Untitled.txt"
        Info["STD-Path"] = file_path
        messagebox.showinfo("Restart App", "Restart The App For The Changes To Take Effect!")
    
def OpenFileOptions():
    global FileOptionschild, time_label, BACKGROUND, FileOptions_label
    FileOptionschild = ctk.CTkToplevel(master=root)
    FileOptionschild.title("File Options")
    FileOptionschild.geometry("1000x600")
    FileOptionschild.configure()
    FileOptionschild.transient(root)
    BACKGROUND = tk.Frame(FileOptionschild, bg="#1B1B1B")
    BACKGROUND.pack(expand=True, fill="both")
    label_frame = tk.Frame(BACKGROUND, bg="#1B1B1B")
    label_frame.pack(pady=20, fill='x')
    time_label = tk.Label(label_frame, text="", font=("Helvetica", 48), bg="#1B1B1B", fg="white")
    time_label.pack(side="right", padx=20)
    FileOptions_image_label = ctk.CTkLabel(label_frame, text='', image=PngIcon_File_Big)
    FileOptions_image_label.pack(side="left", padx=10)
    FileOptions_label = tk.Label(label_frame, text="File Options", font=("Helvetica", 48), bg="#1B1B1B", fg="white")
    FileOptions_label.pack(side="left", padx=(0,20), pady=5)
    b_NewFile = ctk.CTkButton(BACKGROUND, command=new_file, text="New Text File  ", image=PngIcon_CreateNewFile, font=("Helvetica", 17), compound=tk.LEFT)
    b_OpenFile = ctk.CTkButton(BACKGROUND, command=open_file, text="Open File       ", image=PngIcon_OpenFile, font=("Helvetica", 17), compound=tk.LEFT, height=15)
    b_SaveFile = ctk.CTkButton(BACKGROUND, command=save_file, text="Save File        ", image=PngIcon_SaveFile, font=("Helvetica", 17), compound=tk.LEFT, height=15)
    b_SaveFileAs = ctk.CTkButton(BACKGROUND, command=save_file, text="Save File As   ", image=PngIcon_SaveFile, font=("Helvetica", 17), compound=tk.LEFT, height=15)
    b_OpenTerminal = ctk.CTkButton(BACKGROUND, command=OpenTerminal, text="Open Terminal", image=PngIcon_OpenTerminal, font=("Helvetica", 17), compound=tk.LEFT, height=15)
    b_NewFile.pack(anchor='nw', padx=25, pady=(0,25))
    b_OpenFile.pack(anchor='nw', padx=25, pady=(0,25))
    b_SaveFile.pack(anchor='nw', padx=25, pady=(0,25))
    b_SaveFileAs.pack(anchor='nw', padx=25, pady=(0,25))
    b_OpenTerminal.pack(anchor='nw', padx=25, pady=(0,25))
    if ThemeMode == "Light": 
        b_NewFile.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        b_OpenFile.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        b_SaveFile.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        b_SaveFileAs.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        b_OpenTerminal.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        time_label.configure(background="#E5E4E2", fg="#C0C0C0")
        FileOptions_label.configure(background="#C0C0C0", fg="#E5E4E2")
        label_frame.configure(bg="#C0C0C0")
        text_tabs1.configure(selected_color="#D2D0CB", selected_hover_color="#F5F5F5", fg_color="#C0C0C0", unselected_color="#C0C0C0")
        text_tabs2.configure(selected_color="#D2D0CB", selected_hover_color="#F5F5F5", fg_color="#C0C0C0", unselected_color="#C0C0C0")
        BACKGROUND.configure(bg="#E5E4E2")
    elif ThemeMode == "Nitro": 
        b_NewFile.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        b_OpenFile.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        b_SaveFile.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        b_SaveFileAs.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        b_OpenTerminal.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        time_label.configure(background="#1b252c", fg="#9faeb9")
        FileOptions_label.configure(background="#313c43", fg="#9faeb9")
        label_frame.configure(bg="#313c43")
        text_tabs1.configure(selected_color="#303a41", selected_hover_color="#212f39", fg_color="#364148", unselected_color="#364148", unselected_hover_color="#29343b", text_color="#9faeb9")
        text_tabs2.configure(selected_color="#303a41", selected_hover_color="#212f39", fg_color="#364148", unselected_color="#364148", unselected_hover_color="#29343b", text_color="#9faeb9")
        BACKGROUND.configure(bg="#1b252c")
    else: 
        b_NewFile.configure(fg_color="#353839", hover_color="#2A3439")
        b_OpenFile.configure(fg_color="#353839", hover_color="#2A3439")
        b_SaveFile.configure(fg_color="#353839", hover_color="#2A3439")
        b_SaveFileAs.configure(fg_color="#353839", hover_color="#2A3439")
        b_OpenTerminal.configure(fg_color="#353839", hover_color="#2A3439")
        time_label.configure(background="#1B1B1B", fg="#C0C0C0")
        FileOptions_label.configure(background="#353839", fg="#C0C0C0")
        label_frame.configure(bg="#353839")
        text_tabs1.configure(selected_color="#424141", selected_hover_color="#353839", fg_color="#4C4C4C", unselected_color="#4C4C4C")
        text_tabs2.configure(selected_color="#424141", selected_hover_color="#353839", fg_color="#4C4C4C", unselected_color="#4C4C4C")
        BACKGROUND.configure(bg="#1B1B1B")
    update_time()

def delete_word(event):
    widget = event.widget
    if isinstance(widget, tk.Entry):
        cursor_pos = widget.index(tk.INSERT)
        text = widget.get()
        if cursor_pos == 0:
            return "break"
        end = cursor_pos
        start = cursor_pos - 1
        while start > 0 and text[start - 1] not in (' ', '.', '/', '\\'):
            start -= 1
        widget.delete(start, end)
    elif isinstance(widget, tk.Text):
        cursor_pos = widget.index(tk.INSERT)
        if cursor_pos == '1.0':
            return "break"
        
        line_start = widget.index(f"{cursor_pos} linestart")
        line_end = widget.index(f"{cursor_pos} lineend")
        line_text = widget.get(line_start, line_end).strip()

        if line_text.count(' ') == 0 and line_text.count('.') == 0:
            # If the line contains only one word, delete the whole line
            widget.delete(line_start, f"{line_start} lineend +1c")
        else:
            end = cursor_pos
            start = widget.index(f"{cursor_pos} -1c")
            while start != '1.0' and widget.get(f"{start} -1c", start) not in (' ', '.', '/', '\\'):
                start = widget.index(f"{start} -1c")
            if widget.get(start, end).strip() == line_text:
                # If the cursor is at the start of the line
                widget.delete(line_start, f"{line_start} lineend +1c")
            else:
                widget.delete(start, end)
    return "break"

def ChangeTabs(Tab):
    global Tab1_Content, Tab2_Content, Tab3_Content, Tab4_Content
    print(f"Changing to Tab {Tab}")
    if Tab == 1 or Tab == 2:    # * Set 1
        text_tabs2.set(None)
        if Tab == 1:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, Tab1_Content)
            Path_label.configure(text=Tab1_Path)
            text_tabs1.set(1)
        else:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, Tab2_Content)
            Path_label.configure(text=Tab2_Path)
            text_tabs1.set(2)
    else:                       # * Set 2  
        text_tabs1.set(None)
        if Tab == 3:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, Tab3_Content)
            Path_label.configure(text=Tab3_Path)
            text_tabs2.set(3)
        else:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, Tab4_Content)
            Path_label.configure(text=Tab4_Path)
            text_tabs2.set(4)
    if ThemeMode == "Light": 
        text_tabs1.configure(selected_color="#D2D0CB", selected_hover_color="#F5F5F5", fg_color="#C0C0C0", unselected_color="#C0C0C0")
        text_tabs2.configure(selected_color="#D2D0CB", selected_hover_color="#F5F5F5", fg_color="#C0C0C0", unselected_color="#C0C0C0")
    elif ThemeMode == "Nitro":
        text_tabs1.configure(selected_color="#303a41", selected_hover_color="#212f39", fg_color="#364148", unselected_color="#364148", unselected_hover_color="#29343b", text_color="#9faeb9")
        text_tabs2.configure(selected_color="#303a41", selected_hover_color="#212f39", fg_color="#364148", unselected_color="#364148", unselected_hover_color="#29343b", text_color="#9faeb9")
    else:
        text_tabs1.configure(selected_color="#424141", selected_hover_color="#353839", fg_color="#4C4C4C", unselected_color="#4C4C4C")
        text_tabs2.configure(selected_color="#424141", selected_hover_color="#353839", fg_color="#4C4C4C", unselected_color="#4C4C4C")

def modify_text(event):
    global Tab1_Content, Tab2_Content, Tab3_Content, Tab4_Content
    tab1val = text_tabs1.get()
    tab2val = text_tabs2.get()
    
    if tab1val == 1:
        Tab1_Content = text_area.get(1.0, tk.END).rstrip('\n')
    elif tab1val == 2:
        Tab2_Content = text_area.get(1.0, tk.END).rstrip('\n')
    elif tab2val == 3:
        Tab3_Content = text_area.get(1.0, tk.END).rstrip('\n')
    elif tab2val == 4:
        Tab4_Content = text_area.get(1.0, tk.END).rstrip('\n')
    else:
        print("No valid tab selected.")
        
def toggle_fullscreen(event=None):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))
    if ThemeMode == "light":
        ctk.set_appearance_mode("Dark")
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Light")
        ctk.set_appearance_mode("Dark")

# Function to exit fullscreen mode
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)
    if ThemeMode == "light":
        ctk.set_appearance_mode("Dark")
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Light")
        ctk.set_appearance_mode("Dark")
        
def AddTaskToNotes(): # ? Made For When Entering A New Task
    if Info["NoteTasks"] < 9 : Info["NoteTasks"] += 1
    if Info["NoteTasks"] == 1:
        Task1Check.configure(text=TaskName_entry.get(), state="normal")
        Info["Task1Text"] = TaskName_entry.get()
    elif Info["NoteTasks"] == 2:
        Task2Check.configure(text=TaskName_entry.get(), state="normal")
        Info["Task2Text"] = TaskName_entry.get()
    elif Info["NoteTasks"] == 3:
        Task3Check.configure(text=TaskName_entry.get(), state="normal")
        Info["Task3Text"] = TaskName_entry.get()
    elif Info["NoteTasks"] == 4:
        Task4Check.configure(text=TaskName_entry.get(), state="normal")
        Info["Task4Text"] = TaskName_entry.get()
    elif Info["NoteTasks"] == 5:
        Task5Check.configure(text=TaskName_entry.get(), state="normal")
        Info["Task5Text"] = TaskName_entry.get()
    elif Info["NoteTasks"] == 6:
        Task6Check.configure(text=TaskName_entry.get(), state="normal")
        Info["Task6Text"] = TaskName_entry.get()
    elif Info["NoteTasks"] == 7:
        Task7Check.configure(text=TaskName_entry.get(), state="normal")
        Info["Task7Text"] = TaskName_entry.get()
    elif Info["NoteTasks"] == 8:
        Task8Check.configure(text=TaskName_entry.get(), state="normal")
        Info["Task8Text"] = TaskName_entry.get()
    elif Info["NoteTasks"] == 9:
        Task9Check.configure(text=TaskName_entry.get(), state="normal")
        Info["Task9Text"] = TaskName_entry.get()
    AddTaskChild.destroy()
        
def AddTask():
    global BACKGROUND, TaskName_entry, AddTaskChild
    AddTaskChild = ctk.CTkToplevel(TasksChild)
    AddTaskChild.title("Add Task Note")
    AddTaskChild.geometry("500x140")
    AddTaskChild.transient(TasksChild)
    AddTaskChild.resizable(False, False)
    BACKGROUND = tk.Frame(AddTaskChild, bg="#1B1B1B")
    BACKGROUND.pack(expand=True, fill="both")
    if Info["NoteTasks"] < 9:
        TaskName_entry = ctk.CTkEntry(BACKGROUND, placeholder_text="                                         Enter Task Name", width=350)
        TaskName_entry.pack(padx=30, pady=20)
        b_AddTaskNote = ctk.CTkButton(BACKGROUND, text="Add Task Note", command=AddTaskToNotes)
        b_AddTaskNote.pack(padx=30, pady=20)
    if ThemeMode == "Light":
        BACKGROUND.configure(bg="#E5E4E2")
        b_AddTaskNote.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
    elif ThemeMode == "Nitro":
        BACKGROUND.configure(bg="#1b252c")
        b_AddTaskNote.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
    else:
        BACKGROUND.configure(bg="#1B1B1B")
        b_AddTaskNote.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        
def TaskCheckBox():
    Info["Task1Checked"] = var1.get() == "1"
    Info["Task2Checked"] = var2.get() == "1"
    Info["Task3Checked"] = var3.get() == "1"
    Info["Task4Checked"] = var4.get() == "1"
    Info["Task5Checked"] = var5.get() == "1"
    Info["Task6Checked"] = var6.get() == "1"
    Info["Task7Checked"] = var7.get() == "1"
    Info["Task8Checked"] = var8.get() == "1"
    Info["Task9Checked"] = var9.get() == "1"
    
def ModifyTaskButton(button: int):
    global selected_button
    selected_button = button
    if button == 1: 
        Button1.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 2: 
        Button2.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button1.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button1.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button1.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 3: 
        Button3.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 4: 
        Button4.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 5: 
        Button5.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 6: 
        Button6.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 7: 
        Button7.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 8: 
        Button8.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 9: 
        Button9.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")

def Delete_TaskButton(button: int):
    global delete_selected_button
    delete_selected_button = button
    if button == 1: 
        Button1.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 2: 
        Button2.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button1.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button1.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button1.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 3: 
        Button3.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 4: 
        Button4.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 5: 
        Button5.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 6: 
        Button6.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 7: 
        Button7.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 8: 
        Button8.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
            Button9.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
            Button9.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            Button9.configure(fg_color="#C0C0C0")
    if button == 9: 
        Button9.configure(fg_color="#91A3B0")
        if ThemeMode == "Dark":
            Button2.configure(fg_color="#353839")
            Button3.configure(fg_color="#353839")
            Button4.configure(fg_color="#353839")
            Button5.configure(fg_color="#353839")
            Button6.configure(fg_color="#353839")
            Button7.configure(fg_color="#353839")
            Button8.configure(fg_color="#353839")
            Button1.configure(fg_color="#353839")
        elif ThemeMode == "Nitro":
            Button2.configure(fg_color="#313c43")
            Button3.configure(fg_color="#313c43")
            Button4.configure(fg_color="#313c43")
            Button5.configure(fg_color="#313c43")
            Button6.configure(fg_color="#313c43")
            Button7.configure(fg_color="#313c43")
            Button8.configure(fg_color="#313c43")
            Button1.configure(fg_color="#313c43")
        else:
            Button2.configure(fg_color="#C0C0C0")
            Button3.configure(fg_color="#C0C0C0")
            Button4.configure(fg_color="#C0C0C0")
            Button5.configure(fg_color="#C0C0C0")
            Button6.configure(fg_color="#C0C0C0")
            Button7.configure(fg_color="#C0C0C0")
            Button8.configure(fg_color="#C0C0C0")
            Button1.configure(fg_color="#C0C0C0")
            
def DeleteTaskNote():
    if delete_selected_button in range(1, 10):  # Ensure the button number is within the valid range
        start_task = delete_selected_button
        task_count = 9  # Assuming there are 9 tasks

        for i in range(start_task, task_count):
            next_task_text = Info[f"Task{i+1}Text"]
            next_task_checked = Info[f"Task{i+1}Checked"]
            
            if next_task_text != "...":
                Info[f"Task{i}Text"] = next_task_text
                Info[f"Task{i}Checked"] = next_task_checked
            else:
                Info[f"Task{i}Text"] = "..."
                Info[f"Task{i}Checked"] = False
                break

        # Clear the last task slot
        Info[f"Task{task_count}Text"] = "..."
        Info[f"Task{task_count}Checked"] = False

        Info["NoteTasks"] -= 1
        
    Task1Check.configure(text=Info["Task1Text"])
    Task2Check.configure(text=Info["Task2Text"])
    Task3Check.configure(text=Info["Task3Text"])
    Task4Check.configure(text=Info["Task4Text"])
    Task5Check.configure(text=Info["Task5Text"])
    Task6Check.configure(text=Info["Task6Text"])
    Task7Check.configure(text=Info["Task7Text"])
    Task8Check.configure(text=Info["Task8Text"])
    Task9Check.configure(text=Info["Task9Text"])
    
    if Info["Task1Text"] != "...": 
        Task1Check.configure(state="normal")
    else:
        Task1Check.configure(state="disabled")
    if Info["Task2Text"] != "...": 
        Task2Check.configure(state="normal")
    else:
        Task2Check.configure(state="disabled")
    if Info["Task3Text"] != "...": 
        Task3Check.configure(state="normal")
    else:
        Task3Check.configure(state="disabled")
    if Info["Task4Text"] != "...": 
        Task4Check.configure(state="normal")
    else:
        Task4Check.configure(state="disabled")
    if Info["Task5Text"] != "...": 
        Task5Check.configure(state="normal")
    else:
        Task5Check.configure(state="disabled")
    if Info["Task6Text"] != "...": 
        Task6Check.configure(state="normal")
    else:
        Task6Check.configure(state="disabled")
    if Info["Task7Text"] != "...": 
        Task7Check.configure(state="normal")
    else:
        Task7Check.configure(state="disabled")
    if Info["Task8Text"] != "...": 
        Task8Check.configure(state="normal")
    else:
        Task8Check.configure(state="disabled")
    if Info["Task9Text"] != "...": 
        Task9Check.configure(state="normal")
    else:
        Task9Check.configure(state="disabled")
            
def DeleteTask():
    global DeleteTaskChild, Button1, Button2, Button3, Button4, Button5, Button6, Button7, Button8, Button9
    DeleteTaskChild = ctk.CTkToplevel(TasksChild)
    DeleteTaskChild.title("Delete Task Note")
    DeleteTaskChild.geometry("166x150")
    DeleteTaskChild.transient(TasksChild)
    DeleteTaskChild.resizable(False, False)
    BACKGROUND = tk.Frame(DeleteTaskChild, bg="#1B1B1B")
    BACKGROUND.pack(expand=True, fill="both")
    button_frame = ctk.CTkFrame(BACKGROUND, fg_color="#1B1B1B")
    button_frame.grid(row=1, column=1, pady=(13,5), padx=13)
    Button1 = ctk.CTkButton(button_frame, text=" 1 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=1: Delete_TaskButton(btn))
    Button1.grid(row=1, column=1, padx=2, pady=2)
    Button2 = ctk.CTkButton(button_frame, text=" 2 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=2: Delete_TaskButton(btn))
    Button2.grid(row=1, column=2, padx=2, pady=2)
    Button3 = ctk.CTkButton(button_frame, text=" 3 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=3: Delete_TaskButton(btn))
    Button3.grid(row=1, column=3, padx=2, pady=2)
    Button4 = ctk.CTkButton(button_frame, text=" 4 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=4: Delete_TaskButton(btn))
    Button4.grid(row=2, column=1, padx=2, pady=2)
    Button5 = ctk.CTkButton(button_frame, text=" 5 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=5: Delete_TaskButton(btn))
    Button5.grid(row=2, column=2, padx=2, pady=2)
    Button6 = ctk.CTkButton(button_frame, text=" 6 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=6: Delete_TaskButton(btn))
    Button6.grid(row=2, column=3, padx=2, pady=2)
    Button7 = ctk.CTkButton(button_frame, text=" 7 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=7: Delete_TaskButton(btn))
    Button7.grid(row=3, column=1, padx=2, pady=2)
    Button8 = ctk.CTkButton(button_frame, text=" 8 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=8: Delete_TaskButton(btn))
    Button8.grid(row=3, column=2, padx=2, pady=2)
    Button9 = ctk.CTkButton(button_frame, text=" 9 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=9: Delete_TaskButton(btn))
    Button9.grid(row=3, column=3, padx=2, pady=2)
    b_DeleteTaskNote = ctk.CTkButton(BACKGROUND, text="Delete Task Note", command=DeleteTaskNote)
    b_DeleteTaskNote.grid(row=2, column=1, padx=13)
    
    if ThemeMode == "Light":
        b_DeleteTaskNote.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button1.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button2.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button3.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button4.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button5.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button6.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button7.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button8.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button9.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        button_frame.configure(fg_color="#E5E4E2")
        BACKGROUND.configure(bg="#E5E4E2")
    elif ThemeMode == "Nitro":
        b_DeleteTaskNote.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button1.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button2.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button3.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button4.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button5.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button6.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button7.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button8.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button9.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        button_frame.configure(fg_color="#1b252c")
        BACKGROUND.configure(bg="#1b252c")
    else:
        b_DeleteTaskNote.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button1.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button2.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button3.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button4.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button5.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button6.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button7.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button8.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button9.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        button_frame.configure(fg_color="#1B1B1B")
        BACKGROUND.configure(bg="#1B1B1B")
    
def ModifyTaskNote():
    global selected_button
    if selected_button == 1 and Info["Task1Text"] != "...":
        Task1Check.configure(text=ModifyTaskName_entry.get())
        Info["Task1Text"] = ModifyTaskName_entry.get()
    elif selected_button == 2 and Info["Task2Text"] != "...":
        Task2Check.configure(text=ModifyTaskName_entry.get())
        Info["Task2Text"] = ModifyTaskName_entry.get()
        
    elif selected_button == 3 and Info["Task3Text"] != "...":
        Task3Check.configure(text=ModifyTaskName_entry.get())
        Info["Task3Text"] = ModifyTaskName_entry.get()
        
    elif selected_button == 4 and Info["Task4Text"] != "...":
        Task4Check.configure(text=ModifyTaskName_entry.get())
        Info["Task4Text"] = ModifyTaskName_entry.get()
        
    elif selected_button == 5 and Info["Task5Text"] != "...":
        Task5Check.configure(text=ModifyTaskName_entry.get())
        Info["Task5Text"] = ModifyTaskName_entry.get()
        
    elif selected_button == 6 and Info["Task6Text"] != "...":
        Task6Check.configure(text=ModifyTaskName_entry.get())
        Info["Task6Text"] = ModifyTaskName_entry.get()
        
    elif selected_button == 7 and Info["Task7Text"] != "...":
        Task7Check.configure(text=ModifyTaskName_entry.get())
        Info["Task7Text"] = ModifyTaskName_entry.get()
        
    elif selected_button == 8 and Info["Task8Text"] != "...":
        Task8Check.configure(text=ModifyTaskName_entry.get())
        Info["Task8Text"] = ModifyTaskName_entry.get()
        
    elif selected_button == 9 and Info["Task9Text"] != "...":
        Task9Check.configure(text=ModifyTaskName_entry.get())
        Info["Task9Text"] = ModifyTaskName_entry.get()
        
    ModifyTaskChild.destroy()
    selected_button = 0
    
def ModifyTask():
    global ModifyTaskName_entry, ModifyTaskChild, Button1, Button2, Button3, Button4, Button5, Button6, Button7, Button8, Button9
    ModifyTaskChild = ctk.CTkToplevel(TasksChild)
    ModifyTaskChild.title("Modify Task Note")
    ModifyTaskChild.geometry("500x120")
    ModifyTaskChild.transient(TasksChild)
    ModifyTaskChild.resizable(False, False)
    BACKGROUND = tk.Frame(ModifyTaskChild, bg="#1B1B1B")
    BACKGROUND.pack(expand=True, fill="both")
    Button1 = ctk.CTkButton(BACKGROUND, text=" 1 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=1: ModifyTaskButton(btn))
    Button1.grid(row=1, column=1, padx=(13,2), pady=(13,2))
    Button2 = ctk.CTkButton(BACKGROUND, text=" 2 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=2: ModifyTaskButton(btn))
    Button2.grid(row=1, column=2, padx=2, pady=(13,2))
    Button3 = ctk.CTkButton(BACKGROUND, text=" 3 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=3: ModifyTaskButton(btn))
    Button3.grid(row=1, column=3, padx=2, pady=(13,2))
    Button4 = ctk.CTkButton(BACKGROUND, text=" 4 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=4: ModifyTaskButton(btn))
    Button4.grid(row=2, column=1, padx=(13,2), pady=2)
    Button5 = ctk.CTkButton(BACKGROUND, text=" 5 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=5: ModifyTaskButton(btn))
    Button5.grid(row=2, column=2, padx=2, pady=2)
    Button6 = ctk.CTkButton(BACKGROUND, text=" 6 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=6: ModifyTaskButton(btn))
    Button6.grid(row=2, column=3, padx=2, pady=2)
    Button7 = ctk.CTkButton(BACKGROUND, text=" 7 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=7: ModifyTaskButton(btn))
    Button7.grid(row=3, column=1, padx=(13,2), pady=2)
    Button8 = ctk.CTkButton(BACKGROUND, text=" 8 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=8: ModifyTaskButton(btn))
    Button8.grid(row=3, column=2, padx=2, pady=2)
    Button9 = ctk.CTkButton(BACKGROUND, text=" 9 ", height=3, width=3, font=('Helvetica', 19), command=lambda btn=9: ModifyTaskButton(btn))
    Button9.grid(row=3, column=3, padx=2, pady=2)
    ModifyTaskName_entry = ctk.CTkEntry(BACKGROUND, placeholder_text="                                         Enter Task Name", width=350)
    ModifyTaskName_entry.grid(row=1, column=4, padx=(22,0), pady=(13,2))
    b_ModifyTaskNote = ctk.CTkButton(BACKGROUND, text="Modify Task Note", command=ModifyTaskNote)
    b_ModifyTaskNote.grid(row=3, column=4, padx=(25,0))
    
    if ThemeMode == "Light":
        b_ModifyTaskNote.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button1.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button2.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button3.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button4.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button5.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button6.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button7.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button8.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        Button9.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        BACKGROUND.configure(bg="#E5E4E2")
    elif ThemeMode == "Nitro":
        b_ModifyTaskNote.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button1.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button2.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button3.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button4.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button5.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button6.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button7.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button8.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Button9.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        BACKGROUND.configure(bg="#1b252c")
    else:
        b_ModifyTaskNote.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button1.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button2.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button3.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button4.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button5.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button6.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button7.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button8.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        Button9.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        BACKGROUND.configure(bg="#1B1B1B")
        
def OpenTasks():
    global TasksChild, time_label, BACKGROUND, TaskNotes_label, Task1Check, Task2Check, Task3Check, Task4Check, Task5Check, Task6Check, Task7Check, Task8Check, Task9Check, var1, var2, var3, var4, var5, var6, var7, var8, var9
    TasksChild = ctk.CTkToplevel(root)
    TasksChild.title("Task Notes")
    TasksChild.geometry("1000x600")
    TasksChild.transient(root)
    BACKGROUND = tk.Frame(TasksChild, bg="#1B1B1B")
    BACKGROUND.pack(expand=True, fill="both")
    label_frame = tk.Frame(BACKGROUND, bg="#1B1B1B")
    label_frame.pack(pady=(20,0), fill='x')
    time_label = tk.Label(label_frame, text="", font=("Helvetica", 48), bg="#1B1B1B", fg="white")
    time_label.pack(side="right", padx=20)
    TaskNotes_image_label = ctk.CTkLabel(label_frame, text='', image=PngIcon_AddTaskNote_Big)
    TaskNotes_image_label.pack(side="left", padx=10)
    TaskNotes_label = tk.Label(label_frame, text="Task Notes", font=("Helvetica", 48), bg="#1B1B1B", fg="white")
    TaskNotes_label.pack(side="left", padx=(0,20), pady=5)
    button_frame = ctk.CTkFrame(BACKGROUND)
    button_frame.pack(side="left", padx=20, pady=20, anchor="nw")
    b_AddTask = ctk.CTkButton(button_frame, text="Add Task Note", image=PngIcon_AddTaskNote, compound=tk.LEFT, font=("Helvetica", 17), command=AddTask)
    b_AddTask.pack(pady=(0, 20), anchor="nw")
    b_ModifyTask = ctk.CTkButton(button_frame, text="Modify Task    ", image=PngIcon_ModifyTaskNote, compound=tk.LEFT, font=("Helvetica", 17), command=ModifyTask)
    b_ModifyTask.pack(pady=(0, 20),anchor="nw")
    b_DeleteTask = ctk.CTkButton(button_frame, text="Delete Task    ", image=PngIcon_DeleteTaskNote, compound=tk.LEFT, font=("Helvetica", 17), command=DeleteTask)
    b_DeleteTask.pack(anchor="nw")
    Separator_1 = tk.Frame(BACKGROUND, bg="#353839", width=5, height=500)
    Separator_1.pack(side="left", fill="y")
    
    var1 = ctk.StringVar()
    var2 = ctk.StringVar()
    var3 = ctk.StringVar()
    var4 = ctk.StringVar()
    var5 = ctk.StringVar()
    var6 = ctk.StringVar()
    var7 = ctk.StringVar()
    var8 = ctk.StringVar()
    var9 = ctk.StringVar()
    
    Task1Check = ctk.CTkCheckBox(BACKGROUND, text=Info["Task1Text"], font=("helvetica", 17, "bold"), state="disabled", command=TaskCheckBox, variable=var1)
    Task1Check.pack(anchor="w", padx=10, pady=(27,0))
    Task2Check = ctk.CTkCheckBox(BACKGROUND, text=Info["Task2Text"], font=("helvetica", 17, "bold"), state="disabled", command=TaskCheckBox, variable=var2)
    Task2Check.pack(anchor="w", padx=10, pady=(27,0))
    Task3Check = ctk.CTkCheckBox(BACKGROUND, text=Info["Task3Text"], font=("helvetica", 17, "bold"), state="disabled", command=TaskCheckBox, variable=var3)
    Task3Check.pack(anchor="w", padx=10, pady=(27,0))
    Task4Check = ctk.CTkCheckBox(BACKGROUND, text=Info["Task4Text"], font=("helvetica", 17, "bold"), state="disabled", command=TaskCheckBox, variable=var4)
    Task4Check.pack(anchor="w", padx=10, pady=(27,0))
    Task5Check = ctk.CTkCheckBox(BACKGROUND, text=Info["Task5Text"], font=("helvetica", 17, "bold"), state="disabled", command=TaskCheckBox, variable=var5)
    Task5Check.pack(anchor="w", padx=10, pady=(27,0))
    Task6Check = ctk.CTkCheckBox(BACKGROUND, text=Info["Task6Text"], font=("helvetica", 17, "bold"), state="disabled", command=TaskCheckBox, variable=var6)
    Task6Check.pack(anchor="w", padx=10, pady=(27,0))
    Task7Check = ctk.CTkCheckBox(BACKGROUND, text=Info["Task7Text"], font=("helvetica", 17, "bold"), state="disabled", command=TaskCheckBox, variable=var7)
    Task7Check.pack(anchor="w", padx=10, pady=(27,0))
    Task8Check = ctk.CTkCheckBox(BACKGROUND, text=Info["Task8Text"], font=("helvetica", 17, "bold"), state="disabled", command=TaskCheckBox, variable=var8)
    Task8Check.pack(anchor="w", padx=10, pady=(27,0))
    Task9Check = ctk.CTkCheckBox(BACKGROUND, text=Info["Task9Text"], font=("helvetica", 17, "bold"), state="disabled", command=TaskCheckBox, variable=var9)
    Task9Check.pack(anchor="w", padx=10, pady=(27,0))
    
    if Info["Task1Text"] != "...": 
        Task1Check.configure(state="normal")
    else:
        Task1Check.configure(state="disabled")
        Info["Task1Checked"] = False
    if Info["Task2Text"] != "...": 
        Task2Check.configure(state="normal")
    else:
        Task2Check.configure(state="disabled")
        Info["Task2Checked"] = False
    if Info["Task3Text"] != "...": 
        Task3Check.configure(state="normal")
    else:
        Task3Check.configure(state="disabled")
        Info["Task3Checked"] = False
    if Info["Task4Text"] != "...": 
        Task4Check.configure(state="normal")
    else:
        Task4Check.configure(state="disabled")
        Info["Task4Checked"] = False
    if Info["Task5Text"] != "...": 
        Task5Check.configure(state="normal")
    else:
        Task5Check.configure(state="disabled")
        Info["Task5Checked"] = False
    if Info["Task6Text"] != "...": 
        Task6Check.configure(state="normal")
    else:
        Task6Check.configure(state="disabled")
        Info["Task6Checked"] = False
    if Info["Task7Text"] != "...": 
        Task7Check.configure(state="normal")
    else:
        Task7Check.configure(state="disabled")
        Info["Task7Checked"] = False
    if Info["Task8Text"] != "...": 
        Task8Check.configure(state="normal")
    else:
        Task8Check.configure(state="disabled")
        Info["Task8Checked"] = False
    if Info["Task9Text"] != "...": 
        Task9Check.configure(state="normal")
    else:
        Task9Check.configure(state="disabled")
        Info["Task9Checked"] = False
    
    if Info["Task1Checked"]:
        var1.set("1")
        Task1Check.select()
    if Info["Task2Checked"]: 
        Task2Check.select()
        var2.set("1")
    if Info["Task3Checked"]: 
        Task3Check.select()
        var3.set("1")
    if Info["Task4Checked"]: 
        Task4Check.select()
        var4.set("1")
    if Info["Task5Checked"]: 
        Task5Check.select()
        var5.set("1")
    if Info["Task6Checked"]: 
        Task6Check.select()
        var6.set("1")
    if Info["Task7Checked"]: 
        Task7Check.select()
        var7.set("1")
    if Info["Task8Checked"]: 
        Task8Check.select()
        var8.set("1")
    if Info["Task9Checked"]: 
        Task9Check.select()
        var9.set("1")
    
    if ThemeMode == "Light":
        b_AddTask.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        b_ModifyTask.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        b_DeleteTask.configure(fg_color="#C0C0C0", hover_color="#F5F5F5", text_color="#848482")
        time_label.configure(background="#E5E4E2", fg="#C0C0C0")
        TaskNotes_label.configure(background="#C0C0C0", fg="#E5E4E2")
        Task1Check.configure(text_color="#848482", fg_color="#C0C0C0", checkmark_color="#E5E4E2", hover_color="#848482", border_color="#C0C0C0")
        Task2Check.configure(text_color="#848482", fg_color="#C0C0C0", checkmark_color="#E5E4E2", hover_color="#848482", border_color="#C0C0C0")
        Task3Check.configure(text_color="#848482", fg_color="#C0C0C0", checkmark_color="#E5E4E2", hover_color="#848482", border_color="#C0C0C0")
        Task4Check.configure(text_color="#848482", fg_color="#C0C0C0", checkmark_color="#E5E4E2", hover_color="#848482", border_color="#C0C0C0")
        Task5Check.configure(text_color="#848482", fg_color="#C0C0C0", checkmark_color="#E5E4E2", hover_color="#848482", border_color="#C0C0C0")
        Task6Check.configure(text_color="#848482", fg_color="#C0C0C0", checkmark_color="#E5E4E2", hover_color="#848482", border_color="#C0C0C0")
        Task7Check.configure(text_color="#848482", fg_color="#C0C0C0", checkmark_color="#E5E4E2", hover_color="#848482", border_color="#C0C0C0")
        Task8Check.configure(text_color="#848482", fg_color="#C0C0C0", checkmark_color="#E5E4E2", hover_color="#848482", border_color="#C0C0C0")
        Task9Check.configure(text_color="#848482", fg_color="#C0C0C0", checkmark_color="#E5E4E2", hover_color="#848482", border_color="#C0C0C0")
        label_frame.configure(bg="#C0C0C0")
        Separator_1.configure(bg="#C0C0C0")
        BACKGROUND.configure(bg="#E5E4E2")
    elif ThemeMode == "Nitro":
        time_label.configure(background="#1b252c", fg="#9faeb9")
        TaskNotes_label.configure(background="#313c43", fg="#9faeb9")
        label_frame.configure(bg="#313c43")
        b_AddTask.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        b_ModifyTask.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        b_DeleteTask.configure(fg_color="#313c43", hover_color="#283035", text_color="#9faeb9")
        Task1Check.configure(text_color="#9faeb9", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task2Check.configure(text_color="#9faeb9", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task3Check.configure(text_color="#9faeb9", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task4Check.configure(text_color="#9faeb9", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task5Check.configure(text_color="#9faeb9", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task6Check.configure(text_color="#9faeb9", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task7Check.configure(text_color="#9faeb9", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task8Check.configure(text_color="#9faeb9", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task9Check.configure(text_color="#9faeb9", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Separator_1.configure(bg="#313c43")
        button_frame.configure(fg_color="#1b252c")
        BACKGROUND.configure(bg="#1b252c")
    else:
        b_AddTask.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        b_DeleteTask.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        b_ModifyTask.configure(fg_color="#353839", hover_color="#2A3439", text_color="#C0C0C0")
        time_label.configure(background="#1B1B1B", fg="#C0C0C0")
        TaskNotes_label.configure(background="#353839", fg="#C0C0C0")
        label_frame.configure(bg="#353839")
        Separator_1.configure(bg="#353839")
        Task1Check.configure(text_color="#C0C0C0", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task2Check.configure(text_color="#C0C0C0", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task3Check.configure(text_color="#C0C0C0", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task4Check.configure(text_color="#C0C0C0", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task5Check.configure(text_color="#C0C0C0", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task6Check.configure(text_color="#C0C0C0", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task7Check.configure(text_color="#C0C0C0", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task8Check.configure(text_color="#C0C0C0", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        Task9Check.configure(text_color="#C0C0C0", fg_color="#353839", checkmark_color="#C0C0C0", hover_color="#2A3439")
        button_frame.configure(fg_color="#1B1B1B")
        BACKGROUND.configure(bg="#1B1B1B")
    
    update_time()
    
# Set appearance and theme for CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
SystemThemeMode = ctk.get_appearance_mode()
ctk.set_appearance_mode(ThemeMode)

# Create the main application window
root = ctk.CTk()
root.title("Nitrogen Text Editor")
root.geometry("1280x720")
root.wm_iconbitmap(default="Img\\Nitrogen Window Icon.ico")

# Add a Text Area
text_area = ctk.CTkTextbox(root, font=("Bahnschrift SemiBold Condensed", 12))
text_area.pack(expand=True, fill='both', anchor="ne", pady=(15,0), padx=(64,10))  # Pack at the right side of the window

text_tabs1 = ctk.CTkSegmentedButton(root, values=[1,2], font=("Helvetica", 13), command=lambda value: ChangeTabs(value))
text_tabs2 = ctk.CTkSegmentedButton(root, values=[3,4], font=("Helvetica", 13), command=lambda value: ChangeTabs(value))
text_tabs1.place(x=4,y=15)
text_tabs2.place(x=4,y=48)
text_tabs1.set(1)

if ThemeMode == "Dark": 
    separatorColor = "#414141"
elif ThemeMode == "Nitro":
    separatorColor = "#303a41"
    ctk.set_default_color_theme("blue")
else: 
    separatorColor = "#FFFFFF"

if not file_path == "Untitled.txt":
    with open(file_path, 'r') as file:
        text = file.read()
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, text)

# Load the image
image_path = "Img\\Nitrogen Icon.png"  # Replace with the path to your image file
pil_image = Image.open(image_path)
photo_image = ctk.CTkImage(pil_image)

# IMAGES
PngIcon_NitrogenIcon = tk.PhotoImage(file="Img\\Nitrogen Icon.png")
PngIcon_NitrogenWindowIcon = tk.PhotoImage(file="Img\\Nitrogen Window Icon.png")
PngIcon_NitrogenIcon_Res = PngIcon_NitrogenIcon.subsample(max(PngIcon_NitrogenIcon.width() // 15, PngIcon_NitrogenIcon.height() // 15))
PngIcon_PaintBrush = tk.PhotoImage(file="Img\\BrushIcon.png")
PngIcon_PaintBrush_Res = PngIcon_PaintBrush.subsample(max(PngIcon_PaintBrush.width() // 15, PngIcon_PaintBrush.height() // 15))
PngIcon_Settings = tk.PhotoImage(file="Img\\SettingsIcon.png")
PngIcon_Settings_Big = tk.PhotoImage(file="Img\\SettingsIcon_Big.png")
PngIcon_File = tk.PhotoImage(file="Img\\FileIcon.png")
PngIcon_File_Big = tk.PhotoImage(file="Img\\FileIcon_Big.png")
PngIcon_SearchExtensions = tk.PhotoImage(file="Img\\SearchExtensionsIcon.png")
PngIcon_InstalledExtensions = tk.PhotoImage(file="Img\\InstalledExtensionsIcon.png")
PngIcon_ChangePath = tk.PhotoImage(file="Img\\ChangePathIcon.png")
PngIcon_SaveFile = tk.PhotoImage(file="Img\\SaveFileIcon.png")
PngIcon_CreateNewFile = tk.PhotoImage(file="Img\\CreateNewFileIcon.png")
PngIcon_CreateNewFile_Big = tk.PhotoImage(file="Img\\CreateNewFileIcon_Big.png")
PngIcon_OpenTerminal = tk.PhotoImage(file="Img\\OpenTerminalIcon.png")
PngIcon_OpenFile = tk.PhotoImage(file="Img\\OpenFileIcon.png")
PngIcon_ModifyTaskNote = tk.PhotoImage(file="Img\\ModifyTaskNoteIcon.png")
PngIcon_DeleteTaskNote = tk.PhotoImage(file="Img\\DeleteTaskIcon.png")
PngIcon_AddTaskNote = tk.PhotoImage(file="Img\\AddTaskNoteIcon.png")
PngIcon_AddTaskNote_Big = tk.PhotoImage(file="Img\\AddTaskNoteIcon_Big.png")

# Default font settings
current_font_family = "Segoe UI Semibold"
current_font_size = 15
text_area.configure(font=(current_font_family, current_font_size))

# Create a CTkLabel widget to display the image
image_label = ctk.CTkLabel(root, image=PngIcon_NitrogenIcon, text="")
image_label.pack(side="left", padx=(10,0), pady=(0,5))  # Place the image at the bottom of the window

LineCount_label = ctk.CTkLabel(root, text=f"  Ln: {0}, LnCol: {0}", font=('Segoe UI Semibold', 21, 'bold'), text_color="#848482")
LineCount_label.pack(side="left", anchor="w")

# Create a separator frame
separator1 = tk.Frame(root, bg=separatorColor, width=2)
separator1.pack(side="left", fill="y", padx=(10,0))

Path_label = ctk.CTkLabel(root, text=f"{file_path}", font=('Segoe UI Semibold', 21, 'bold'), text_color="#848482")
Path_label.pack(side="left", anchor="w", padx=10)

separator2 = tk.Frame(root, bg=separatorColor, width=2)
separator2.pack(side="left", fill="y", padx=(0,0))

btn_File = ctk.CTkButton(root, text="", width=15, height=50, image=PngIcon_File, command=OpenFileOptions)
btn_File.pack()
btn_File.place(x=7, y=86) 

btn_Settings = ctk.CTkButton(root, text="", width=15, height=50, image=PngIcon_Settings, command=OpenSettings)
btn_Settings.pack()
btn_Settings.place(x=7, y=146) 

btn_TaskNotes = ctk.CTkButton(root, text="", width=15, height=50, image=PngIcon_AddTaskNote, command=OpenTasks) # TODO
btn_TaskNotes.pack()
btn_TaskNotes.place(x=7, y=206) 

btn_SearchExtensions = ctk.CTkButton(root, text="", width=15, height=50, image=PngIcon_SearchExtensions, command=OpenExtensions)
btn_SearchExtensions.pack()
btn_SearchExtensions.place(x=7, y=266) 

btn_InstalledExtensions = ctk.CTkButton(root, text="", width=15, height=50, image=PngIcon_InstalledExtensions, command=OpenExtensions)
btn_InstalledExtensions.pack()
btn_InstalledExtensions.place(x=7, y=326) 

# Bind mouse wheel events to the functions
root.bind('<Control-MouseWheel>', lambda event: increase_font(event) if event.delta > 0 else decrease_font(event))
root.bind('<Control-t>', toggle_tree)
root.bind('<Control-s>', save_file_shortcut)
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', exit_fullscreen)
text_area.bind("<KeyRelease>", lambda event: on_cursor_move(event, text_area))
text_area.bind("<ButtonRelease-1>", lambda event: on_cursor_move(event, text_area))
text_area.bind("<Tab>", insert_tab)
text_area.bind('<Control-BackSpace>', delete_word)
text_area.bind("<KeyRelease>", modify_text)
text_area.bind('<Control-z>', lambda event: text_area.edit_undo())
text_area.bind('<Control-y>', lambda event: text_area.edit_redo())

if ThemeMode == "Dark": 
    separatorColor = "#414141"
    btn_Settings.configure(fg_color="#353839", hover_color="#2A3439")
    btn_File.configure(fg_color="#353839", hover_color="#2A3439")
    btn_SearchExtensions.configure(fg_color="#353839", hover_color="#2A3439")
    btn_InstalledExtensions.configure(fg_color="#353839", hover_color="#2A3439")
    btn_TaskNotes.configure(fg_color="#353839", hover_color="#2A3439")
    text_tabs1.configure(selected_color="#424141", selected_hover_color="#353839", fg_color="#4C4C4C", unselected_color="#4C4C4C")
    text_tabs2.configure(selected_color="#424141", selected_hover_color="#353839", fg_color="#4C4C4C", unselected_color="#4C4C4C")
elif ThemeMode == "Nitro":
    separatorColor = "#303a41"
    btn_Settings.configure(fg_color="#313c43", hover_color="#283035")
    btn_File.configure(fg_color="#313c43", hover_color="#283035")
    btn_SearchExtensions.configure(fg_color="#313c43", hover_color="#283035")
    btn_TaskNotes.configure(fg_color="#313c43", hover_color="#283035")
    btn_InstalledExtensions.configure(fg_color="#313c43", hover_color="#283035")
    text_tabs1.configure(selected_color="#303a41", selected_hover_color="#212f39", fg_color="#364148", unselected_color="#364148", unselected_hover_color="#29343b", text_color="#9faeb9")
    text_tabs2.configure(selected_color="#303a41", selected_hover_color="#212f39", fg_color="#364148", unselected_color="#364148", unselected_hover_color="#29343b", text_color="#9faeb9")
    text_area.configure(fg_color="#303a41")
    root.configure(fg_color="#212b32")
    Path_label.configure(text_color="#9faeb9")
    LineCount_label.configure(text_color="#9faeb9")
else: 
    separatorColor = "#FFFFFF"
    btn_Settings.configure(fg_color="#C0C0C0", hover_color="#F5F5F5")
    btn_File.configure(fg_color="#C0C0C0", hover_color="#F5F5F5")
    btn_SearchExtensions.configure(fg_color="#C0C0C0", hover_color="#F5F5F5")
    btn_InstalledExtensions.configure(fg_color="#C0C0C0", hover_color="#F5F5F5")
    btn_TaskNotes.configure(fg_color="#C0C0C0", hover_color="#F5F5F5")
    text_tabs1.configure(selected_color="#D2D0CB", selected_hover_color="#F5F5F5", fg_color="#C0C0C0", unselected_color="#C0C0C0")
    text_tabs2.configure(selected_color="#D2D0CB", selected_hover_color="#F5F5F5", fg_color="#C0C0C0", unselected_color="#C0C0C0")

SHARED_STATE.SHARED_root = root                      
SHARED_STATE.SHARED_text_area = text_area                 
SHARED_STATE.SHARED_LineCount_label = LineCount_label           
SHARED_STATE.SHARED_ChangeTabs = ChangeTabs                
SHARED_STATE.SHARED_ThemeMode = ThemeMode                 
SHARED_STATE.SHARED_ChangeTheme = ChangeTheme
SHARED_STATE.SHARED_separatorColor = separatorColor
SHARED_STATE.SHARED_text_tabs1 = text_tabs1
SHARED_STATE.SHARED_text_tabs2 = text_tabs2
SHARED_STATE.SHARED_separator1 = separator1
SHARED_STATE.SHARED_separator2 = separator2
SHARED_STATE.SHARED_btn_File = btn_File
SHARED_STATE.SHARED_btn_Settings = btn_Settings
SHARED_STATE.SHARED_btn_TaskNotes = btn_TaskNotes
SHARED_STATE.SHARED_btn_SearchExtensions = btn_SearchExtensions
SHARED_STATE.SHARED_btn_InstalledExtensions = btn_InstalledExtensions

ExtensionRunner.ExtensionRunner()

# Run the application
root.mainloop()

Info["THEME"] = ThemeMode
if file_path == "" or file_path == "Untitled.txt":
    Info["STD-Path"] = "Untitled.txt"
JSON.JsonSaveInfo(Info, "Info.json")