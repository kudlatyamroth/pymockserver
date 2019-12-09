import uvicorn
from fastapi import FastAPI

from routers import meta, mockserver


__version__ = "0.7.1"
app = FastAPI(
    title="MockServer API", description="Simple and fast mock server implemented in python", version=__version__,
)

app.include_router(meta.router, tags=["Meta"])
app.include_router(mockserver.router, tags=["MockServer"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
