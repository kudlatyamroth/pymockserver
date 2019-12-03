import uvicorn
from fastapi import FastAPI

import router

app = FastAPI(title="MockServer API", description="Simple and fast mock server implemented in python", version="0.5.1",)

app.include_router(router.router, tags=["MockServer"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
