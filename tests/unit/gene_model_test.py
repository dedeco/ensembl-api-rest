import unittest

from src.gene.models import Gene


class GeneModelCase(unittest.TestCase):
    def setUp(self):
        new_gene = Gene("id",
                        "species 1",
                        "name 1",
                        "location 1",
                        "core")

        self.test_gene = new_gene

    def test_create_gene(self):
        self.assertIsInstance(self.test_gene, Gene)

    def test_new_gene(self):
        self.assertTrue(self.test_gene.stable_id == "id")
        self.assertTrue(self.test_gene.species == "species 1")
        self.assertTrue(self.test_gene.display_label == "name 1")
        self.assertTrue(self.test_gene.location == "location 1")
        self.assertTrue(self.test_gene.db == "core")


if __name__ == '__main__':
    unittest.main()
