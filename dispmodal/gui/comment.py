import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tk_font


class CommentFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        frame = ttk.Frame(self)
        ttk.Label(frame, text="Комментарий:").pack(side=tk.LEFT)
        ttk.Label(frame, text="not", font=tk_font.Font(size=12, weight="bold")).pack(side=tk.LEFT)
        frame.pack()
