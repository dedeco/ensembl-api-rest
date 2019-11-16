from http import HTTPStatus

from flask import url_for
from flask_restful import Api, Resource, reqparse

from src import db, cache
from src.gene.models import Gene
from src.gene.schema import GeneSchema
from src.gene.utils import get_paginated_list, get_parameters_url, get_parsed_parameters, make_cache_key
from . import gene_blueprint

gene_restfull = Api(gene_blueprint)


class GenesResource(Resource):

    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        Get the genes. The entry point accepts a string as parameter and
        return the list of matching genes in our database.

        Parameters
        ----------
        lookup : str
            display_name - the name of the gene. The partial query typed
            by the user, e.g. brc
        species : str
            species - the name of the species to which the gene belongs.
            The name of the target species, e.g. homo_sapiens (not mandatory)

        Returns
        -------
        The server should return something like this:
         {
             "start": 1,
             "limit": 3,
             "count": 4,
             "previous": "",
             "next": "/api/v1/genes?start=4&limit=2&lookup=brc&species=sapiens",
             "results": [
                 {
                     "species": "homo_sapiens",
                     "ensembl_stable_id": "ENSG00000012048",
                     "gene_name": "BRCA1",
                     "location": "17:43044295-43170245"
                 },
                 {
                     "species": "homo_sapiens",
                     "ensembl_stable_id": "ENSG00000185515",
                     "gene_name": "BRCC3",
                     "location": "X:155071420-155123074"
                 }
             ]
         }
        """

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
