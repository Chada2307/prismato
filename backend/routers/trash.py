from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
import os
import models
from schemas import PhotoResponse
from database import get_db
from utils.image import get_thumbnail, get_advanced_metadata
from core.tasks import delete_physical_file_task

UPLOAD_DIR = "storage"
THUMBS_DIR = os.path.join(UPLOAD_DIR, "thumbnails")

if not os.path.exists(UPLOAD_DIR) :
    os.makedirs(UPLOAD_DIR)

if not os.path.exists(THUMBS_DIR):
    os.makedirs(THUMBS_DIR)


router = APIRouter(
    prefix="/trash",
    tags=["Trash"]
)

@router.get("/", response_model=List[PhotoResponse])
def get_photos_list(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    photos = db.query(models.Photo)\
        .filter(models.Photo.is_deleted == True)\
        .offset(skip).limit(limit).all()
    result =[]
    for photo in photos:
        result.append({
            "id": photo.id,
            "captured_at": photo.captured_at,
            "camera_model": photo.camera_model,
            "thumbnail_url": f"/photos/{photo.id}/thumbnail",
            "original_url": f"/photos/{photo.id}/original",
            "is_favorite": photo.is_favorite,
        })
            
    return result

@router.delete("/{photo_id}")
async def delete_photo(photo_id: uuid.UUID, db: Session = Depends(get_db)):
    photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code = 404, detail="photo not found")
    paths_to_delete = [photo.file_path, photo.thumbnail_path]

    for path in paths_to_delete:
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"couldnt delete file {path}: {e}")

    db.delete(photo)
    db.commit()

    return {"message": f"Photo {photo_id} and its thumbnails have been deleted"}

@router.post("/bulk-delete-soft")
def bulk_delete_photos_soft(req: models.BulkDeleteRequest, db: Session = Depends(get_db)):
    deleted_count = db.query(models.Photo).filter(
        models.Photo.id.in_(req.photo_ids)
    ).update({"is_deleted": True}, synchronize_session=False)

    db.commit()

    return{
        "message": f"Przeniesiono do kosza {deleted_count} zdjęć.",
        "deleted_count": deleted_count
    }

@router.post("/bulk-delete-hard")
def bulk_delete_photos_hard(req: models.BulkDeleteRequest, db: Session = Depends(get_db)):
    
    paths = db.query(models.Photo.file_path, models.Photo.thumbnail_path)\
              .filter(models.Photo.id.in_(req.photo_ids)).all()
              
    files_to_delete = []
    for file_path, thumb_path in paths:
        if file_path: files_to_delete.append(file_path)
        if thumb_path: files_to_delete.append(thumb_path)

    deleted_count = db.query(models.Photo).filter(
        models.Photo.id.in_(req.photo_ids)
    ).delete(synchronize_session=False)
    
    db.commit()
    
    if files_to_delete:
       delete_physical_file_task.delay(files_to_delete)
    print("wywolanie trash")
    return {
        "message": f"Trwale usunięto {deleted_count} zdjęć z bazy. Pliki są usuwane w tle.",
        "deleted_count": deleted_count
    }