from fastapi import APIRouter, Response, Request, Depends, HTTPException

from urllib.parse import unquote

from termci_api.db.termci_graph import TermCIGraph
from termci_api.utils import decode_uri
from termci_api.enums import ConceptReferenceKeyName, SearchModifier

router = APIRouter(
    prefix='/conceptreferences',
    tags=['ConceptReferences'],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


def build_jsonld_link_header(base: str, resource: str):
    uri = f'{base}static/jsonld/jsonld_10/context/{resource}.context.jsonld'
    params = {
        'rel': 'http://www.w3.org/ns/json-ld#context',
        'type': 'application/ld+json'
    }
    return f'<{uri}>; ' + '; '.join([f'{k}="{v}"' for k, v in params.items()])


@router.get('')
def get_concept_references(key: ConceptReferenceKeyName, value: str, modifier: SearchModifier, request: Request, response: Response):
    graph: TermCIGraph = request.app.state.graph
    new_value = value
    if key == ConceptReferenceKeyName.uri:
        new_value = unquote(value)
    elif key == ConceptReferenceKeyName.curie:
        new_value = unquote(decode_uri(value))
    records = graph.get_concept_references_by_value(key, new_value, modifier)
    if not records:
        raise HTTPException(status_code=404, detail=f"ConceptReference {key}={value}|modifier not found.")
    response.headers['Link'] = build_jsonld_link_header(str(request.base_url) + request.scope.get("root_path"), 'termci_schema')
    return records
