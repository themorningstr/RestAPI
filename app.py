from flask import Flask
from flask_smorest import Api
from resources import ItemBluePrint
from resources  import StoreBluePrint
from resources import  TagBluePrint
from db import db
import models
import os

def create_app(db_url=None):
    
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.init_app(app)


    api = Api(app)

    def create_tables():
        with app.app_context():
            db.create_all()
            print("Tables created!")

    app._got_first_request = False

    @app.before_request
    def before_request():
        if not app._got_first_request:
            create_tables()
            app._got_first_request = True

    api.register_blueprint(ItemBluePrint)
    api.register_blueprint(StoreBluePrint)
    api.register_blueprint(TagBluePrint)


    return app




# if __name__ == '__main__':
#     app = create_app()
    # app.run(debug=True)
