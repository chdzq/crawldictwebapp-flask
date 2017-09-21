# encoding: utf-8
from unittest import TestCase
from core.redis import Redis

class TestRedis(TestCase):

    def setUp(self):
        self.redis = Redis({'host': '127.0.0.1',
                            'port': 6379,
                            'db': 0,
                            'password': ''
                            })

    def test_save_update_delete(self):
        self.redis.set_data("1", "哈哈")
        self.assertEqual(self.redis.get_data("1"), "哈哈")
        self.assertFalse(self.redis.get_data("1") == "哈哈2")
        self.redis.delete("1")
        self.assertFalse(self.redis.get_data("1"))
