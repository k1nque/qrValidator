from redis import Redis
import os
from json import loads
import re
from time import sleep

class Validator:
    def __init__(self):
        self.HOST = os.environ.get('REDIS_HOST')
        self.PORT = int(os.environ.get('REDIS_PORT'))
        self.SUBSCRIBE_KEY = os.environ.get('REDIS_SUBSCRIBE_KEY')
        self.PREV_BARCODE = "000000"
        self.subscribe()

    def validate_msg(self, msg):
        encoded_msg = loads(msg)
        if "qr" not in encoded_msg.keys():
            pass  # Unvalidated
        if "barcode" not in encoded_msg.keys():
            encoded_msg["barcode"] = self.PREV_BARCODE
        match = re.fullmatch(r"https:\/\/qrc\.ai\/\w+", encoded_msg["qr"])
        if not match:
            pass  # Unvalidated
        self.PREV_BARCODE = encoded_msg["barcode"]

    def subscribe(self):
        def event_handler(msg):
            print(msg)
            self.validate_msg()
        # sleep(1000)
        redis_server = Redis(host=self.HOST, port=self.PORT)
        pubsub = redis_server.pubsub()
        pubsub.psubscribe(**{self.SUBSCRIBE_KEY: event_handler})

        pubsub.run_in_thread(sleep_time=.01)


validator = Validator()
