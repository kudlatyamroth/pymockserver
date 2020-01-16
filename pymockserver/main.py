import uvicorn
from fastapi import FastAPI

from routers import meta, mockserver

from utils import use_route_names_as_operation_ids


__version__ = "1.3.6"

app = FastAPI(
    title="MockServer API", description="Simple and fast mock server implemented in python", version=__version__,
)

app.include_router(meta.router, tags=["Meta"])
app.include_router(mockserver.router, tags=["MockServer"])

use_route_names_as_operation_ids(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)