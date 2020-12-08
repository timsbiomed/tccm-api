from fastapi import APIRouter
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


@router.get('/{uri}')
def get_concepts(uri: str):
    uri = decode_uri(uri)
    node = tccm_graph.get_concept(unquote(uri))
    if node is not None:
        node['@context'] = '/static/contexts/concept.context.jsonld'
        node['@type'] = 'skos:Concept'
        node['@id'] = node.pop('uri')
    return node


