import json

import pytest
import requests
from requests.exceptions import ConnectionError
from distutils import dir_util
from termci_api.app import app
from fastapi.testclient import TestClient


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
def datadir(tmpdir, pytestconfig):
    data_dir = pytestconfig.rootpath / 'tests/data'
    dir_util.copy_tree(str(data_dir), str(tmpdir))
    return tmpdir


@pytest.fixture(scope='session')
def neo4j_graph(docker_ip, docker_services):
    port = docker_services.port_for('fhir-neo4j', 7474)
    url = f'http://{docker_ip}:{port}'
    docker_services.wait_until_responsive(
        timeout=60.0, pause=0.1, check=lambda: is_responsive(url)
    )
    bolt_port = docker_services.port_for('fhir-neo4j', 7687)
    bolt_url = f'bolt://{docker_ip}:{bolt_port}'
    graph = Graph(bolt_url, auth=('neo4j', 'password'))
    yield graph


@pytest.fixture(scope='session')
def fhirbase(docker_ip, docker_services):
    port = docker_services.port_for('fhir-base', 5432)
    connection = psycopg2.connect(dbname='fhirbase', user='postgres', host=docker_ip, port=port)
    yield FHIRBase(connection)
