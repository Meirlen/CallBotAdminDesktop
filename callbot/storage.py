from queue import Queue
import logging

from firebase_admin import initialize_app, credentials, firestore

from .config import CWD

_db = None


def get_db():
    global _db

    if _db is None:
        initialize_app(
            credentials.Certificate(CWD / "serviceAccount.json")
        )
        _db = firestore.client()

    return _db


def attach_listener(queue: Queue):
    return get_db().collection("orders").on_snapshot(
        lambda *args: queue.put(args)
    )


def snapshots2doc(doc_snapshots, ignored_docs):
    for doc in doc_snapshots:
        if doc.id in ignored_docs:
            continue

        try:
            doc_status = doc.get("status")
        except Exception as e:
            logging.error(e, exc_info=True)
            continue

        if doc_status != "new":
            continue

        yield (
            {"id": doc.id, **doc.to_dict()}
        )


def get_next_doc(doc_snapshots, current_doc, ignored_docs):
    docs = list(snapshots2doc(doc_snapshots, ignored_docs))

    if not docs:
        return None

    next_doc = docs[0]

    if current_doc is not None:
        for doc in docs:
            if doc["id"] == current_doc["id"]:
                next_doc = doc
                break

    return next_doc


def accept_doc(doc):
    col_ref = get_db().collection("orders")

    doc_ref = col_ref.document(doc["id"])
    doc_ref.update({"status": "accept"})


def get_all_docs():
    col_ref = get_db().collection("orders")

    return list(col_ref.stream())
