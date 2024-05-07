from flask import Blueprint

newslang = Blueprint("newslang_api", __name__)

from . import views