from enum import Enum


class ConceptReferenceKeyName(str, Enum):
    uri = "uri"
    curie = "curie"
    code = "code"


class SearchModifier(str, Enum):
    equals = 'equals'
    starts_with = "starts_with"
    contains = "contains"
    any = "any"
    all = "all"
