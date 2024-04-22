from .key_generator import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox,filedialog
WINDOW_SIZE = "500x450"
WINDOW_TITLE = "Key Generator"
KEY_FORMAT = ".bin"

def start_app():
    window = tk.Tk()
    window.geometry(WINDOW_SIZE)
    window.title(WINDOW_TITLE)

    tab_control = ttk.Notebook(window)
    tab1 = tk.Frame(tab_control)
    tab2 = tk.Frame(tab_control)
    tab_control.add(tab1, text='Key generator')
    setup_tab1(tab1)

    tab_control.pack(expand=1, fill='both')
    
    window.mainloop()

def setup_tab1(tab1: tk.Frame):
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


    generate_button = tk.Button(tab1, text="Generate Keys", command=generate_keys)
    generate_button.grid(row=0, column=0, pady=5)

    public_key_label = tk.Label(tab1, text="Public Key:")
    public_key_label.grid(row=1, column=0, pady=5, sticky="w")

    public_key_text = tk.Text(tab1, height=5, width=60)
    public_key_text.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    private_key_label = tk.Label(tab1, text="Private Key:")
    private_key_label.grid(row=3, column=0, pady=5, sticky="w")

    private_key_text = tk.Text(tab1, height=5, width=60)
    private_key_text.grid(row=4, column=0, padx=5, pady=5, sticky="w")

    pin_label = tk.Label(tab1, text="Enter PIN:")
    pin_label.grid(row=5, column=0, pady=5, sticky="w")

    pin_entry = tk.Entry(tab1, show="*")
    pin_entry.grid(row=6, column=0, padx=5, pady=5, sticky="w")

    save_button = tk.Button(tab1, text="Save Private Key", command=save_private_key)
    save_button.grid(row=7, column=0, pady=5)
    save_button = tk.Button(tab1, text="Save Public Key", command=save_public_key)
    save_button.grid(row=8, column=0, pady=5)