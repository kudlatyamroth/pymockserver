import uvicorn
from fastapi import FastAPI

from pymockserver.adapters.shared_memory import db
from pymockserver.domain.fixture import load_fixtures
from pymockserver.routers import meta, mockserver
from pymockserver.tools.utils import use_route_names_as_operation_ids

__version__ = "2.0.2"

app = FastAPI(
    title="MockServer API",
    description="Simple and fast mock server implemented in python",
    version=__version__,
)


@app.on_event("startup")
def startup() -> None:
    db.connect()
    load_fixtures()


@app.on_event("shutdown")
def shutdown() -> None:
    db.close()


app.include_router(meta.router)
app.include_router(mockserver.router)

use_route_names_as_operation_ids(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
