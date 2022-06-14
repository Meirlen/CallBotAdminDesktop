from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tk_font

import pyperclip


class PropertyEntry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", "Property.TEntry")
        kwargs.setdefault("justify", "center")
        kwargs.setdefault("font", tk_font.Font(size=12))

        super().__init__(*args, **kwargs)

        self._icon_copy = tk.PhotoImage(file=Path(__file__).parent.parent / "icons" / "copy.png")

        ttk.Button(
            self,
            style="Copy.Property.TButton",
            image=self._icon_copy,
            takefocus=0,
            command=self.copy,
        ).pack(side=tk.RIGHT, padx=5)

    def copy(self):
        pyperclip.copy(self.get())


class PropertiesFrame(ttk.Frame):
    length = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.entries = [PropertyEntry(self) for _ in range(self.length)]

        for entry in self.entries:
            entry.pack(fill=tk.X, ipadx=100, pady=5, ipady=5)

    def set_values(self, *values):
        for entry, value in zip(self.entries, values):
            if value is None:
                value = ""

            entry.delete(0, tk.END)
            entry.insert(0, str(value))
