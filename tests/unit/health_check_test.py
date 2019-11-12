import unittest
from http import HTTPStatus

import pytest

from flask import url_for


@pytest.mark.usefixtures('client_class')
class HealthCheckCase(unittest.TestCase):

    def setUp(self):
        self.response = self.client.get(url_for('genes.health_check'))

    def test_response_ok(self):
        self.assertEqual(HTTPStatus.OK, self.response.status_code)

    def test_api_health_check(self):
        self.response.json['results'][0]['output'] == 'Api running'


if __name__ == '__main__':
    unittest.main()
