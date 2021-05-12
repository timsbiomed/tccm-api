from tccm_api.namespaces import NAMESPACES
from tccm_api.utils import curie_to_uri


def test_curie_to_uri_ncit():
    curie = "NCIT:C7227"
    uri = curie_to_uri(curie, NAMESPACES)
    assert uri == "http://purl.obolibrary.org/obo/NCIT_C7227"


def test_curie_to_uri_icdo3m():
    curie = "ICDO3M:800"
    uri = curie_to_uri(curie, NAMESPACES)
    assert uri == "https://ontologies-r.us/ontology/ICD-O-3-M/800"


def test_curie_to_uri_uri():
    curie = "https://ontologies-r.us/ontology/ICD-O-3-M/800"
    uri = curie_to_uri(curie, NAMESPACES)
    assert uri == "https://ontologies-r.us/ontology/ICD-O-3-M/800"
