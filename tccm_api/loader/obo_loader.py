from pronto import Ontology, Term
from rdflib import Graph, URIRef, Literal, RDF, SKOS, RDFS

from tccm_api.loader.onto_loader import OntoLoader
from tccm_api.namespaces import NAMESPACES
from tccm_api.utils import curie_to_uri


class OboLoader(OntoLoader):
    def __init__(self, ontology, ontology_uri):
        self.ontology = Ontology(ontology)
        self.ontology_uri = ontology_uri
        self.graph = Graph()
        self.graph.namespace_manager.bind('skos', SKOS)

    def to_termci(self):
        i = 0
        term: Term
        for term in self.ontology.terms():
            uri = URIRef(curie_to_uri(term.id, NAMESPACES))
            self.graph.add((uri, RDF.type, SKOS.Concept))
            self.graph.add((uri, SKOS.notation, Literal(term.id.split(':')[-1])))
            self.graph.add((uri, SKOS.definition, Literal(term.definition)))
            self.graph.add((uri, SKOS.prefLabel, Literal(term.name)))
            self.graph.add((uri, RDFS.seeAlso, Literal(uri)))
            for sc in iter(term.superclasses(distance=1, with_self=False)):
                sc_uri = URIRef(curie_to_uri(sc.id, NAMESPACES))
                self.graph.add((uri, SKOS.broader, sc_uri))
            self.graph.add((uri, SKOS.inScheme, URIRef(self.ontology_uri)))
