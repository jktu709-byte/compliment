import asyncio #noqa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn #noqa
from contextlib import asynccontextmanager #noqa

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await ComplimentCRUD.create_tables()
#     yield

app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins = "*")

if __name__ == "__main__":
    uvicorn.run(app = "src.main:app",host="0.0.0.0",reload=True,port=8000)