from dataclasses import dataclass
from py2neo.ogm import Model, Property, RelatedFrom, RelatedTo
from typing import List


@dataclass
class ConceptReference(Model):
    __primarykey__ = 'identifier'
    identifier: str = Property()
    code: str = Property()
    uri: str = Property()
    designation: str = Property()
    definition: str = Property()
    reference: List[str] = Property()

    narrower_than = RelatedTo('ConceptReference', 'NARROWER_THAN')
    defined_in = RelatedTo('ConceptSystem', 'DEFINED_IN')


@dataclass
class ConceptSystem(Model):
    __primarykey__ = 'identifier'
    identifier: str = Property()
    uri: str = Property()
    description: str = Property()
    prefix: str = Property()
    reference: List[str] = Property()
    namespace: str = Property()

    root_concept = RelatedTo(ConceptReference, 'ROOT_CONCEPT')

