from flask import Blueprint

forum_bp = Blueprint('forum', __name__, url_prefix = '/', template_folder = 'templates',\
    static_folder = 'static')

from .Display import *