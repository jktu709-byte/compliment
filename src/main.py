from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import router
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins = "*")
app.include_router(router=router)
 
if __name__ == "__main__":
    uvicorn.run(app="src/main:app", reload= True, host= "localhost") 