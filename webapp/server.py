# encoding: utf-8

from webapp.exception import handle
from webapp import \
    app, \
    hook_api

if __name__ == '__main__':
    from webapp import mongo
    mongo.output_rows("dict")
    app.run(debug=True)
