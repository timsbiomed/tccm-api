from fastapi import FastAPI
from tccm_api.routers import concepts
from fastapi.staticfiles import StaticFiles

app = FastAPI(title='TCCM API')
app.include_router(concepts.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def root():
    return {'message': 'Hello TCCM!'}


