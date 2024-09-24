import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from tkinter import ttk
import subprocess


class ADBExecutor:
    def __init__(self, master):
        self.master = master
        self.master.title("PyADB")
        self.master.geometry("700x600")  # Adjusted height for compactness
        self.master.configure(bg="#f0f0f0")  # Light background color

        # Create a Notebook (tabbed interface) with left-aligned tabs
        self.notebook = ttk.Notebook(self.master, width=600)  # Set width for the notebook
        self.notebook.pack(padx=10, pady=10, fill="both", expand=True)

        # Create tabs with padding for separation
        self.info_output_area = self.create_info_tab()
        self.repair_output_area = self.create_repair_tab()
        self.command_output_area = self.create_command_tab()
        self.flashing_output_area = self.create_flashing_tab()

        # Customize the style
        self.style = ttk.Style()
        self.style.configure("TNotebook", padding=0)
        self.style.configure("TNotebook.Tab", padding=[10, 5])
        self.style.configure("TButton", padding=5)
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
        self.style.configure("TText", font=("Arial", 10))

        # Place the tabs on the left side
        self.notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a frame for the tabs
        self.tab_frame = ttk.Frame(self.master)
        self.tab_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.notebook.add(self.tab_frame)

    def create_info_tab(self):
        """Creates the informational ADB commands tab."""
        frame_info = ttk.Frame(self.notebook)
        self.notebook.add(frame_info, text="Info")

        # Button to check ADB devices
        button_devices = ttk.Button(frame_info, text="Check ADB Devices", command=self.execute_adb_devices)
        button_devices.pack(pady=20)

        # Output area for the informational tab
        output_area = self.create_output_area(frame_info)
        return output_area

    def create_repair_tab(self):
        """Creates the repair ADB commands tab."""
        frame_repair = ttk.Frame(self.notebook)
        self.notebook.add(frame_repair, text="Repairing")

        # Buttons for repair commands
        button_reboot_bootloader = ttk.Button(frame_repair, text="Reboot to Bootloader", command=self.execute_adb_reboot_bootloader)
        button_reboot_bootloader.pack(pady=10)

        button_reboot_recovery = ttk.Button(frame_repair, text="Reboot to Recovery", command=self.execute_adb_reboot_recovery)
        button_reboot_recovery.pack(pady=10)

        button_reboot_normal = ttk.Button(frame_repair, text="Reboot Normally", command=self.execute_adb_reboot)
        button_reboot_normal.pack(pady=10)

        # Output area for the repair tab
        output_area = self.create_output_area(frame_repair)
        return output_area

    def create_command_tab(self):
        """Creates the custom ADB command executor tab."""
        frame_command = ttk.Frame(self.notebook)
        self.notebook.add(frame_command, text="Command")

        # Text box for custom ADB command input
        self.custom_command_entry = scrolledtext.ScrolledText(frame_command, height=5, width=60, wrap=tk.WORD)
        self.custom_command_entry.pack(pady=10, padx=10)

        # Bind the Enter key to execute custom command and prevent new line
        self.custom_command_entry.bind("<Return>", self.execute_custom_command)
        self.custom_command_entry.bind("<KeyRelease-Return>", lambda event: "break")  # Prevent new line on Enter

        # Output area for the command tab
        output_area = self.create_output_area(frame_command)
        return output_area

    def create_flashing_tab(self):
        """Creates the flashing commands tab."""
        frame_flashing = ttk.Frame(self.notebook)
        self.notebook.add(frame_flashing, text="Flashing")

        # Button to browse for a file
        button_browse = ttk.Button(frame_flashing, text="Browse for ZIP/IMG", command=self.browse_file)
        button_browse.pack(pady=10)

        # Label to display selected file path
        self.file_label = ttk.Label(frame_flashing, text="No file selected", wraplength=400)
        self.file_label.pack(pady=10)

        # Button for ADB sideload
        button_sideload = ttk.Button(frame_flashing, text="ADB Sideload", command=self.execute_adb_sideload)
        button_sideload.pack(pady=10)

        # Button for Fastboot flash
        button_fastboot = ttk.Button(frame_flashing, text="Fastboot Flash", command=self.execute_fastboot_flash)
        button_fastboot.pack(pady=10)

        # Output area for the flashing tab
        output_area = self.create_output_area(frame_flashing)
        return output_area

    def create_output_area(self, parent):
        """Creates an output area for the given parent frame."""
        output_area = scrolledtext.ScrolledText(parent, height=8, width=70, state='disabled', bg="#ffffff")
        output_area.pack(pady=10, padx=10, fill=tk.X)
        return output_area

    def execute_command(self, command):
        """Executes an ADB command and returns the result."""
        try:
            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = result.communicate()

            if result.returncode == 0:
                return output.strip()
            else:
                return error.strip()

        except Exception as e:
            return f"An error occurred: {e}"

    def execute_adb_devices(self):
        """Executes the 'adb devices' command."""
        output = self.execute_command("adb devices")
        self.display_output(output, self.info_output_area)

    def execute_adb_reboot_bootloader(self):
        """Executes the 'adb reboot bootloader' command."""
        output = self.execute_command("adb reboot bootloader")
        self.display_output(output, self.repair_output_area)
        messagebox.showinfo("Info", "Rebooting to bootloader...")

    def execute_adb_reboot_recovery(self):
        """Executes the 'adb reboot recovery' command."""
        output = self.execute_command("adb reboot recovery")
        self.display_output(output, self.repair_output_area)
        messagebox.showinfo("Info", "Rebooting to recovery...")

    def execute_adb_reboot(self):
        """Executes the 'adb reboot' command."""
        output = self.execute_command("adb reboot")
        self.display_output(output, self.repair_output_area)
        messagebox.showinfo("Info", "Rebooting normally...")

    def execute_custom_command(self, event):
        """Executes a custom ADB command from the text box."""
        command = self.custom_command_entry.get("1.0", tk.END).strip()
        if command:
            output = self.execute_command(command)
            self.display_output(output, self.command_output_area)

    def browse_file(self):
        """Opens a file dialog to select a zip or img file."""
        self.selected_file = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip"), ("IMG files", "*.img")])
        if self.selected_file:
            self.file_label.config(text=self.selected_file)

    def execute_adb_sideload(self):
        """Executes the 'adb sideload' command."""
        if hasattr(self, 'selected_file'):
            command = f"adb sideload {self.selected_file}"
            output = self.execute_command(command)
            self.display_output(output, self.flashing_output_area)
        else:
            messagebox.showwarning("Warning", "No file selected!")

    def execute_fastboot_flash(self):
        """Executes the 'fastboot flash' command."""
        if hasattr(self, 'selected_file'):
            command = f"fastboot flash {self.selected_file}"
            output = self.execute_command(command)
            self.display_output(output, self.flashing_output_area)
        else:
            messagebox.showwarning("Warning", "No file selected!")

    def display_output(self, output, output_area):
        """Displays the command output in the appropriate output area."""
        output_area.config(state='normal')  # Enable the text area for editing
        output_area.delete("1.0", tk.END)  # Clear previous output
        output_area.insert(tk.END, output)  # Insert new output
        output_area.config(state='disabled')  # Disable the text area for editing


if __name__ == "__main__":
    root = tk.Tk()
    app = ADBExecutor(root)
    root.mainloop()
