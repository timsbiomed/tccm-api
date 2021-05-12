import requests
import csv
import pandas as pd
from pathlib import Path

from rdflib import Graph

from tccm_model.tccm_model import *
from linkml.dumpers.rdf_dumper import as_rdf_graph
ROOT = Path(__file__).parent.parent.absolute()


def get_icdo():
    # url = 'https://www.naaccr.org/wp-content/uploads/2020/10/Copy-of-ICD-O-3.2_MFin_17042019_web.xls'
    f = ROOT / 'tccm_loader/Copy-of-ICD-O-3.2_MFin_17042019_web.csv'
    df = pd.read_csv(open(f, 'r', encoding='utf-8'), skiprows=[0])

    ns = "https://ontologies-r.us/ontology/ICD-O-3-M/"
    cs = ConceptSystem(uri=ns[:-1], namespace=ns, prefix="ICDO3M")
    cs.contents = list()
    parent = None
    for index, row in df.iterrows():
        # print(row[0], '|', row[1], '|', row[2])
        if row[1] == 'Preferred' or row[1] == '2':
            uri = ns + row[0].replace('/', '.')
            cr = ConceptReference(uri=uri, code=row[0], defined_in=ns[:-1])
            cr.definition = row[2]
            if row[1] == '2':
                parent = uri
            else:
                cr.narrower_than = parent
            cs.contents.append(cr)
    # context = str(ROOT/'static/jsonld_10/context/termci_schema.context.jsonld').replace('\\', '/')
    context = "https://termci.ontologies-r.us/static/jsonld/jsonld_10/context/termci_schema.context.jsonld"
    graph = as_rdf_graph(cs, contexts=context)
    graph.namespace_manager.bind('ICDO3M', URIRef(ns))
    graph.serialize(destination='icdo3m-termci.ttl', format='turtle')


if __name__ == '__main__':
    get_icdo()



