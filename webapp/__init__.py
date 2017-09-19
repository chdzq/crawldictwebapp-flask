#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
app = Flask(__name__)

from config import current_config
from core.mongo import Mongodb
mongo = Mongodb(current_config.mongodb)


from core.redis import Redis
redis = Redis(current_config.redis)
