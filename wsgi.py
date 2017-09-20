# encoding: utf-8

from webapp.server import app

if __name__ == "__main__":
    from webapp import mongo
    mongo.output_rows("dict")
    app.run(debug=True)