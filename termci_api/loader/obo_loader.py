from pronto import Ontology, Term
from rdflib import Graph, URIRef, Literal, RDF, SKOS, RDFS

from termci_api.loader.onto_loader import OntoLoader
from termci_api.namespaces import NAMESPACES, HP
from termci_api.utils import curie_to_uri


class OboLoader(OntoLoader):
    def __init__(self, ontology_uri):
        self.ontology = Ontology(ontology_uri)
        self.graph = Graph()
        self.graph.namespace_manager.bind('skos', SKOS)
        self.graph.namespace_manager.bind('hp', HP)

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
        with open('hp.turtle', 'w') as file:
            file.write(self.graph.serialize(format='turtle').decode('utf-8'))


if __name__ == '__main__':
    loader = OboLoader('http://purl.obolibrary.org/obo/hp.obo')
    loader.to_termci()
