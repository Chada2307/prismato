from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Path
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
from datetime import datetime
from exiftool import ExifToolHelper
import shutil
import uuid
import os
from database import get_db, engine
import model
from schema import PhotoResponse
from typing import List


model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "storage"
THUMBS_DIR = os.path.join(UPLOAD_DIR, "thumbnails")

if not os.path.exists(UPLOAD_DIR) :
    os.makedirs(UPLOAD_DIR)

if not os.path.exists(THUMBS_DIR):
    os.makedirs(THUMBS_DIR)

def get_advanced_metadata(path):
    try:
        with ExifToolHelper() as et:
            metadata = et.get_metadata(path)[0]
            
            date_str = metadata.get('EXIF:DateTimeOriginal') or metadata.get('IPTC:DateCreated')
            captured_at = None
            if date_str:
                captured_at = datetime.strptime(date_str,"%Y:%m:%d %H:%M:%S")

            lat = metadata.get('Composite:GPSLatitude')
            lon = metadata.get('Composite:GPSLongitude')

            camera= metadata.get('EXIF:Model', 'Unknown')
            return captured_at, lat, lon, camera, metadata
    except Exception as e:
        print(f"Blad ExifTool: {e}")
        return None, None, None, None, {}


def get_exif_date(path):
    try:
        image = Image.open(path)
        exif_data = image._getexif()
        if not exif_data:
            return None
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "DateTimeOriginal":
                return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Blad exif: {e}")
    return None

def get_thumbnail(in_path, out_path):
        image = Image.open(in_path)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        image = ImageOps.fit(image, (600, 600), Image.Resampling.LANCZOS)
        image.save(out_path, format="WEBP", quality=80)

@app.post("/upload/")
async def upload_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    thumb_path = os.path.join(THUMBS_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    get_thumbnail(file_path, thumb_path)
        

    test_user = db.query(model.User).first()
    if not test_user:
        test_user = model.User(username="test_user", passwd_hash="dummy")
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

    date_taken, lat, lon, camera, raw_data = get_advanced_metadata(file_path)

    new_photo = model.Photo(
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

@app.get("/photos/{photo_id}/original")
async def get_original_photo( photo_id: uuid.UUID = Path(...), db: Session = Depends(get_db)):

    photo = db.query(model.Photo).filter(model.Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code=404, detail="photo not found")
    
    if not os.path.exists(photo.file_path):
        raise HTTPException(status_code=404, detail="photo file directory missing")
    
    return FileResponse(photo.file_path)

@app.get("/photos/{photo_id}/thumbnail") ## DONT REPEAT YOURSELF?
async def get_thumbnail_photo( photo_id: uuid.UUID = Path(...), db: Session = Depends(get_db)):

    photo = db.query(model.Photo).filter(model.Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code=404, detail="photo not found")
    
    if not os.path.exists(photo.file_path):
        raise HTTPException(status_code=404, detail="thumbnail file directory missing")
    
    return FileResponse(photo.file_path)



@app.get("/photos/", response_model=List[PhotoResponse])
def get_photos_list(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    photos = db.query(model.Photo)\
        .filter(model.Photo.is_deleted == False)\
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

@app.get("/trash/", response_model=List[PhotoResponse])
def get_photos_list(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    photos = db.query(model.Photo)\
        .filter(model.Photo.is_deleted == True)\
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


@app.delete("/photo/{photo_id}")
async def move_to_trash(photo_id: uuid.UUID, db: Session = Depends(get_db)):
    photo = db.query(model.Photo).filter(model.Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code = 404, detail="photo not found")
    if photo.is_deleted:
        return {"message": "photo already in trash"}
    
    photo.is_deleted = True
    photo.deleted_at = datetime.now()

    db.commit()
    return {"message": f"Photo {photo_id} moved to trash"}

@app.delete("/trash/{photo_id}")
async def delete_photo(photo_id: uuid.UUID, db: Session = Depends(get_db)):
    photo = db.query(model.Photo).filter(model.Photo.id == photo_id).first()

    if not photo:
        raise HTTPException(status_code = 404, detail="photo not found")
    paths_to_delete = [photo.file_path, photo.thumbnail_path]

    for path in paths_to_delete:
        try:
            if path and os.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"couldnt delete file {path}: {e}")

    db.delete(photo)
    db.commit()

    return {"message": f"Photo {photo_id} and its thumbnails have been deleted"}


@app.get("/")
def read_root():
    try:
        get_db()
    
        return {"status": "polaczono z baza danych"}
    except Exception as e:
        return {"status": "Blad polaczenia z baza", "error": str(e)}