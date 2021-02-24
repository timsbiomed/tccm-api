from typing import Union

from neo4j import Driver, GraphDatabase
from termci_api.config import get_settings, Settings
from contextlib import contextmanager


class TermCIGraph:
    def __init__(self, settings: Settings = get_settings()):
        self.user = settings.neo4j_username
        self.password = settings.neo4j_password
        self.uri = f"bolt://{settings.neo4j_host}:{settings.neo4j_bolt_port}"
        self._driver: Union[Driver, None] = None

    def connect(self):
        if not self._driver:
            self._driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def disconnect(self):
        if self._driver:
            self._driver.close()

    @contextmanager
    def create_session(self):
        if not self._driver:
            self.connect()
        session = self._driver.session()
        try:
            yield session
        finally:
            session.close()

    @staticmethod
    def get_concept_references_tx(tx, uri):
        records = []
        result = tx.run("MATCH (n:ConceptReference {uri: $uri}) " 
                        "MATCH q=(n)-[:defined_in]->(s:Resource) "
                        "OPTIONAL MATCH (n)-[:narrower_than]->(p:ConceptReference) "
                        "return n, apoc.coll.toSet(COLLECT(p.uri)) as nt, s.uri as cs", uri=uri)
        for record in result:
            n, nt, cs = record
            node = dict(n.items())
            if len(nt) > 0:
                node['narrower_than'] = nt
            if cs:
                node['defined_in'] = cs
            records.append(node)
        return records

    def get_concept_references(self, uri: str):
        with self._driver.session() as session:
            return session.read_transaction(self.get_concept_references_tx, uri)
