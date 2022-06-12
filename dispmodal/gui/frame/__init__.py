import tkinter as tk
import tkinter.ttk as ttk

from .properties import PropertiesFrame
from .comment import CommentFrame
from .buttons import AcceptButton


class AppFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.properties = PropertiesFrame(self)
        self.properties.pack(fill=tk.X)

        self.comment = CommentFrame(self)
        self.comment.pack(fill=tk.X)

        self.accept_btn = AcceptButton(self)
        self.accept_btn.pack(fill=tk.X, pady=20, ipady=10)
