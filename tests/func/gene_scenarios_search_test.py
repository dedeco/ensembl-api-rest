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
                    "species": "def xyz",
                    "ensembl_stable_id": "ENSAP3333333333333",
                    "gene_name": "gene zzz",
                    "location": "MVNR3333333.3:333333-333333"
                },
                {
                    "species": "def ghi",
                    "ensembl_stable_id": "ENSAP4444444444444",
                    "gene_name": "gene zzzxyz",
                    "location": "MVNR4444444.4:444444-444444"
                },
                {
                    "species": "def GHI",
                    "ensembl_stable_id": "ENSAP5555555555555",
                    "gene_name": "gene ZZZ",
                    "location": "MVNR5555555.5:555555-555555"
                }
            ]
        }
        self._helper_add_genes()

    def test_search_missing_parameters(self):
        res = self.app.test_client().get(url_for('genes.genesresource'))
        self.assertEqual(HTTPStatus.BAD_REQUEST, res.status_code)

    def test_search_by_gene_name(self):
        KEYWORD = 'xyz'
        res = self._get_genes(KEYWORD)
        expected = [gene for gene in self.data.get('results') if KEYWORD.casefold() in gene.get('gene_name').casefold()]
        self.assertEqual(_sort(expected), _sort(res.json.get('results')))

    def test_search_by_gene_name_and_species(self):
        GENE_KEYWORD = 'zzz'
        SPECIES_KEYWORD = 'ghi'
        res = self.app.test_client().get(url_for('genes.genesresource', lookup=GENE_KEYWORD, species=SPECIES_KEYWORD))

        expected = []
        for gene in self.data.get('results'):
            if GENE_KEYWORD.casefold() in gene.get('gene_name').casefold() and \
                    SPECIES_KEYWORD.casefold() in gene.get('species').casefold():
                expected.append(gene)
        self.assertEqual(_sort(expected), _sort(res.json.get('results')))

    def test_search_by_gene_name_less_three_chars(self):
        KEYWORD = 'x'
        res = self.app.test_client().get(url_for('genes.genesresource', lookup=KEYWORD))
        self.assertEqual(HTTPStatus.BAD_REQUEST, res.status_code)

    def test_search_by_gene_name_and_species_less_three_chars(self):
        GENE_KEYWORD = 'z'
        SPECIES_KEYWORD = 'g'
        res = self.app.test_client().get(url_for('genes.genesresource', lookup=GENE_KEYWORD, species=SPECIES_KEYWORD))
        self.assertEqual(HTTPStatus.BAD_REQUEST, res.status_code)

    def test_search_by_gene_name_using_special_chars(self):
        KEYWORD = 'ß€⨭'
        res = self._get_genes(KEYWORD)
        expected = [gene for gene in self.data.get('results') if KEYWORD.casefold() in gene.get('gene_name').casefold()]
        self.assertEqual(_sort(expected), _sort(res.json.get('results')))

    def test_search_by_gene_name_using_japanese_chars(self):
        KEYWORD = '昨夜のコンサート'
        res = self._get_genes(KEYWORD)
        expected = [gene for gene in self.data.get('results') if KEYWORD.casefold() in gene.get('gene_name').casefold()]
        self.assertEqual(_sort(expected), _sort(res.json.get('results')))

    def _get_genes(self, gene_name_lookup):
        return self.app.test_client().get(url_for('genes.genesresource', lookup=gene_name_lookup))

    def _helper_add_genes(self):
        for item in self.data.get('results'):
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
