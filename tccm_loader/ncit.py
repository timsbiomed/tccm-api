from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

from rdflib import Graph, Literal, RDFS, RDF

from tccm_model.tccm_model import *
from tccm_api.namespaces import NAMESPACES, NCIT
from utils import curie_to_uri

ROOT = Path(__file__).parent.parent


def get_ncit():
    resp = urlopen("https://evs.nci.nih.gov/ftp1/NCI_Thesaurus/Thesaurus.FLAT.zip")
    zipfile = ZipFile(BytesIO(resp.read()))
    graph = Graph()
    graph.namespace_manager.bind('skos', SKOS)
    graph.namespace_manager.bind('sh', SH)
    graph.namespace_manager.bind('dc', DC)
    graph.namespace_manager.bind('ncit', NCIT)
    cs_uri = URIRef("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl")
    graph.add((cs_uri, RDF.type, SKOS.ConceptScheme))
    graph.add((cs_uri, DC.description, Literal(
        "A vocabulary for clinical care, translational and basic research, and public information and administrative activities.")))
    graph.add((cs_uri, RDFS.seeAlso, Literal("https://ncithesaurus.nci.nih.gov/ncitbrowser/")))
    graph.add((cs_uri, SH.namespace, URIRef("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#")))
    graph.add((cs_uri, SH.prefix, Literal("NCIT")))

    for line in zipfile.open("Thesaurus.txt"):
        tokens = line.decode("utf-8").split("\t")
        uri = URIRef(tokens[1][1:-1])
        graph.add((uri, RDF.type, SKOS.Concept))
        graph.add((uri, SKOS.notation, Literal(tokens[0])))
        graph.add((uri, SKOS.definition, Literal(tokens[4])))
        graph.add((uri, SKOS.prefLabel, Literal(tokens[3].split("|")[0])))
        if tokens[2]:
            for code in tokens[2].split("|"):
                code = code.strip()
                sc_uri = URIRef(curie_to_uri(f"NCIT:{code}", NAMESPACES))
                graph.add((uri, SKOS.broader, sc_uri))
        see_also = f"https://ncit.nci.nih.gov/ncitbrowser/pages/concept_details.jsf?dictionary=NCI%20Thesaurus&code={tokens[0]}"
        graph.add((uri, RDFS.seeAlso, Literal(see_also)))
        graph.add((uri, SKOS.inScheme, cs_uri))
    with open('ncit-termci.ttl', 'w') as file:
        file.write(graph.serialize(format='turtle').decode('utf-8'))


if __name__ == '__main__':
    get_ncit()



