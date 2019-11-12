import re
import unittest
from http import HTTPStatus

from flask import url_for

from src import create_app, db
from src.gene.models import Gene


def _sort(data):
    if data:
        return sorted(data, key=lambda k: k['ensembl_stable_id'])
    else:
        return []


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
                    "species": "abc def",
                    "ensembl_stable_id": "ENSAP1111111111111",
                    "gene_name": "gene xxx",
                    "location": "MVNR11111111.1:111111-111111"
                },
                {
                    "species": "zwx abc",
                    "ensembl_stable_id": "ENSAP2222222222222",
                    "gene_name": "gene yyy",
                    "location": "MVNR22222222.2:222222-222222"
                },
                {
                    "species": "def ghij",
                    "ensembl_stable_id": "ENSAP3333333333333",
                    "gene_name": "gene zzz",
                    "location": "MVNR3333333.3:333333-333333"
                },
                {
                    "species": "def ghij",
                    "ensembl_stable_id": "ENSAP4444444444444",
                    "gene_name": "gene zzzxyz",
                    "location": "MVNR4444444.4:444444-444444"
                }
            ]
        }

    def test_search_by_name(self):
        self._helper_add_genes()
        partial_word = 'xyz'
        res = self.app.test_client().get(url_for('genes.genesresource',lookup=partial_word))
        expected = [gene for gene in self.data.get('results') if partial_word in gene['gene_name']]
        self.assertEqual(_sort(expected), _sort(res.json.get('results')))

    def _helper_add_genes(self):
        for item in self.data.get('results'):
            # print('inserting genge{0}'.format(item['ensembl_stable_id']))
            gene = Gene(item['ensembl_stable_id'],
                        item['species'],
                        item['gene_name'],
                        item['location'])
            self.db.session.add(gene)
        self.db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
        self.ctx.pop()


if __name__ == '__main__':
    unittest.main()
