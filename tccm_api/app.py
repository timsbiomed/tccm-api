from pathlib import Path

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from tccm_api.routers import concept_reference, concept_system, code_set
from fastapi.staticfiles import StaticFiles
from tccm_api.db.tccm_graph import TccmGraph


app = FastAPI(title='TCCM (Terminology Core Common Model) API', dependencies=[])
app.include_router(concept_reference.router)
app.include_router(concept_system.router)
app.include_router(code_set.router)
app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent/"static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/')
def root():
    return RedirectResponse(url="/docs")


@app.on_event("startup")
async def startup():
    app.state.graph = TccmGraph()
    app.state.graph.connect()


@app.on_event("shutdown")
async def shutdown():
    if app.state.graph:
        app.state.graph.disconnect()
