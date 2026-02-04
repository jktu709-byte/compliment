import time #noqa
import asyncio #noqa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins = "*")

compliment_app = app

if __name__ == "__main__":
    # asyncio.run(main())
    uvicorn.run(app = "compliment_app.main:app",host="0.0.0.0",reload=True,port=8000)