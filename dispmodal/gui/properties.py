from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tk_font


class PropertyEntry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", "Property.TEntry")
        kwargs.setdefault("justify", "center")
        kwargs.setdefault("font", tk_font.Font(size=12))

        super().__init__(*args, **kwargs)

        self._icon_copy = tk.PhotoImage(file=Path(__file__).parent / "icons" / "copy.png")

        ttk.Button(
            self,
            style="Copy.Property.TButton",
            image=self._icon_copy,
            takefocus=0,
        ).pack(side=tk.RIGHT, padx=5)


class PropertiesFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        PropertyEntry(self).pack(fill=tk.X, pady=5, ipady=10)
        PropertyEntry(self).pack(fill=tk.X, pady=5, ipady=10)
        PropertyEntry(self).pack(fill=tk.X, pady=5, ipady=10)
