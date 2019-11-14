from http import HTTPStatus

from flask import url_for
from flask_restful import Api, Resource, reqparse

from src import db
from src.gene.models import Gene
from src.gene.schema import GeneSchema
from src.gene.utils import get_paginated_list, get_parameters_url, get_parsed_parameters
from . import gene_blueprint

gene_restfull = Api(gene_blueprint)


class GenesResource(Resource):

    def get(self):
        args = get_parsed_parameters(reqparse.RequestParser())

        q = db.session.query(Gene) \
            .filter(Gene.display_label.ilike('%{0}%'.format(args.get('lookup'))))

        if args.get('species'):
            q = q.filter(Gene.species.ilike('%{0}%'.format(args.get('species'))))

        genes = q.all()

        gene_schema = GeneSchema(many=True)

        return get_paginated_list(
            gene_schema,
            genes,
            url_for('genes.genesresource'),
            get_parameters_url(args),
            start=args.get('start'),
            limit=args.get('limit')
        ), HTTPStatus.OK


gene_restfull.add_resource(GenesResource, "/genes")
