import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tk_msgbox
import logging
import queue

from .properties import PropertiesFrame
from .comment import CommentFrame
from .buttons import AcceptButton
from .style import STYLE
from dispmodal.storage import attach_listener


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self._start_storage_listener()

        self.attributes("-topmost", True)

        self.style = ttk.Style(self)
        self._configure_style()

        frame = ttk.Frame(self)

        self.properties_frame = PropertiesFrame(frame)
        self.properties_frame.pack(fill=tk.X)

        self.comment_frame = CommentFrame(frame)
        self.comment_frame.pack(fill=tk.X)

        self.accept_button = AcceptButton(frame)
        self.accept_button.pack(fill=tk.X, pady=20, ipady=10)

        frame.pack(fill=tk.X, padx=125, pady=35)

    def _start_storage_listener(self):
        self._hide()

        self.listener_queue = queue.Queue()
        attach_listener(self.listener_queue)

        self.current_doc = None
        self.after(100, self._poll_queue)

    def _configure_style(self):
        for selector, kw in STYLE["widgets"].items():
            self.style.configure(selector, **kw)
        self.config(**STYLE["root"])

    def _poll_queue(self):
        try:
            snapshot = self.listener_queue.get_nowait()
        except queue.Empty:
            pass
        else:
            self._process_snapshot(snapshot)

        self.after(100, self._poll_queue)

    def _process_snapshot(self, snapshot):
        try:
            docs = []

            for doc in snapshot[0]:
                try:
                    doc_status = doc.get("status")
                except Exception as e:
                    logging.warning(str(e))
                    continue

                if doc_status == "new":
                    docs.append({"id": doc.id} | doc.to_dict())

            if not docs:
                self._hide()
                return

            current_doc = docs[0]

            if self.current_doc is not None:
                for doc in docs:
                    if doc["id"] == self.current_doc["id"]:
                        current_doc = doc
                        break

            self.current_doc = current_doc

            self._show()

        except Exception as e:
            tk_msgbox.showerror("", str(e))

    def _show(self):
        try:
            self.properties_frame.set_values(
                self.current_doc.get("from"),
                self.current_doc.get("to"),
                self.current_doc.get("price"),
            )
            self.comment_frame.set_value(
                self.current_doc.get("user_comment", ""),
            )
        except Exception as e:
            logging.error("", exc_info=True)

        self.deiconify()

    def _hide(self):
        self.withdraw()
