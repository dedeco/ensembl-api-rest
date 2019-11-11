
import marshmallow
from flask_marshmallow import Marshmallow

from . import gene_blueprint

from .models import Gene

ma = Marshmallow(gene_blueprint)


class GeneSchema(ma.Schema):
    class Meta:
        model = Gene

    gene_name = marshmallow.fields.String(attribute="display_label")
    ensembl_stable_id = marshmallow.fields.String(attribute="stable_id")
    location = marshmallow.fields.String(attribute="location")
    species = marshmallow.fields.String(attribute="species")
