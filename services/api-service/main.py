from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST
)

from routes.auth import router as auth_router
from routes.debug import router as debug_router

from observation.tracing import setup_tracing


app = FastAPI()


app.include_router(
    auth_router,
    prefix="/auth"
)

app.include_router(
    debug_router
)


setup_tracing(app)


@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )