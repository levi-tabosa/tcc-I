from fastapi import APIRouter, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from api.deputados.router import router as deputados_router
import uvicorn



app = FastAPI()
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(deputados_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "API de Deputados em funcionamento"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
