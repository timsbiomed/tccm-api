from rdflib import Namespace
from rdflib.namespace import SKOS, RDF, RDFS, OWL, XSD, DC, DCTERMS

NCIT = Namespace('http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#')
OBO = Namespace('http://purl.obolibrary.org/obo/')
HP = Namespace('http://purl.obolibrary.org/obo/HP_')
CS = Namespace('http://termci.ontologies-r.us/CS#')
MONDO = Namespace('http://purl.obolibrary/org/obo/MONDO_')
ICDO3M = Namespace('https://ontologies-r.us/ontology/ICD-O-3-M/')
SH = Namespace('http://www.w3.org/ns/shacl#')
PATO = Namespace('http://purl.obolibrary.org/obo/PATO_')

# Used by prefixcommons functions
NAMESPACES = {
    'DC': DC,
    'DCTERMS': DCTERMS,
    'HP': HP,
    'OBO': OBO,
    'OWL': OWL,
    'NCIT': NCIT,
    'RDF': RDF,
    'SKOS': SKOS,
    'CS': CS,
    'MONDO': MONDO,
    'ICDO3M': ICDO3M,
    'PATO': PATO,
}

