# TODO: Add descriptions for endpoints
from fastapi import APIRouter, Response, Request, Depends, HTTPException

from urllib.parse import unquote

from tccm_api.enums import ConceptSystemKeyName, SearchModifier
from tccm_api.db.tccm_graph import TccmGraph
from tccm_api.utils import decode_uri, build_jsonld_link_header

router = APIRouter(
    prefix='/conceptsystems',
    tags=['ConceptSystems'],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get('')
def get_concept_systems(key: ConceptSystemKeyName, value: str, modifier: SearchModifier, request: Request, response: Response):
    graph: TccmGraph = request.app.state.graph
    records = graph.get_concept_systems_by_value(key, value, modifier)
    if not records:
        raise HTTPException(status_code=404, detail=f"ConceptSystem {key}={value}|{modifier} not found.")
    response.headers['Link'] = build_jsonld_link_header(str(request.base_url) + request.scope.get("root_path"), 'termci_schema')
    return records


@router.get('/{prefix}')
def get_concept_reference_by_id(prefix: str, request: Request, response: Response):
    graph: TccmGraph = request.app.state.graph
    records = graph.get_concept_systems_by_value(ConceptSystemKeyName.prefix, prefix, SearchModifier.equals)
    if not records:
        raise HTTPException(status_code=404, detail=f"ConceptReference prefix={prefix} not found.")
    response.headers['Link'] = build_jsonld_link_header(str(request.base_url) + request.scope.get("root_path"), 'termci_schema')
    return records[0]


