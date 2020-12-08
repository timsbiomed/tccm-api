from fastapi import FastAPI
from tccm_api.routers import concepts

app = FastAPI(title='TCCM API')
app.include_router(concepts.router)


@app.get('/')
def root():
    return {'message': 'Hello TCCM!'}


