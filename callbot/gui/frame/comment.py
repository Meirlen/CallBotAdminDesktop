import tkinter as tk
import tkinter.font as tk_font


class CommentFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        frame = tk.Frame(self)
        tk.Label(frame, text="Комментарий:").pack(side=tk.LEFT)

        self.value_label = tk.Label(frame, font=tk_font.Font(weight="bold"))
        self.value_label.pack(side=tk.LEFT)

        frame.pack()

    def set_value(self, value):
        self.value_label.config(text=value)
