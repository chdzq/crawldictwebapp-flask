# encoding: utf-8

from webapp.exception import handle
from webapp import \
    app, \
    hook_api

if __name__ == '__main__':
    from core.mongo import Mongodb
    from webapp import current_config
    mongo = Mongodb(current_config.mongodb)
    app.run(debug=True)
