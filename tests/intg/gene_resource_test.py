import unittest
from http import HTTPStatus

from flask import url_for

from src import create_app, db
from src.gene.models import Gene


class GeneResourceCase(unittest.TestCase):

    def setUp(self):
        self.db = db
        self.app = create_app('flask-test.cfg')
        self.client = self.app.test_client()
        with self.app.app_context():
            self.db.drop_all()
            self.db.create_all()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.data = {
            "results": [
                {
                    "species": "acanthochromis_polyacanthus",
                    "ensembl_stable_id": "ENSAPOG00000019081",
                    "gene_name": "tbpl2 abc",
                    "location": "MVNR01000308.1:147400-150913"
                },
                {
                    "species": "acanthochromis_polyacanthus",
                    "ensembl_stable_id": "ENSAPOG00000024458",
                    "gene_name": "tbr1b abc",
                    "location": "MVNR01000044.1:444385-449064"
                },
                {
                    "species": "acanthochromis_polyacanthus",
                    "ensembl_stable_id": "ENSAPOG00000017352",
                    "gene_name": "tbrg1 abc",
                    "location": "MVNR01000378.1:502653-510844"
                }
            ]
        }

    def test_request_get_should_response_ok(self):
        res = self.app.test_client().get(url_for('genes.genesresource', lookup='xpz'))
        self.assertEqual(HTTPStatus.OK, res.status_code)

    def test_request_get_should_response_some_gene_data(self):
        for item in self.data['results']:
            gene = Gene(item['ensembl_stable_id'],
                        item['species'],
                        item['gene_name'],
                        item['location'])
            self.db.session.add(gene)
        self.db.session.commit()
        res = self.app.test_client().get(url_for('genes.genesresource', lookup='abc'))
        self.maxDiff = None
        self.assertEqual(sorted(res.json['results'], key=lambda k: k['ensembl_stable_id'])
                         , sorted(self.data['results'], key=lambda k: k['ensembl_stable_id']))

    def test_request_post_should_returns_not_allowed(self):
        res = self.app.test_client().post(url_for('genes.genesresource'))
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, res.status_code)

    def test_request_patch_should_returns_not_allowed(self):
        res = self.app.test_client().patch(url_for('genes.genesresource'))
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, res.status_code)

    def test_request_put_should_returns_not_allowed(self):
        res = self.app.test_client().put(url_for('genes.genesresource'))
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, res.status_code)

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
        self.ctx.pop()


if __name__ == '__main__':
    unittest.main()
