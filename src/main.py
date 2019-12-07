import uvicorn
from fastapi import FastAPI

import router
import meta_router

app = FastAPI(title="MockServer API", description="Simple and fast mock server implemented in python", version="0.6.0",)

app.include_router(router.router, tags=["MockServer"])
app.include_router(meta_router.router, tags=["Meta"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
