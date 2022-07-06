import unittest
from redis import Redis
import json
from time import sleep

if __name__ == "__main__":
    unittest.main()


class TestQrValidator(unittest.TestCase):
    def test_blank_barcode(self):
        _publish_key = "message_to_approve"
        _approved_key = "approved_messages"
        _unapproved_key = "unapproved_messages"
        r = Redis("localhost", 6379)
        pubsub = r.pubsub()

        qr = "https://qrc.ai/mCgsWN8cnTqz"
        barcode = ""
        self.answer = False

        def event_handler(msg: str):
            encoded_msg = json.loads(msg)
            if encoded_msg["data"]["qr"] == qr and encoded_msg["data"]["barcode"] == "000000":
                self.answer = True
            else:
                self.answer = False

        pubsub.subscribe(**{_approved_key: event_handler})

        test_msg = {"qr": qr, "barcode": barcode}
        r.publish(_publish_key, json.dumps(test_msg))
        sleep(10)
        self.assertEqual(self.answer, True)
        pubsub.unsubscribe()

    def test_blank_qr(self):
        PUBLISH_KEY = "message_to_approve"
        APPROVED_KEY = "approved_messages"
        UNAPPROVED_KEY = "unapproved_messages"
        r = Redis("localhost", 6379)
        pubsub = r.pubsub()

        qr = ""
        barcode = "012345"
        test_msg = {"qr": qr, "barcode": barcode}
        self.answer = False

        def event_handler(msg: str):
            encoded_msg = json.loads(msg)
            if encoded_msg["data"] == test_msg:
                self.answer = True

        pubsub.subscribe(**{UNAPPROVED_KEY: event_handler})
        r.publish(PUBLISH_KEY, json.dumps(test_msg))
        sleep(10)
        self.assertEqual(self.answer, True)
        pubsub.unsubscribe()

    def test_incorrect_qr(self):
        PUBLISH_KEY = "message_to_approve"
        APPROVED_KEY = "approved_messages"
        UNAPPROVED_KEY = "unapproved_messages"
        r = Redis("localhost", 6379)
        pubsub = r.pubsub()

        qr = "https://docs.python.org/3/library/unittest.html"
        barcode = "012345"
        self.answer = False

        def event_handler(msg: str):
            encoded_msg = json.loads(msg)
            if encoded_msg["data"] == test_msg:
                self.answer = True

        pubsub.subscribe(**{UNAPPROVED_KEY: event_handler})
        test_msg = {"qr": qr, "barcode": barcode}
        r.publish(PUBLISH_KEY, json.dumps(test_msg))
        sleep(10)
        pubsub.unsubscribe()
        self.assertEqual(self.answer, True)
