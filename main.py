from fastapi import FastAPI
from .routers import projects
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Green Finance Platform", 
             description="Blockchain-Cloud integrated Green Finance Platform", 
             version="1.0.0")

app.include_router(projects.router)

@app.get("/")
async def root():
    return {"message": "Green Finance Platform API"}