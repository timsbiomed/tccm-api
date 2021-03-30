from fastapi import APIRouter, Response, Request, Depends, HTTPException

from urllib.parse import unquote

from termci_api.db.termci_graph import TermCIGraph
from termci_api.utils import decode_uri

router = APIRouter(
    prefix='/conceptsystems',
    tags=['ConceptSystems'],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


def build_jsonld_link_header(resource):
    uri = f'/static/jsonld/jsonld_10/context/{resource}.context.jsonld'
    params = {
        'rel': 'http://www.w3.org/ns/json-ld#context',
        'type': 'application/ld+json'
    }
    return f'<{uri}>; ' + '; '.join([f'{k}="{v}"' for k, v in params.items()])


@router.get('/{uri}')
def get_concept_systems(uri: str, request: Request, response: Response):
    graph: TermCIGraph = request.app.state.graph
    orig_uri = uri
    uri = decode_uri(uri)
    records = graph.get_concept_systems(unquote(uri))
    if not records:
        raise HTTPException(status_code=404, detail=f"ConceptSystem {orig_uri} not found.")
    node = records[0]
    response.headers['Link'] = build_jsonld_link_header('termci_schema')
    return node


