# encoding: utf-8

from webapp import api
from webapp.exception import handle

if __name__ == '__main__':
    from webapp import mongo
    mongo.output_rows("dict")
    from webapp import app
    app.run(debug=True)
