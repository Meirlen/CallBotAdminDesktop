from itertools import zip_longest
from pathlib import Path
import tkinter as tk

import pyperclip


class PropertiesFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        try:
            size = kwargs.pop("size")
        except KeyError:
            raise ValueError("`size` kwarg is not specified")

        self.size = size

        super().__init__(*args, **kwargs)

        self.labels = []
        self._build_labels()

    def _build_labels(self):
        for _ in range(self.size):
            label = PropertyLabel(self)
            label.pack(fill=tk.X, ipadx=100, pady=5, ipady=5)

            self.labels.append(label)

    def set_values(self, *values):
        for label, value in zip_longest(self.labels, values):
            label.configure(
                text=value
            )


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
            takefocus=0,
        ).pack(side=tk.RIGHT, padx=5)

    def copy(self):
        pyperclip.copy(self["text"])
