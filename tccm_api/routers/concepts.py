from fastapi import APIRouter, Response, Request

from tccm_api.config import neo4j_graph
from tccm_api.db.tccm_graph import TccmGraph
from urllib.parse import unquote

from tccm_api.utils import decode_uri

router = APIRouter(
    prefix='/concepts',
    tags=['Concepts'],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

tccm_graph = TccmGraph(neo4j_graph())


def build_jsonld_link_header(resource):
    uri = f'/static/contexts/{resource}.context.jsonld'
    params = {
        'rel': 'http://www.w3.org/ns/json-ld#context',
        'type': 'application/ld+json'
    }
    return f'<{uri}>; ' + '; '.join([f'{k}="{v}"' for k, v in params.items()])


@router.get('/{uri}')
def get_concepts(uri: str, response: Response):
    uri = decode_uri(uri)
    node = tccm_graph.get_concept(unquote(uri))
    if node is not None:
        node['type'] = 'skos:Concept'
    response.headers['Link'] = build_jsonld_link_header('concept')
    return node


