from flask import Flask
import logging

logging.basicConfig(level="INFO", format='[%(levelname)s] %(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


def create_app():
    """
    creation of application using blueprint
    """
    # Flask app initialization
    app = Flask(__name__)


    # for CORs: adding all the headers
    @app.after_request
    def add_headers(response):
        response.headers.add("Content-Type", "application/json")
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Methods", "PUT, GET, POST, DELETE, OPTIONS, PATCH"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization"
        )
        response.headers.add(
            "Access-Control-Expose-Headers",
            "Content-Type,Content-Length,Authorization,X-Pagination",
        )
        return response

    # registering the APIs for blueprint
    with app.app_context():
        from .newslang import newslang

        app.register_blueprint(newslang,  url_prefix="/api/v1")
        return app