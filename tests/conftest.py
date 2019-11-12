import pytest

from src import create_app
from src.gene.models import Gene


@pytest.yield_fixture(scope='class')
def some_gene():
    gene = Gene("ENSAPOG00000019081",
                "acanthochromis_polyacanthus",
                "tbpl2",
                "VNR01000308.1:147400-150913",
                "core")
    return gene


@pytest.fixture(scope='module')
def app():
    app = create_app('flask-test.cfg')
    return app


