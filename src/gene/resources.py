from http import HTTPStatus

from flask_restful import Api, Resource

from src import db
from src.gene.models import Gene
from src.gene.schema import GeneSchema
from . import gene_blueprint

gene_restfull = Api(gene_blueprint)


class GenesResource(Resource):

    def get(self):
        all_genes = db.session.query(Gene).all()
        print(all_genes)
        schema = GeneSchema(many=True)
        return {"results": schema.dump(
            all_genes
        )}, HTTPStatus.OK


gene_restfull.add_resource(GenesResource, "/gene")
