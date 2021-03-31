from termci_api.enums import ConceptReferenceKeyName


def concept_reference_query_by_value(key: ConceptReferenceKeyName):
    if key == ConceptReferenceKeyName.uri or key == ConceptReferenceKeyName.curie:
        return "MATCH (n:ConceptReference {uri: $value}) " \
               "MATCH q=(n)-[:defined_in]->(s:Resource) " \
               "OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference) " \
               "return n, apoc.coll.toSet(COLLECT(p.uri)) as nt, s.uri as cs"
    elif key == ConceptReferenceKeyName.code:
        return "MATCH (n:ConceptReference) " \
               "WHERE n.code STARTS WITH $value " \
               "MATCH q=(n)-[:defined_in]->(s:Resource) " \
               "OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference) " \
               "return n, apoc.coll.toSet(COLLECT(p.uri)) as nt, s.uri as cs"

