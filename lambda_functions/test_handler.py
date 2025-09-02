import os
import unittest
import sys
import json
import uuid
from unittest.mock import MagicMock

print(sys.modules)
sys.modules['boto3'] = MagicMock()
os.environ['DYNAMODB_TABLE'] = "test_table"


class MyTestCase(unittest.TestCase):
    def test_create_customer(self):
        from handler import create_customer
        event = {
            'body': '{"firstname":"lakshman", "lastname":"kosaraju"}'
        }
        customer = create_customer(event, None)
        json_body = json.loads(customer['body'])
        expected = {"firstname":"lakshman", "lastname":"kosaraju"}
        parsed_uuid = uuid.UUID(json_body["item"]["id"])
        self.assertEqual(customer['statusCode'], 200)
        self.assertEqual(json_body["item"]["firstname"],expected["firstname"])
        self.assertEqual(json_body["item"]["lastname"],expected["lastname"])
        self.assertEqual(str(parsed_uuid),json_body["item"]["id"])# add assertion here


if __name__ == '__main__':
    unittest.main()
