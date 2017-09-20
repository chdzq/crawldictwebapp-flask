# encoding: utf-8

from enum import Enum, unique

@unique
class ARPAbetError(Enum):
    ipa_unable_convert_arpabet = 1
    unable_crawl_ipa = 2


@unique
class SystemError(Enum):
    server_maintenance = 999
    mongo_db = 100
    redis = 200
    request_param = 300


@unique
class OtherError(Enum):
    unknow = 999