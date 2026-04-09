from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from exiftool import ExifToolHelper
import shutil
import uuid
import os
from database import get_db, engine
import model


model.Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = "storage"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

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


@app.post("/upload/")
async def upload_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

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



@app.get("/")
def read_root():
    try:
        get_db()
    
        return {"status": "polaczono z baza danych"}
    except Exception as e:
        return {"status": "Blad polaczenia z baza", "error": str(e)}