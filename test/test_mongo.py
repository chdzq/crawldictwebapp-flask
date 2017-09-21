# encoding: utf-8
from unittest import TestCase
from core.mongo import Mongodb

class TestMongo(TestCase):
    def setUp(self):
        self.mongo = Mongodb({
            'host': 'localhost',
            'port': 27017,
            'username': '',
            'password': '',
            'database': 'test_db'
            })

    def test_save_update_delete_find(self):
        self.mongo.update(table_name="test", condition={"word": "1"}, update_data={"word": "1", "body": 2}, upsert=True)

        self.assertEqual(self.mongo.find_one(table_name="test", condition={"word": "1"}).get("body"), 2)

        self.mongo.delete(table_name="test", condition={"word": "1"})

        self.assertFalse(self.mongo.find_one(table_name="test", condition={"word": "1"}))

