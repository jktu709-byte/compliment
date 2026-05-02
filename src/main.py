from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager #noqa
from src.api.routers import router as comp_router

app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins = "*")
app.include_router(router=comp_router)

if __name__ == "__main__":
    uvicorn.run(app = "src.main:app",host="0.0.0.0",reload=True,port=8000)