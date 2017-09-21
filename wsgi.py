# encoding: utf-8

from webapp.server import app

if __name__ == "__main__":
    from core.mongo import Mongodb
    from webapp import current_config
    mongo = Mongodb(current_config.mongodb)
    mongo.output_rows("cmudict")
    app.run(debug=True)