from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Path
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import uuid
import os
import shutil
from datetime import datetime
import models
from schemas import PhotoResponse
from database import get_db
from utils.image import get_thumbnail, get_advanced_metadata

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

@router.get("/", response_model=List[PhotoResponse])
def get_photos_list(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    photos = db.query(models.Photo)\
        .filter(models.Photo.is_deleted == False)\
        .offset(skip).limit(limit).all()
    result =[]
    for photo in photos:
        result.append({
            "id": photo.id,
            "captured_at": photo.captured_at,
            "camera_model": photo.camera_model,
            "thumbnail_url": f"/photos/{photo.id}/thumbnail",
            "original_url": f"/photos/{photo.id}/original",
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
        
    get_thumbnail(file_path, thumb_path)
        

    test_user = db.query(models.User).first()
    if not test_user:
        test_user = models.User(username="test_user", passwd_hash="dummy")
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

    date_taken, lat, lon, camera, raw_data = get_advanced_metadata(file_path)

    new_photo = models.Photo(
        owner_id = test_user.id,
        file_path = file_path,
        file_size = os.path.getsize(file_path),
        thumbnail_path = thumb_path,
        captured_at = date_taken,
        latitude = lat,
        longitude = lon,
        camera_model = camera,
        exif_raw = raw_data
    )

    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)

    return{
        "message": "zdjecie pomyslnie wgrane",
        "photo_id": new_photo.id,
        "path": file_path,
        "captured_at": date_taken
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