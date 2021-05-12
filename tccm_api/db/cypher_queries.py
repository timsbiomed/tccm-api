from tccm_api.enums import ConceptReferenceKeyName, ConceptSystemKeyName, SearchModifier
import sys

def concept_reference_query_by_value(key: ConceptReferenceKeyName, modifier: SearchModifier):
    if key == ConceptReferenceKeyName.uri or key == ConceptReferenceKeyName.curie:
        if modifier == SearchModifier.equals:
            return "MATCH (n:ConceptReference {uri: $value}) " \
                   "MATCH q=(n)-[:defined_in]->(s:Resource) " \
                   "OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference) " \
                   "return n, apoc.coll.toSet(COLLECT(p.uri)) as nt, s.uri as cs"
    elif key == ConceptReferenceKeyName.code:
        if modifier == SearchModifier.equals:
            return "MATCH (n:ConceptReference) " \
                   "WHERE n.code = $value " \
                   "MATCH q=(n)-[:defined_in]->(s:Resource) " \
                   "OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference) " \
                   "return n, apoc.coll.toSet(COLLECT(p.uri)) as nt, s.uri as cs"
        elif modifier == SearchModifier.starts_with:
            return "MATCH (n:ConceptReference) " \
                   "WHERE n.code STARTS WITH $value " \
                   "MATCH q=(n)-[:defined_in]->(s:Resource) " \
                   "OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference) " \
                   "return n, apoc.coll.toSet(COLLECT(p.uri)) as nt, s.uri as cs"


def concept_reference_query_by_value_and_concept_system(key: ConceptReferenceKeyName, modifier: SearchModifier):
    if key == ConceptReferenceKeyName.uri or key == ConceptReferenceKeyName.curie:
        if modifier == SearchModifier.equals:
            return "MATCH (n:ConceptReference {uri: $value) " \
                   "MATCH q=(n)-[:defined_in]->(s:Resource {uri: $concept_system}) " \
                   "OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference) " \
                   "return n, apoc.coll.toSet(COLLECT(p.uri))"
    elif key == ConceptReferenceKeyName.code:
        if modifier == SearchModifier.equals:
            return "MATCH (n:ConceptReference) " \
                   "WHERE n.code = $value " \
                   "MATCH q=(n)-[:defined_in]->(s:Resource {uri: $concept_system}) " \
                   "OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference) " \
                   "return n, apoc.coll.toSet(COLLECT(p.uri)) as nt"
        elif modifier == SearchModifier.starts_with:
            return "MATCH (n:ConceptReference) " \
                   "WHERE n.code STARTS WITH $value " \
                   "MATCH q=(n)-[:defined_in]->(s:Resource {uri: $concept_system}) " \
                   "OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference) " \
                   "return n, apoc.coll.toSet(COLLECT(p.uri)) as nt"


def concept_references_query_by_values_and_concept_system(key: ConceptReferenceKeyName):
    if key == ConceptReferenceKeyName.uri or key == ConceptReferenceKeyName.curie:
        return "MATCH (n:ConceptReference) " \
               "WHERE n.uri IN $values " \
               "MATCH q=(n)-[:defined_in]->(s:Resource {prefix: $concept_system}) " \
               "OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference) " \
               "return n, apoc.coll.toSet(COLLECT(p.uri)) as nt, s.uri as cs"
    elif key == ConceptReferenceKeyName.code:
        return "MATCH (n:ConceptReference) " \
               "WHERE n.code IN $values " \
               "MATCH q=(n)-[:defined_in]->(s:Resource {prefix: $concept_system}) " \
               "OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference) " \
               "return n, apoc.coll.toSet(COLLECT(p.uri)) as nt, s.uri as cs"


def concept_system_query_by_value(key: ConceptReferenceKeyName, modifier: SearchModifier):
    if key == ConceptSystemKeyName.uri:
        if modifier == SearchModifier.equals:
            return "MATCH (n:ConceptSystem {uri: $value}) " \
                   "return n"
    elif key == ConceptSystemKeyName.prefix:
        if modifier == SearchModifier.equals:
            return "MATCH (n:ConceptSystem {prefix: $value}) " \
                   "return n"


def concept_references_query_by_descendants_of(depth: int = sys.maxsize):
    if depth == sys.maxsize:
        depth_str = "*1.."
    elif depth == 1:
        depth_str = ""
    else:
        depth_str = f"*1..{depth}"

    # MATCH q=(n)-[:narrower_than *1..]->(:ConceptReference{uri: "http://purl.obolibrary.org/obo/PATO_0000014"})
    # WITH collect(DISTINCT n) as nList
    # WITH nList, size(nList) as total
    # UNWIND nList as n
    # OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference)
    # OPTIONAL MATCH (n)-[:defined_in]->(s:Resource)
    # return n, apoc.coll.toSet(COLLECT(p.uri)) as nt, s.uri as cs, total limit 10"

    return "MATCH (n:ConceptReference) " \
           "MATCH q=(n)-[:narrower_than " + depth_str + "]->(:ConceptReference{uri: $uri}) " \
           "WITH collect(DISTINCT n) as nList " \
           "WITH nList, size(nList) as total " \
           "UNWIND nList as n " \
           "OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference) " \
           "OPTIONAL MATCH (n)-[:defined_in]->(s:Resource) " \
           "return n, apoc.coll.toSet(COLLECT(p.uri)) as nt, s.uri as cs, total"
