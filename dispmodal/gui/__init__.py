import tkinter as tk
import tkinter.ttk as ttk

from .properties import PropertiesFrame
from .comment import CommentFrame
from .buttons import AcceptButton
from .style import STYLE


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.attributes("-topmost", True)

        self.style = ttk.Style(self)
        self._configure_style()

        frame = ttk.Frame(self)

        PropertiesFrame(frame).pack(fill=tk.X)
        CommentFrame(frame).pack(fill=tk.X)
        AcceptButton(frame).pack(fill=tk.X, pady=20, ipady=10)

        frame.pack(fill=tk.X, padx=125, pady=35)

    def _configure_style(self):
        for selector, kw in STYLE["widgets"].items():
            self.style.configure(selector, **kw)

        self.config(**STYLE["root"])
