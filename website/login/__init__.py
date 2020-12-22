from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix = '/', template_folder = 'templates')

from .login import *