import unittest
import pytest

from flask import url_for


@pytest.mark.usefixtures('client_class')
class HealthCheckCase(unittest.TestCase):
    def test_api_health_check(self):
        res = self.client.get(url_for('gene.health_check'))
        assert res.json['results'][0]['output'] == 'Api running'


if __name__ == '__main__':
    unittest.main()
