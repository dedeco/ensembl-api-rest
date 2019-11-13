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
                            help='The partial query for gene name typed by the user, e.g. brc.')

        parser.add_argument('species',
                            help='The name of the target species, e.g. homo_sapiens.')

        args = parser.parse_args()

        q = db.session.query(Gene) \
            .filter(Gene.display_label.ilike('%{0}%'.format(args.get('lookup'))))

        if args.get('species'):
            q += q.filter(Gene.species.ilike('%{0}%'.format(args.get('species'))))

        genes = q.all()

        schema = GeneSchema(many=True)

        return {"results": schema.dump(
            genes
        )}, HTTPStatus.OK


gene_restfull.add_resource(GenesResource, "/gene")
