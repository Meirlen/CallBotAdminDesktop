import tkinter as tk


class AcceptButton(tk.Button):
    def __init__(self, *args, **kwargs):
        for prefix in ("", "active"):
            kwargs.setdefault(prefix + "background", "#0071FE")

        for prefix in ("", "active"):
            kwargs.setdefault(prefix + "foreground", "white")

        kwargs.setdefault("text", "Применить")
        
        super().__init__(*args, **kwargs)
