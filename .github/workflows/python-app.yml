import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import font as tkfont
import subprocess
import sys
import threading
import time
import webbrowser

class ModernButton(tk.Canvas):
    def __init__(self, master, text, command=None, corner_radius=10, padding=10, **kwargs):
        self.text = text
        self.corner_radius = corner_radius
        self.padding = padding

        # Calculate button size based on text
        self.font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        text_width = self.font.measure(self.text)
        text_height = self.font.metrics("linespace")

        self.width = text_width + (2 * self.padding)
        self.height = text_height + (2 * self.padding)

        super().__init__(master, width=self.width, height=self.height, highlightthickness=0, **kwargs)
        
        self.command = command

        self.normal_color = "#4CAF50"
        self.hover_color = "#45a049"
        self.click_color = "#3d8b40"

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

        self.draw_normal()

    def draw_normal(self):
        self.create_rounded_rect(0, 0, self.width, self.height, self.corner_radius, fill=self.normal_color, outline="")
        self.create_text(self.width/2, self.height/2, text=self.text, fill="white", font=self.font)

    def on_enter(self, event):
        self.delete("all")
        self.create_rounded_rect(0, 0, self.width, self.height, self.corner_radius, fill=self.hover_color, outline="")
        self.create_text(self.width/2, self.height/2, text=self.text, fill="white", font=self.font)

    def on_leave(self, event):
        self.delete("all")
        self.draw_normal()

    def on_press(self, event):
        self.delete("all")
        self.create_rounded_rect(0, 0, self.width, self.height, self.corner_radius, fill=self.click_color, outline="")
        self.create_text(self.width/2, self.height/2, text=self.text, fill="white", font=self.font)

    def on_release(self, event):
        self.delete("all")
        self.draw_normal()
        if self.command:
            self.command()

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]

        return self.create_polygon(points, smooth=True, **kwargs)

class SimpleGUI:
    def __init__(self, master):
        self.master = master
        master.title("TkinterADB")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.setup_styles()

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both")

        # Create frames for the tabs
        self.executor_tab = ttk.Frame(self.notebook)
        self.preset_cmds_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.others_tab = ttk.Frame(self.notebook)  # New tab

        # Add the frames as tabs to the notebook
        self.notebook.add(self.executor_tab, text="Executor")
        self.notebook.add(self.preset_cmds_tab, text="Preset Cmds")
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.add(self.others_tab, text="Others")  # Add the new tab

        # Add content to tabs
        self.setup_executor_tab()
        self.setup_preset_cmds_tab()
        self.setup_settings_tab()
        self.setup_others_tab()  # Setup the new tab

        # Start device list refresh thread
        self.refresh_thread = threading.Thread(target=self.refresh_device_list_periodically, daemon=True)
        self.refresh_thread.start()

    def setup_styles(self):
        self.bg_color = "#E8E8E8"
        self.fg_color = "#333333"
        self.button_bg = "#4CAF50"
        self.button_fg = "white"
        self.entry_bg = "#F5F5F5"
        self.hover_bg = "#45a049"

        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TButton", padding=10, relief="flat", background=self.button_bg, foreground=self.button_fg)
        self.style.map("TButton", background=[("active", self.hover_bg)])
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, padding=5)
        self.style.configure("TEntry", padding=5, fieldbackground=self.entry_bg)
        self.style.configure("TCombobox", padding=5, fieldbackground=self.entry_bg)
        self.style.configure("TNotebook", background=self.bg_color)
        self.style.configure("TNotebook.Tab", padding=[10, 5], background="#D0D0D0")
        self.style.map("TNotebook.Tab", background=[("selected", self.bg_color)])

    def setup_executor_tab(self):
        # Device selection dropdown
        ttk.Label(self.executor_tab, text="Select Device:").pack(pady=(10, 0))
        self.device_var = tk.StringVar()
        self.device_dropdown = ttk.Combobox(self.executor_tab, textvariable=self.device_var, state="readonly")
        self.device_dropdown.pack(pady=5, padx=10, fill=tk.X)

        # ADB command input
        ttk.Label(self.executor_tab, text="Enter ADB Command:").pack(pady=(10, 0))
        self.command_entry = ttk.Entry(self.executor_tab)
        self.command_entry.pack(pady=5, padx=10, fill=tk.X)

        # Execute button
        self.execute_button = ModernButton(self.executor_tab, text="Execute", command=self.execute_adb_command)
        self.execute_button.pack(pady=10)

        # Output text area
        ttk.Label(self.executor_tab, text="Output:").pack(pady=(10, 0))
        self.output_text = tk.Text(self.executor_tab, height=10, wrap=tk.WORD, bg=self.entry_bg, fg=self.fg_color)
        self.output_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

    def setup_preset_cmds_tab(self):
        # Preset commands dropdown
        ttk.Label(self.preset_cmds_tab, text="Select Preset:").pack(pady=(10, 0))
        self.preset_var = tk.StringVar()
        self.preset_dropdown = ttk.Combobox(self.preset_cmds_tab, textvariable=self.preset_var, state="readonly")
        self.preset_dropdown['values'] = ['Reboot', 'Flashing']
        self.preset_dropdown.set('Reboot')
        self.preset_dropdown.pack(pady=5, padx=10, fill=tk.X)
        self.preset_dropdown.bind('<<ComboboxSelected>>', self.on_preset_selected)

        # Frame for preset buttons
        self.preset_frame = ttk.Frame(self.preset_cmds_tab)
        self.preset_frame.pack(pady=10, fill=tk.X)

        # Reboot buttons
        self.reboot_frame = ttk.Frame(self.preset_frame)
        self.reboot_frame.pack(fill=tk.X)

        self.reboot_recovery_btn = ModernButton(self.reboot_frame, text="Reboot to Recovery", command=lambda: self.execute_preset_cmd("reboot recovery"))
        self.reboot_recovery_btn.pack(side=tk.LEFT, padx=5)

        self.reboot_bootloader_btn = ModernButton(self.reboot_frame, text="Reboot to Bootloader", command=lambda: self.execute_preset_cmd("reboot bootloader"))
        self.reboot_bootloader_btn.pack(side=tk.LEFT, padx=5)

        self.reboot_btn = ModernButton(self.reboot_frame, text="Reboot", command=lambda: self.execute_preset_cmd("reboot"))
        self.reboot_btn.pack(side=tk.LEFT, padx=5)

        # Flashing buttons
        self.flashing_frame = ttk.Frame(self.preset_frame)
        self.flashing_frame.pack(fill=tk.X)
        self.flashing_frame.pack_forget()  # Initially hidden

        self.sideload_btn = ModernButton(self.flashing_frame, text="ADB Sideload", command=self.adb_sideload)
        self.sideload_btn.pack(side=tk.LEFT, padx=5)

        self.fastboot_flash_btn = ModernButton(self.flashing_frame, text="Fastboot Flash", command=self.fastboot_flash)
        self.fastboot_flash_btn.pack(side=tk.LEFT, padx=5)

    def setup_settings_tab(self):
        # Theme selection
        theme_frame = ttk.Frame(self.settings_tab)
        theme_frame.pack(padx=10, pady=10, fill=tk.X)

        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=(0, 10))

        self.theme_switch = ttk.Checkbutton(theme_frame, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(side=tk.LEFT)

    def setup_others_tab(self):
        # Create a frame for the hyperlink
        link_frame = ttk.Frame(self.others_tab)
        link_frame.pack(pady=20)

        # Create a label with hyperlink styling
        link_label = ttk.Label(link_frame, 
                               text="Visit Odin Download",
                               foreground="blue", 
                               cursor="hand2")
        link_label.pack()

        # Bind the click event to open the URL
        link_label.bind("<Button-1>", lambda e: self.open_url("https://odindownload.com"))

        # Optional: Add an underline when hovering
        link_label.bind("<Enter>", lambda e: link_label.configure(font=("TkDefaultFont", 10, "underline")))
        link_label.bind("<Leave>", lambda e: link_label.configure(font=("TkDefaultFont", 10)))

    def open_url(self, url):
        webbrowser.open_new(url)

    def toggle_theme(self):
        if self.theme_switch.instate(["selected"]):  # Dark mode
            self.bg_color = "#2E2E2E"
            self.fg_color = "#E0E0E0"
            self.button_bg = "#4CAF50"
            self.button_fg = "white"
            self.entry_bg = "#3E3E3E"
            self.hover_bg = "#45a049"
        else:  # Light mode
            self.bg_color = "#E8E8E8"
            self.fg_color = "#333333"
            self.button_bg = "#4CAF50"
            self.button_fg = "white"
            self.entry_bg = "#F5F5F5"
            self.hover_bg = "#45a049"

        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TButton", background=self.button_bg, foreground=self.button_fg)
        self.style.map("TButton", background=[("active", self.hover_bg)])
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        self.style.configure("TEntry", fieldbackground=self.entry_bg, foreground=self.fg_color)
        self.style.configure("TCombobox", fieldbackground=self.entry_bg, foreground=self.fg_color)
        self.style.configure("TNotebook", background=self.bg_color)
        self.style.configure("TNotebook.Tab", background=self.entry_bg, foreground=self.fg_color)
        self.style.map("TNotebook.Tab", background=[("selected", self.bg_color)])
        
        self.output_text.config(bg=self.entry_bg, fg=self.fg_color)
        self.master.configure(bg=self.bg_color)

    def on_preset_selected(self, event):
        selected = self.preset_var.get()
        if selected == 'Reboot':
            self.reboot_frame.pack(fill=tk.X)
            self.flashing_frame.pack_forget()
        elif selected == 'Flashing':
            self.flashing_frame.pack(fill=tk.X)
            self.reboot_frame.pack_forget()

    def execute_adb_command(self):
        command = self.command_entry.get()
        device = self.device_var.get()
        if device:
            command = f"adb -s {device} {command}"
        else:
            command = f"adb {command}"
        
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, output)
        except subprocess.CalledProcessError as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error: {e.output}")

    def execute_preset_cmd(self, cmd):
        device = self.device_var.get()
        if device:
            command = f"adb -s {device} {cmd}"
        else:
            command = f"adb {cmd}"
        
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, output)
        except subprocess.CalledProcessError as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error: {e.output}")

    def adb_sideload(self):
        file_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if file_path:
            device = self.device_var.get()
            if device:
                command = f"adb -s {device} sideload \"{file_path}\""
            else:
                command = f"adb sideload \"{file_path}\""
            
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, output)
            except subprocess.CalledProcessError as e:
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, f"Error: {e.output}")

    def fastboot_flash(self):
        file_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if file_path:
            command = f"fastboot flash boot \"{file_path}\""
            
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, output)
            except subprocess.CalledProcessError as e:
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, f"Error: {e.output}")

    def refresh_device_list_periodically(self):
        while True:
            try:
                output = subprocess.check_output("adb devices", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                lines = output.strip().split('\n')[1:]  # Skip the first line which is usually "List of devices attached"
                devices = []
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 2 and parts[1] == "device":
                        devices.append(parts[0])
                
                self.master.after(0, self.update_device_list, devices)
            except subprocess.CalledProcessError as e:
                print(f"Error refreshing device list: {e}")
            except Exception as e:
                print(f"Unexpected error refreshing device list: {e}")
            
            time.sleep(5)  # Refresh every 5 seconds

    def update_device_list(self, devices):
        self.device_dropdown['values'] = devices
        if devices and not self.device_var.get():
            self.device_var.set(devices[0])
        elif not devices:
            self.device_var.set('')  # Clear the selection if no devices are available

def run_gui():
    root = tk.Tk()
    root.geometry("600x500")
    gui = SimpleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
