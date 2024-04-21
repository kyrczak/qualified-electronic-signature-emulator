from .key_generator import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox,filedialog
from .hardware import *
WINDOW_SIZE = "800x600"
WINDOW_TITLE = "Qualified electronic signature emulator"
KEY_FORMAT = ".bin"

def start_app():
    window = tk.Tk()
    window.geometry(WINDOW_SIZE)
    window.title(WINDOW_TITLE)

    tab_control = ttk.Notebook(window)
    tab1 = tk.Frame(tab_control)
    tab2 = tk.Frame(tab_control)
    tab3 = tk.Frame(tab_control)
    tab_control.add(tab1, text='Sign a document')
    tab_control.add(tab2, text='Encryption/Decryption')
    tab_control.add(tab3, text="Key generator")

    setup_tab1(tab1)
    setup_tab2(tab2)
    setup_tab3(tab3)
    tab_control.pack(expand=1, fill='both')
    
    window.mainloop()


def setup_tab1(tab1: tk.Frame):
    def get_keys_wrapper():
         usb_stick_path = usb_sticks_var.get()
         get_keys(key_dropdown,usb_stick_path)

    def refresh_drives_wrapper():
         usb_sticks = get_available_usb_sticks()
         usb_drive_dropdown['values'] = usb_sticks
         key_dropdown['values'] = []
         key_dropdown.set("")
         if usb_sticks:
            usb_drive_dropdown.current(0)  # Select the first key file by default
         else:
            usb_drive_dropdown.set("")

    label = tk.Label(tab1, text="Select USB Drive")
    label.grid(row=0, column=0, padx=5, pady=10, sticky="nw")

    usb_sticks = []
    usb_sticks_var = tk.StringVar(tab1)
    

    usb_drive_dropdown = ttk.Combobox(tab1, textvariable=usb_sticks_var, values=usb_sticks)
    usb_drive_dropdown.grid(row=0, column=1, padx=5, pady=10, sticky="nw")

    refresh_usb_sticks_button = ttk.Button(tab1, text="Refresh", command=refresh_drives_wrapper)
    refresh_usb_sticks_button.grid(row=0, column=2, padx=5, pady=7, sticky="nw")

    key_files = []
    key_var = tk.StringVar(tab1)
    key_dropdown = ttk.Combobox(tab1, textvariable=key_var, values=key_files)
    
    find_keys_button = ttk.Button(tab1, text="Find Keys", command=get_keys_wrapper)
    find_keys_button.grid(row=0, column=3, pady=7, sticky="nw")

    key_label = tk.Label(tab1, text="Select Key File")
    key_label.grid(row=1, column=0, padx=5, pady=10, sticky="nw")

    key_dropdown.grid(row=1, column=1, padx=5, pady=10, sticky="nw")
    refresh_drives_wrapper()
    get_keys_wrapper()
    return tab1

def setup_tab2(tab2: tk.Frame):
    load_button = tk.Button(tab2, text="Load File", command=load_file)
    load_button.pack(pady=10)

    encrypt_button = tk.Button(tab2, text="Encrypt File", command=aes_encryption)
    encrypt_button.pack(pady=5)

    decrypt_button = tk.Button(tab2, text="Decrypt File", command=aes_decryption)
    decrypt_button.pack(pady=5) 

def setup_tab3(tab3: tk.Frame):
    def generate_keys():
        public_key, private_key = rsa_generate_key_pair()
        public_key_text.delete(1.0, tk.END)
        public_key_text.insert(tk.END, public_key.decode('utf-8'))
        private_key_text.delete(1.0, tk.END)
        private_key_text.insert(tk.END, private_key.decode('utf-8'))

    def save_private_key():
        pin = pin_entry.get()
        if not pin:
            messagebox.showerror("Error", "Please enter a PIN.")
            return
        
        private_key = private_key_text.get(1.0, tk.END).strip()
        encrypted_private_key = aes_encryption(private_key.encode('utf-8'), pin)
        filename = filedialog.asksaveasfilename(defaultextension=KEY_FORMAT)
        if filename:
            save_key_to_file(encrypted_private_key, filename)
            messagebox.showinfo("Success", "Private key saved successfully.")

    def save_public_key():
             public_key = public_key_text.get(1.0, tk.END).strip()
             filename = filedialog.asksaveasfilename(defaultextension=KEY_FORMAT)
             if filename:
                save_key_to_file(str.encode(public_key), filename)
                messagebox.showinfo("Success", "Public key saved successfully.")


    generate_button = tk.Button(tab3, text="Generate Keys", command=generate_keys)
    generate_button.grid(row=0, column=0, pady=5)

    public_key_label = tk.Label(tab3, text="Public Key:")
    public_key_label.grid(row=1, column=0, pady=5, sticky="w")

    public_key_text = tk.Text(tab3, height=5, width=60)
    public_key_text.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    private_key_label = tk.Label(tab3, text="Private Key:")
    private_key_label.grid(row=3, column=0, pady=5, sticky="w")

    private_key_text = tk.Text(tab3, height=5, width=60)
    private_key_text.grid(row=4, column=0, padx=5, pady=5, sticky="w")

    pin_label = tk.Label(tab3, text="Enter PIN:")
    pin_label.grid(row=5, column=0, pady=5, sticky="w")

    pin_entry = tk.Entry(tab3, show="*")
    pin_entry.grid(row=6, column=0, padx=5, pady=5, sticky="w")

    save_button = tk.Button(tab3, text="Save Private Key", command=save_private_key)
    save_button.grid(row=7, column=0, pady=5)
    save_button = tk.Button(tab3, text="Save Public Key", command=save_public_key)
    save_button.grid(row=8, column=0, pady=5)


def get_keys(key_dropdown:ttk.Combobox, usb_stick_path:str):
        key_files = scan_for_key_files(usb_stick_path)
        key_dropdown['values'] = key_files
        if key_files:
            key_dropdown.current(0)  # Select the first key file by default
        else:
            key_dropdown.set("")
    
def load_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Do something with the file_path, such as reading the file
        print("File path:", file_path)