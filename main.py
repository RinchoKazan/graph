import os.path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.routes.graph import router as graph_router

app = FastAPI(title=settings.app_name)

app.mount("/static", StaticFiles(directory=os.path.join("app", "static")), name="static")

app.include_router(graph_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )