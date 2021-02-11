from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from termci_api.routers import concept_reference
from fastapi.staticfiles import StaticFiles
from termci_api.db.termci_graph import TermCIGraph


app = FastAPI(title='TermCI (Terminology Code Index) API', dependencies=[Depends(get_graph)])
app.include_router(concept_reference.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)


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
