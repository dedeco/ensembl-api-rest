from flask import Blueprint

gene_blueprint = Blueprint('gene', __name__)

from . import health_check
from . import resources
