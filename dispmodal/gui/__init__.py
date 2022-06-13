import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tk_msgbox
import logging
import queue

from dispmodal.gui.frame import AppFrame
from dispmodal.gui.style import STYLE
from dispmodal.storage import attach_listener, get_next_doc, accept_doc


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self._start_storage_listener()

        self._configure_style()

        self.frame = AppFrame(self)
        self.frame.pack(fill=tk.X, padx=125, pady=35)

        self.frame.accept_btn.config(command=self._accept)
        self.protocol("WM_DELETE_WINDOW", self._ignore)

    def _configure_style(self):
        self.style = ttk.Style(self)

        for selector, kw in STYLE["widgets"].items():
            self.style.configure(selector, **kw)
        self.config(**STYLE["root"])

        self.attributes("-topmost", True)

    def _start_storage_listener(self):
        self._hide()

        self.listener_queue = queue.Queue()
        attach_listener(self.listener_queue)

        self.current_doc = None
        self.ignored_docs = set()

        self.after(100, self._poll_queue)

    def _poll_queue(self):
        try:
            snapshot = self.listener_queue.get_nowait()
        except queue.Empty:
            pass
        else:
            self._process_snapshot(snapshot)

        self.after(100, self._poll_queue)

    def _process_snapshot(self, snapshot):
        doc_snapshots, changes, _ = snapshot

        try:
            self.ignored_docs -= {change.document.id for change in changes}

            doc = get_next_doc(doc_snapshots, self.current_doc, self.ignored_docs)

            if doc is None:
                self._hide()
            else:
                self._show(doc)
        except Exception as e:
            logging.error(e, exc_info=True)
            tk_msgbox.showerror(message=str(e))

    def _show(self, doc):
        self.current_doc = doc

        try:
            self.frame.properties.set_values(
                self.current_doc.get("from"),
                self.current_doc.get("to"),
                self.current_doc.get("price"),
            )
            self.frame.comment.set_value(
                self.current_doc.get("user_comment", ""),
            )
        except Exception as e:
            logging.error("", exc_info=True)

        self.deiconify()

    def _hide(self):
        self.current_doc = None
        self.withdraw()

    def _accept(self):
        accept_doc(self.current_doc)
        self._hide()

    def _ignore(self):
        if self.current_doc is not None:
            self.ignored_docs.add(self.current_doc["id"])

        self._hide()
