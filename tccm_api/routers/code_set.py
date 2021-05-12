from fastapi import APIRouter, Response, Request, Depends, HTTPException, UploadFile, File

from urllib.parse import unquote

from tccm_api.enums import ConceptReferenceKeyName
from tccm_api.db.tccm_graph import TccmGraph
from tccm_api.utils import decode_uri, build_jsonld_link_header
import yaml
from copy import deepcopy

router = APIRouter(
    prefix='/codesets',
    tags=['CodeSets'],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


def parse_code_set_def_yaml(yaml_str):
    code_set_def = yaml.safe_load(yaml_str)
    return code_set_def


def resolve_code_set_def(code_set_def, graph):
    code_set_res = deepcopy(code_set_def)
    if 'include' in code_set_def:
        includes = code_set_res.pop('include')
        ns = includes['entities']['namespace']
        codes = includes['entities']['codes']
        # resolve the codes with namespace
        code_set_res['members'] = graph.get_concept_references_by_values_and_concept_system(ConceptReferenceKeyName.code, codes, ns)
    elif 'descendants_of' in code_set_def:
        uri = code_set_res.pop('descendants_of')
        uri = decode_uri(uri)
        code_set_res['total'], code_set_res['members'] = graph.get_concept_references_by_descendants_of(uri)
    return code_set_res


@router.get('/{uri}')
def get_code_set(uri: str, request: Request, response: Response):
    graph: TccmGraph = request.app.state.graph
    orig_uri = uri
    uri = decode_uri(uri)
    records = graph.get_code_set(unquote(uri))
    if not records:
        raise HTTPException(status_code=404, detail=f"CodeSet {orig_uri} not found.")
    node = records[0]
    response.headers['Link'] = build_jsonld_link_header('termci_schema')
    return node


@router.post('/resolve', responses={
                200: {
                    "content": {
                        'application/yaml': {}
                    },
                    "description": "Return the resoved code set in JSON or YAML format.",
                }
            })
def resolve_code_set_definition(request: Request, response: Response, file: UploadFile = File(...)):
    graph: TccmGraph = request.app.state.graph
    value = None
    # parse the codeset definition
    if file.content_type == 'application/json':
        ...
    elif file.content_type == 'application/x-yaml' or file.content_type == 'text/yaml':
        code_set_def = parse_code_set_def_yaml(file.file)
        code_set_res = resolve_code_set_def(code_set_def, graph)
    # response.headers['Link'] = build_jsonld_link_header('termci_schema')
    if request.headers['accept'] == 'application/json':
        return code_set_res
    elif request.headers['accept'] == 'application/x-yaml':
        return Response(content=yaml.dump(code_set_res), media_type="application/x-yaml")

