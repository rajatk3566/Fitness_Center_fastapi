from fastapi import FastAPI
from .database import engine,Base
from .models import user, member
from .api.v1.router import api_router



Base.metadata.create_all(bind=engine)


app = FastAPI(title="Fitness Center Management")

app.include_router(
    api_router,
    prefix="/api/v1"
)

@app.get("/")
def root():
    return {"message": "Welcome to Fitness Center API"}