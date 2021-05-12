import logging

from neo4j.exceptions import ServiceUnavailable
from tccm_api.db.termci_graph import TermCIGraph


def get_concepts(tx):
    query = "MATCH(n:Resource) RETURN n LIMIT 10"
    result = tx.run(query)

    try:
        return [record for record in result]
    # Capture any errors along with the query and data for traceability
    except ServiceUnavailable as exception:
        logging.error(f"{query} raised an error: \n {exception}")
        raise


def test_check_graph(termci_graph: TermCIGraph):
    with termci_graph.create_session() as session:
        records = session.read_transaction(get_concepts)
    assert len(records) == 0


def test_sum():
    assert 1 + 1 == 2
