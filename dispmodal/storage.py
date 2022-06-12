from queue import Queue

from firebase_admin import initialize_app, credentials, firestore

_db = None


def get_db():
    global _db

    if _db is None:
        initialize_app(
            credentials.Certificate("transport-2f82d-firebase-adminsdk-2crxy-133469a4e3.json")
        )
        _db = firestore.client()

    return _db


def attach_listener(queue: Queue):
    return get_db().collection("orders").on_snapshot(
        lambda *args: queue.put(args)
    )
