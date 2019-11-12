from http import HTTPStatus

from flask_restful import Api, Resource, reqparse

from src import db
from src.gene.models import Gene
from src.gene.schema import GeneSchema
from . import gene_blueprint

gene_restfull = Api(gene_blueprint)

parser = reqparse.RequestParser()


class GenesResource(Resource):

    def get(self):
        parser.add_argument('lookup',
                            required=True,
                            help='The partial query for gene name typed by the user, e.g. brc')
        args = parser.parse_args()

        all_genes = db.session.query(Gene)\
            .filter(Gene.display_label.
                    ilike('%{0}%'.format(args['lookup'])))\
            .all()

        schema = GeneSchema(many=True)
        
        return {"results": schema.dump(
            all_genes
        )}, HTTPStatus.OK


gene_restfull.add_resource(GenesResource, "/gene")
