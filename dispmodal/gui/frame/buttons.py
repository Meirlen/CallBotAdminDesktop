import tkinter as tk
import tkinter.ttk as ttk


class AcceptButton(ttk.Button):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", "Accept.TButton")
        kwargs.setdefault("text", "Применить")
        kwargs.setdefault("takefocus", 0)

        super().__init__(*args, **kwargs)
