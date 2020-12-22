from flask import Blueprint

problem_bp = Blueprint('problem', __name__, url_prefix = '/', template_folder = 'templates')

from .problem import *