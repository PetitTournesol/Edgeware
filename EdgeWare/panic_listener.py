import asyncio
from threading import Event


PORT = 58008
ADDRESS = ("localhost", 58008)
AUTH_KEY = b"16s0g64sd1g8sd4g6qs1g431sqdg1dauigssdgsd9g"


def listen(event: Event):
    import logging
    from multiprocessing.connection import Listener

    with Listener(ADDRESS, authkey=AUTH_KEY) as listener:
        with listener.accept() as conn:
            print("connection accepted from", listener.last_accepted)
            while not event.is_set():
                msg = conn.recv()
                if msg == "panic_close":
                    logging.info("Closed after listening to 'panic' packet")
                    event.set()
                    break
