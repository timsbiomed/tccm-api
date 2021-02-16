import json

import pytest
import requests
from fastapi import FastAPI
from requests.exceptions import ConnectionError
from distutils import dir_util

from starlette.staticfiles import StaticFiles

from fastapi.testclient import TestClient
from termci_api.app import app
from termci_api.db.termci_graph import TermCIGraph
from termci_api.config import get_settings, Settings


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return pytestconfig.rootpath / 'docker-compose.yml'

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
    #port = docker_services.port_for('test-termci-neo4j', 7474)
    #url = f'http://{docker_ip}:{port}'
    settings = get_settings()
    url = f"http://{settings.neo4j_host}:{settings.neo4j_http_port}"
    docker_services.wait_until_responsive(
        timeout=60.0, pause=0.1, check=lambda: is_responsive(url)
    )
    #bolt_port = docker_services.port_for('test-termci-neo4j', 7687)
    bolt_url = f'bolt://{settings.neo4j_host}:{settings.neo4j_bolt_port}'
    graph = TermCIGraph()
    yield graph


@pytest.fixture
def app():
    yield app
