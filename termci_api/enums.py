from enum import Enum


class ConceptReferenceKeyName(str, Enum):
    uri = "uri"
    curie = "curie"
    code = "code"


class ConceptSystemKeyName(str, Enum):
    prefix = "prefix"
    uri = "uri"


class SearchModifier(str, Enum):
    equals = 'equals'
    starts_with = "starts_with"
    contains = "contains"
    any = "any"
    all = "all"

