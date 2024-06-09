from .key_generator import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox,filedialog
from .hardware import *
from .file_modification import *
from .signature import *
WINDOW_SIZE = "450x300"
WINDOW_TITLE = "Qualified electronic signature emulator"
KEY_FORMAT = ".bin"

def start_app():
    window = tk.Tk()
    window.geometry(WINDOW_SIZE)
    window.title(WINDOW_TITLE)

    tab_control = ttk.Notebook(window)
    tab1 = tk.Frame(tab_control)
    tab2 = tk.Frame(tab_control)
    tab_control.add(tab1, text='Sign a document')
    tab_control.add(tab2, text='Encryption/Decryption')
    

    setup_tab1(tab1)
    setup_tab2(tab2)
    
    
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

    def sign_document_wrapper():
        key_path = key_var.get()
        file_path = file_var.get()
        try:
            sign(file_path, key_path)
            messagebox.showinfo("Success", f"Document signed sucesfully at {file_path}.xml")
        except:
            messagebox.showerror("Error", f"Can't sign document")
        
    def verify_signature_wrapper():
        key_path = key_var.get()
        file_path = file_var.get()
        try:
            verify(file_path, key_path)
            messagebox.showinfo("Success", f"Signature verified sucesfully")
        except:
            messagebox.showerror("Error", f"Can't verify signature")

    label = tk.Label(tab1, text="Select USB Drive")
    label.grid(row=0, column=0, padx=5, pady=10, sticky="nw")

    usb_sticks = []
    usb_sticks_var = tk.StringVar(tab1)
    
    file_var = tk.StringVar(tab1)
    file_label = ttk.Label(tab1, text="Select File")
    file_label.grid(row=2, column=0, padx=5, pady=10, sticky="nw")
    file_entry = ttk.Entry(tab1, textvariable=file_var)
    file_entry.grid(row=2, column=1, padx=5, pady=10, sticky="nw")
    choose_file_button = ttk.Button(tab1, text="Choose File", command=lambda: file_var.set(filedialog.askopenfilename()))
    choose_file_button.grid(row=2, column=2, padx=5, pady=10, sticky="nw")
    
    sign_button = ttk.Button(tab1, text="Sign Document", command=sign_document_wrapper)
    sign_button.grid(row=3, column=1, padx=5, pady=10, sticky="nw")
    verify_button = ttk.Button(tab1, text="Verify Signature", command=verify_signature_wrapper)
    verify_button.grid(row=3, column=2, padx=5, pady=10, sticky="nw")

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
    def load_file_to_encrypt():
        nonlocal file_path
        file_path = filedialog.askopenfilename()
        if file_path:
            print("File path:", file_path)

    def load_public_key()->bytes:
        nonlocal key_path
        nonlocal file_path
        nonlocal public_key
        if file_path == "":
            messagebox.showerror("Error","Firstly load the file")
            return
        key_path = filedialog.askopenfilename()
        if key_path.endswith(KEY_FORMAT):
            print("Key: ",key_path)
            public_key = read_key_from_file(key_path)

    def load_private_key()->bytes:
        nonlocal key_path
        nonlocal file_path
        nonlocal private_key
        nonlocal pin
        pin = pin_entry.get()
        if file_path == "":
            messagebox.showerror("Error","Firstly load the file")
            return
        if(pin == ""):
            messagebox.showerror("Error","Enter pin")
            return
        
        if file_path:
            key_path = filedialog.askopenfilename()
            if key_path.endswith(KEY_FORMAT):
                print("Key: ",key_path)
                private_key = read_key_from_file(key_path,pin)

    def rsa_encrypt_wrapper():
        try:    
            rsa_encrypt(file_path,public_key)
            messagebox.showinfo("Success", f"File encrypted sucesfully at {os.path.dirname(file_path)}\\encrypted_{os.path.basename(file_path)}")
        except:
            messagebox.showerror("Error", f"Can't encrypt")
            
    def rsa_decrypt_wrapper():
         try:    
            rsa_decrypt(file_path,private_key)
            messagebox.showinfo("Success", f"File decrypted sucesfully at {os.path.dirname(file_path)}\\decrypted_{os.path.basename(file_path)}")
         except:
            messagebox.showerror("Error", f"Can't decrypt")
            
    file_path = ""
    key_path = ""
    public_key = ""
    private_key = ""
    pin = ""

    load_button = tk.Button(tab2, text="Load File", command=load_file_to_encrypt)
    load_button.pack(pady=10)
    load_button = tk.Button(tab2, text="Load Public Key", command=load_public_key)
    load_button.pack(pady=10)

    pin_label = tk.Label(tab2, text="Enter PIN:")
    pin_label.pack(pady=5)

    pin_entry = tk.Entry(tab2, show="*")
    pin_entry.pack(pady=5)

    load_button = tk.Button(tab2, text="Load Private Key", command=load_private_key)
    load_button.pack(pady=10)

    encrypt_button = tk.Button(tab2, text="Encrypt File", command=rsa_encrypt_wrapper)
    encrypt_button.pack(pady=5)

    

    decrypt_button = tk.Button(tab2, text="Decrypt File", command=rsa_decrypt_wrapper)
    decrypt_button.pack(pady=5) 



def get_keys(key_dropdown:ttk.Combobox, usb_stick_path:str):
        key_files = scan_for_key_files(usb_stick_path)
        key_dropdown['values'] = key_files
        if key_files:
            key_dropdown.current(0)  # Select the first key file by default
        else:
            key_dropdown.set("")
    


