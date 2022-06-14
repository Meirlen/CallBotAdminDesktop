import tkinter as tk
import tkinter.messagebox as tk_msgbox
from pathlib import Path
import logging
import queue

from callbot.gui.frame import AppFrame
from callbot.storage import (
    attach_listener,
    get_all_docs,
    get_next_doc,
    accept_doc
)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self._start_storage_listener()

        self._app_icon = tk.PhotoImage(
            file=Path(__file__).parent / "icons" / "app.png"
        )
        self.iconphoto(False, self._app_icon)
        
        self.title("CallBot")
        self.attributes("-topmost", True)
        
        self.config(background="white")
        self.option_readfile(Path(__file__).parent / "style.cfg")

        self.frame = AppFrame(self)
        self.frame.pack(fill=tk.X, padx=125, pady=35)

        self.frame.accept_btn.config(command=self._accept)
        self.protocol("WM_DELETE_WINDOW", self._ignore)

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
            self._next()
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
                self.current_doc.get("phone"),
            )
            self.frame.comment.set_value(
                self.current_doc.get("user_comment", ""),
            )
        except Exception as e:
            logging.error("", exc_info=True)

        self.eval('tk::PlaceWindow . center')
        self.deiconify()

    def _hide(self):
        self.current_doc = None
        self.withdraw()

    def _accept(self):
        accept_doc(self.current_doc)

        self._next()

    def _ignore(self):
        if self.current_doc is not None:
            self.ignored_docs.add(self.current_doc["id"])

        self._next()

    def _next(self, doc_snapshots=None):
        if doc_snapshots is None:
            doc_snapshots = get_all_docs()

        doc = get_next_doc(doc_snapshots, self.current_doc, self.ignored_docs)

        if doc is None:
            self._hide()
        else:
            self._show(doc)
