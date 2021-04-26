from typing import Union, List

from neo4j import Driver, GraphDatabase

from termci_api.config import get_settings, Settings
from contextlib import contextmanager
from termci_api.db.cypher_queries import *
from termci_api.enums import ConceptReferenceKeyName, ConceptSystemKeyName, SearchModifier


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
    def get_concept_references_by_value_tx(tx, key: ConceptReferenceKeyName, value: str, modifier: SearchModifier):
        records = []
        query = concept_reference_query_by_value(key, modifier)
        result = tx.run(query, value=value)
        for record in result:
            n, nt, cs = record
            node = dict(n.items())
            if len(nt) > 0:
                node['narrower_than'] = nt
            if cs:
                node['defined_in'] = cs
            records.append(node)
        return records

    @staticmethod
    def get_concept_references_by_values_and_concept_system_tx(tx, key: ConceptReferenceKeyName, values: List[str], concept_system: str):
        records = []
        query = concept_references_query_by_values_and_concept_system(key)
        result = tx.run(query, values=values, concept_system=concept_system)
        for record in result:
            n, nt, cs = record
            node = dict(n.items())
            if len(nt) > 0:
                node['narrower_than'] = nt
            if cs:
                node['defined_in'] = cs
            records.append(node)
        return records

    def get_concept_references_by_value(self, key: ConceptReferenceKeyName, value: str, modifier: SearchModifier):
        with self._driver.session() as session:
            return session.read_transaction(self.get_concept_references_by_value_tx, key, value, modifier)

    def get_concept_references_by_values_and_concept_system(self, key: ConceptReferenceKeyName, values: List[str], concept_system: str):
        with self._driver.session() as session:
            return session.read_transaction(self.get_concept_references_by_values_and_concept_system_tx, key, values, concept_system)


    def get_code_set_by_id_tx(self, code_set_id: str):
        records = []
        return records

    def get_code_set_by_id(self, code_set_id: str):
        with self._driver.session() as session:
            return session.read_transaction(self.get_code_set_by_id_tx, code_set_id)

    @staticmethod
    def get_concept_systems_by_value_tx(tx, key: ConceptSystemKeyName, value: str, modifier: SearchModifier):
        records = []
        query = concept_system_query_by_value(key, modifier)
        result = tx.run(query, value=value)
        for record in result:
            records.append(record['n'])
        return records

    def get_concept_systems_by_value(self, key: ConceptSystemKeyName, value: str, modifier: SearchModifier):
        with self._driver.session() as session:
            return session.read_transaction(self.get_concept_systems_by_value_tx, key, value, modifier)
