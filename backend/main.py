from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from database import get_db, engine
import models as models
from routers import photos, trash

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(photos.router)
app.include_router(trash.router)

UPLOAD_DIR = "storage"
THUMBS_DIR = os.path.join(UPLOAD_DIR, "thumbnails")

if not os.path.exists(UPLOAD_DIR) :
    os.makedirs(UPLOAD_DIR)

if not os.path.exists(THUMBS_DIR):
    os.makedirs(THUMBS_DIR)

@app.get("/")
def read_root():
    try:
        get_db()
        return {"status": "polaczono z baza danych"}
    except Exception as e:
        return {"status": "Blad polaczenia z baza", "error": str(e)}