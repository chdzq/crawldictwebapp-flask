#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
app = Flask(__name__)

from config import current_config
from webapp.mongo import Mongodb
mongo = Mongodb(current_config.DB_MONGO)