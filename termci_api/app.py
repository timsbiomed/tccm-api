from fastapi import FastAPI, Request, Depends
from neo4j import GraphDatabase, Driver

from termci_api.config import get_settings
from termci_api.routers import concept_reference
from fastapi.staticfiles import StaticFiles
from termci_api.db.termci_graph import TermCIGraph


def get_graph():
    settings = get_settings()
    graph: Driver = GraphDatabase.driver(settings.neo4j_bolt_uri, auth=(settings.neo4j_username, settings.neo4j_password))
    try:
        yield graph
    finally:
        graph.close()


app = FastAPI(title='TermCI (Terminology Code Index) API', dependencies=[Depends(get_graph)])
app.include_router(concept_reference.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
def root():
    return {'message': 'Hello TermCI!'}


@app.on_event("startup")
async def startup():
    app.state.graph = TermCIGraph()
    app.state.graph.connect()


@app.on_event("shutdown")
async def shutdown():
    if app.state.graph:
        app.state.graph.disconnect()
