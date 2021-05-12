import json

import pytest
import requests
from requests.exceptions import ConnectionError
from distutils import dir_util

from fastapi.testclient import TestClient
from tccm_api.app import app
from tccm_api.db.tccm_graph import TccmGraph
from tccm_api.config import get_settings, Settings


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def data_dir(tmp_dir, pytestconfig):
    data_dir = pytestconfig.rootpath / 'tests/data'
    dir_util.copy_tree(str(data_dir), str(tmp_dir))
    return tmp_dir


@pytest.fixture(scope='session')
def termci_graph(docker_ip, docker_services):
    settings = get_settings()
    url = f"http://{settings.neo4j_host}:{settings.neo4j_http_port}"
    docker_services.wait_until_responsive(
        timeout=60.0, pause=0.1, check=lambda: is_responsive(url)
    )
    graph = TccmGraph()
    yield graph


@pytest.fixture
def app():
    yield app
