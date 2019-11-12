import pytest
import unittest

from src import create_app, db
from src.gene.models import Gene


@pytest.mark.usefixtures('client_class')
class GeneModelCase(unittest.TestCase):

    def setUp(self):
        self.flask_app = create_app('flask-test.cfg')
        with self.flask_app.app_context():
            db.create_all()

    def test_add_gene(self):
        expected = Gene("ENSAPOG00000019081",
                    "acanthochromis_polyacanthus",
                    "tbpl2",
                    "VNR01000308.1:147400-150913",
                    "core")
        db.session.add(expected)
        persisted = db.session.query(Gene).get(expected.stable_id)
        self.assertEqual(expected, persisted)

    def tearDown(self):
        with self.flask_app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
