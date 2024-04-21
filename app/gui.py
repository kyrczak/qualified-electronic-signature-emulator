import key_generator as kg
import tkinter as tk
from tkinter import ttk

WINDOW_SIZE = "800x600"
WINDOW_TITLE = "Qualified electronic signature emulator"

def start_app():
    window = tk.Tk()
    window.geometry(WINDOW_SIZE)
    window.title(WINDOW_TITLE)

    tab_control = ttk.Notebook(window)

    tab1 = tk.Frame(tab_control)
    tab2 = tk.Frame(tab_control)
    tab3 = tk.Frame(tab_control)

    tab_control.add(tab1, text='Key generator')
    tab_control.add(tab2, text='Sign a document')
    tab_control.add(tab3, text='Encryption/Decryption')
    tab_control.pack(expand=1, fill='both')
    
    window.mainloop()

