import tkinter as tk

from .properties import PropertiesFrame
from .comment import CommentFrame
from .buttons import AcceptButton


class AppFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.properties = PropertiesFrame(self, size=4)
        self.properties.pack(fill=tk.X)

        self.comment = CommentFrame(self)
        self.comment.pack(fill=tk.X)

        self.accept_btn = AcceptButton(self)
        self.accept_btn.pack(fill=tk.X, pady=20, ipady=10)
