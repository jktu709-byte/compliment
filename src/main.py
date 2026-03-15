import time #noqa
import asyncio #noqa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn #noqa
from src.api.CRUD import AsyncCREATE
async def main():
    app = FastAPI()
    app.add_middleware(CORSMiddleware,allow_origins = "*")
    
    @app.post("Compliment/CreateBase")
    async def AsCreate():
        result = AsyncCREATE.create_tables()
        await result

if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(app = "src.main:app",host="0.0.0.0",reload=True,port=8000)