from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Path
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import uuid
import os
import shutil
from datetime import datetime
import models
from schemas import PhotoResponse
from database import get_db
from utils.image import get_thumbnail, get_advanced_metadata
from core.tasks import process_photo_task

router = APIRouter(
    prefix="/photos",
    tags=["Gallery"]
)

UPLOAD_DIR = "storage"
THUMBS_DIR = os.path.join(UPLOAD_DIR, "thumbnails")
if not os.path.exists(UPLOAD_DIR) :
    os.makedirs(UPLOAD_DIR)

if not os.path.exists(THUMBS_DIR):
    os.makedirs(THUMBS_DIR)

@router.get("", response_model=List[PhotoResponse])
def get_photos_list(
    favorites: Optional[bool] = False,
    skip: int = 0,
    limit: int = 20,
    
    db: Session = Depends(get_db)
):
    query  = db.query(models.Photo).filter(models.Photo.is_deleted == False)
    if favorites:
        query = query.filter(models.Photo.is_favorite == True)

    photos = query.offset(skip).limit(limit).all()
    result =[]

    for photo in photos:
        result.append({
            "id": photo.id,
            "captured_at": photo.captured_at,
            "camera_model": photo.camera_model,
            "thumbnail_url": f"/photos/{photo.id}/thumbnail",
            "original_url": f"/photos/{photo.id}/original",
            "is_favorite": photo.is_favorite
        })
            
    return result

@router.post("/upload/")
async def upload_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    thumb_path = os.path.join(THUMBS_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
                
    test_user = db.query(models.User).first()
    if not test_user:
        test_user = models.User(username="test_user", passwd_hash="dummy")
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

    new_photo = models.Photo(
        owner_id = test_user.id,
        file_path = file_path,
        file_size = os.path.getsize(file_path),
        thumbnail_path = thumb_path,
    )

    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)

    process_photo_task.delay(new_photo.id, file_path, thumb_path)

    return{
        "message": "zdjecie przyjete. przetwarzanie w tle",
        "photo_id": new_photo.id,
        "status": "processing"
    }

@router.get("/{photo_id}/original")
async def get_original_photo( photo_id: uuid.UUID = Path(...), db: Session = Depends(get_db)):

    photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code=404, detail="photo not found")
    
    if not os.path.exists(photo.file_path):
        raise HTTPException(status_code=404, detail="photo file directory missing")
    
    return FileResponse(photo.file_path)

@router.get("/{photo_id}/thumbnail") ## DONT REPEAT YOURSELF?
async def get_thumbnail_photo( photo_id: uuid.UUID = Path(...), db: Session = Depends(get_db)):

    photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code=404, detail="photo not found")
    
    if not os.path.exists(photo.file_path):
        raise HTTPException(status_code=404, detail="thumbnail file directory missing")
    
    return FileResponse(photo.file_path)

@router.put("/{photo_id}/favorite")
async def toggle_favorite(photo_id: uuid.UUID, db: Session = Depends(get_db)):
    photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    photo.is_favorite = not photo.is_favorite
    db.commit()
    return {"id": photo.id, "is_favorite": photo.is_favorite}


@router.delete("/{photo_id}")
async def move_to_trash(photo_id: uuid.UUID, db: Session = Depends(get_db)):
    photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code = 404, detail="photo not found")
    if photo.is_deleted:
        return {"message": "photo already in trash"}
    
    photo.is_deleted = True
    photo.deleted_at = datetime.now()

    db.commit()
    return {"message": f"Photo {photo_id} moved to trash"}

@router.get("/map-data")
def get_map_photos(db: Session = Depends(get_db)):
    photos = db.query(models.Photo).filter(
        models.Photo.latitude.isnot(None),
        models.Photo.longitude.isnot(None),
        models.Photo.is_deleted == False
    ).all()

    return [
        {
            "id": p.id,
            "lat": p.latitude,
            "lng": p.longitude,
            "thumbnail_url": p.thumbnail_path,        
            "original_url": f"/photos/{p.id}/original",
            "camera_model": p.camera_model,
            "captured_at": p.captured_at,
        }
        for p in photos
    ]

@router.get("/info")
def get_info(db: Session = Depends(get_db)):
    total_count = db.query(func.count(models.Photo.id)).filter(
        models.Photo.is_deleted == False
    ).scalar()

    return {
        "count": total_count
    }