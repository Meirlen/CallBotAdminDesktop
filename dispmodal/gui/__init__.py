import tkinter as tk
import tkinter.ttk as ttk

from .properties import PropertiesFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        frame = tk.Frame(self)

        PropertiesFrame(frame).pack(fill=tk.X)
        ...

        frame.pack(fill=tk.BOTH, padx=125, pady=35)
