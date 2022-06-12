import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tk_msgbox
import logging
import queue

from dispmodal.gui.frame import AppFrame
from dispmodal.gui.style import STYLE
from dispmodal.storage import attach_listener


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self._start_storage_listener()

        self._configure_style()

        self.frame = AppFrame(self)
        self.frame.pack(fill=tk.X, padx=125, pady=35)

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
        self.ignored_docs_ids = set()

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
        try:
            doc_snapshots, changes, _ = snapshot

            self.ignored_docs_ids -= {change.document.id for change in changes}

            docs = []

            for doc in doc_snapshots:
                if doc.id in self.ignored_docs_ids:
                    continue

                try:
                    doc_status = doc.get("status")
                except Exception as e:
                    logging.warning("", exc_info=True)
                    continue

                if doc_status != "new":
                    continue

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

    def _ignore(self):
        if self.current_doc is not None and "id" in self.current_doc:
            self.ignored_docs_ids.add(self.current_doc["id"])

        self._hide()
