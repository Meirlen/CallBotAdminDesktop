import tkinter as tk
import tkinter.ttk as ttk

from .properties import PropertiesFrame
from .style import BACKGROUND


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.config(background=BACKGROUND)
        ttk.Style(self).configure("TFrame", background=BACKGROUND)

        frame = ttk.Frame(self)

        PropertiesFrame(frame).pack(fill=tk.X)
        ...

        frame.pack(fill=tk.BOTH, padx=125, pady=35)
