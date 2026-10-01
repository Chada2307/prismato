from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/albums",
    tags=["Albums"]
)

@router.post("/", response_model=schemas.AlbumResponse)
def create_album(album: schemas.AlbumCreate, db: Session = Depends(get_db)):
    db_album = models.Album(title=album.title)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)

    return{
        "id": db_album.id,
        "title": db_album.title,
        "created_at": db_album.created_at,
        "photo_count": 0
    }

@router.get("/", response_model=List[schemas.AlbumResponse])
def get_albums(skip: int=0, limit: int=20, db: Session = Depends(get_db)):
    albums = db.query(models.Album).order_by(models.Album.created_at.desc()).offset(skip).limit(limit).all()

    result = []
    for a in albums:
        active_photos = [p for p in a.photos if not p.is_deleted]
        result.append({
            "id": a.id,
            "title": a.title,
            "created_at": a.created_at,
            "photo_count": len(active_photos)
        })

    return result

@router.post("/{album_id}/photos")
def add_photos_to_album(album_id: uuid.UUID, payload: schemas.AlbumAddPhotos, db: Session = Depends(get_db)):
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, details="Nie znaleziono albumu")

    photos = db.query(models.Photo).filter(
        models.Photo.id.in_(payload.photos_ids),
        models.Photo.is_deleted == False
    ).all()

    existing_photo_ids = {p.id for p in album.photos}
    added_count = 0

    for photo in photos:
        if photo.id not in existing_photo_ids:
            album.photos.append(photo)
            added_count += 1

    db.commit()
    return {"message": f"pomyslnie dodano {added_count} zdjęć do albumu"}

@router.get("/{albums}/photos")
def get_album_photos(album_id: uuid.UUID, db: Session = Depends(get_db)):
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Nie znaleziono albumu")

    active_photos = [p for p in album.photos if not p.is_deleted]

    result = []
    for photo in active_photos:
        result.append({
            "id": photo.id,
            "captured_at": photo.captured_at,
            "camera_model": photo.camera_model,
            "thumbnail_url": f"/photos/{photo.id}/thumbnail",
            "original_url": f"/photos/{photo.id}/original",
            "is_favorite": photo.is_favorite
        })
    return result