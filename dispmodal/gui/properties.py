import tkinter as tk
import tkinter.ttk as ttk


class PropertyEntry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ttk.Button(self, text="\u2398").pack(side=tk.RIGHT)


class PropertiesFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        PropertyEntry(self).pack(fill=tk.X, pady=5)
        PropertyEntry(self).pack(fill=tk.X, pady=5)
        PropertyEntry(self).pack(fill=tk.X, pady=5)
