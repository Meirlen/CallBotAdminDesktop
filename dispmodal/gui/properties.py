import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tk_font

class PropertyEntry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", "Property.TEntry")
        kwargs.setdefault("justify", "center")
        kwargs.setdefault("font", tk_font.Font(size=12))

        super().__init__(*args, **kwargs)

        ttk.Button(self, text="\u2398").pack(side=tk.RIGHT)


class PropertiesFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        PropertyEntry(self).pack(fill=tk.X, pady=5, ipady=10)
        PropertyEntry(self).pack(fill=tk.X, pady=5, ipady=10)
        PropertyEntry(self).pack(fill=tk.X, pady=5, ipady=10)
