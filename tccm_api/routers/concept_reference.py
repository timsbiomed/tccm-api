from typing import Optional, Union, List

from fastapi import APIRouter, Response, Request, Depends, HTTPException

from urllib.parse import unquote

from pydantic.main import BaseModel

from tccm_api.db.tccm_graph import TccmGraph
from tccm_api.utils import curie_to_uri, build_jsonld_link_header
from tccm_api.enums import ConceptReferenceKeyName, SearchModifier

router = APIRouter(
    prefix='/conceptreferences',
    tags=['ConceptReferences'],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


class ConceptReference(BaseModel):
    code: Optional[str]
    defined_in: Optional[str]
    uri: str
    designation: Optional[str]
    definition: Optional[str]
    reference: Optional[str]
    narrower_than: Optional[List[str]]


@router.get('', response_model=List[ConceptReference])
def get_concept_references(key: ConceptReferenceKeyName, value: str, modifier: SearchModifier, request: Request, response: Response):
    graph: TccmGraph = request.app.state.graph
    new_value = value
    if key == ConceptReferenceKeyName.uri:
        new_value = unquote(value)
    elif key == ConceptReferenceKeyName.curie:
        new_value = unquote(curie_to_uri(value))
    records = graph.get_concept_references_by_value(key, new_value, modifier)
    if not records:
        raise HTTPException(status_code=404, detail=f"ConceptReference {key}={value}|{modifier} not found.")
    response.headers['Link'] = build_jsonld_link_header(str(request.base_url) + request.scope.get("root_path"), 'termci_schema')
    return records


@router.get('/{curie}', response_model=ConceptReference)
def get_concept_reference_by_id(curie: str, request: Request, response: Response):
    graph: TccmGraph = request.app.state.graph
    new_value = unquote(curie_to_uri(curie))
    records = graph.get_concept_references_by_value(ConceptReferenceKeyName.curie, new_value, SearchModifier.equals)
    if not records:
        raise HTTPException(status_code=404, detail=f"ConceptReference curie={curie} not found.")
    response.headers['Link'] = build_jsonld_link_header(str(request.base_url) + request.scope.get("root_path"), 'termci_schema')
    return records[0]
