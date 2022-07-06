from redis import Redis
import os
from json import loads, dumps
from re import fullmatch


class Validator:
    def __init__(self):
        self._host = os.environ.get('REDIS_HOST')
        self._port = int(os.environ.get('REDIS_PORT'))
        self._subscribe_key = os.environ.get('REDIS_SUBSCRIBE_KEY')
        self._approved_publish_key = os.environ.get("REDIS_APPROVED_PUBLISH_KEY")
        self._unapproved_publish_key = os.environ.get("REDIS_UNAPPROVED_PUBLISH_KEY")
        self.prev_barcode = "000000"
        self.redis_server = Redis(host=self._host, port=self._port)
        self.subscribe()

    def validate_msg(self, msg: dict):
        encoded_msg: dict = loads(msg["data"])

        if "qr" not in encoded_msg.keys():
            print(f"no qr in json: {dumps(encoded_msg)}")
            self.redis_server.publish(self._unapproved_publish_key, dumps(encoded_msg))
            return

        if "barcode" not in encoded_msg.keys() or encoded_msg["barcode"] == "":
            print(f"no barcode: {dumps(encoded_msg)}")
            encoded_msg["barcode"] = self.prev_barcode
            print(f"barcoded added: {dumps(encoded_msg)}")

        match = fullmatch(r"https://qrc\.ai/\w+", encoded_msg["qr"])
        if not match:
            print(f"unmatched qr: {dumps(encoded_msg)}")
            self.redis_server.publish(self._unapproved_publish_key, dumps(encoded_msg))
            return

        self.prev_barcode: str = encoded_msg["barcode"]
        print(f"approved: {dumps(encoded_msg)}")
        self.redis_server.publish(self._approved_publish_key, dumps(encoded_msg))

    def subscribe(self):
        pubsub = self.redis_server.pubsub()
        pubsub.subscribe(**{self._subscribe_key: self.validate_msg})
        pubsub.run_in_thread(sleep_time=.01)


if __name__ == "__main__":
    validator = Validator()
