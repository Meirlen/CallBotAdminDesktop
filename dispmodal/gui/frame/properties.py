from pathlib import Path
import tkinter as tk

import pyperclip


class PropertyLabel(tk.Label):
    color = "#F8F9FA"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("background", self.color)
        kwargs.setdefault("justify", tk.CENTER)

        super().__init__(*args, **kwargs)

        self._icon_copy = tk.PhotoImage(
            file=Path(__file__).parent.parent / "icons" / "copy.png"
        )

        tk.Button(
            self,
            command=self.copy,
            background=self.color,
            activebackground=self.color,
            image=self._icon_copy,
            relief=tk.FLAT,
            takefocus=0,
        ).pack(side=tk.RIGHT, padx=5)

    def copy(self):
        pyperclip.copy(self["text"])


class PropertiesFrame(tk.Frame):
    length = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.labels = [PropertyLabel(self) for _ in range(self.length)]

        for label in self.labels:
            label.pack(fill=tk.X, ipadx=100, pady=5, ipady=5)

    def set_values(self, *values):
        for label, value in zip(self.labels, values):
            label.configure(
                text=value
            )
