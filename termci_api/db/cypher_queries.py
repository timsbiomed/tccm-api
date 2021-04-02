from termci_api.enums import ConceptReferenceKeyName, ConceptSystemKeyName, SearchModifier


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


def concept_system_query_by_value(key: ConceptReferenceKeyName, modifier: SearchModifier):
    if key == ConceptSystemKeyName.uri:
        if modifier == SearchModifier.equals:
            return "MATCH (n:ConceptSystem {uri: $value}) " \
                   "return n"
    elif key == ConceptSystemKeyName.prefix:
        if modifier == SearchModifier.equals:
            return "MATCH (n:ConceptSystem {prefix: $value}) " \
                   "return n"


