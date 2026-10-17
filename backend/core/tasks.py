import time
from core.celery_app import celery_app
import models
from database import SessionLocal
from utils.image import get_thumbnail, get_advanced_metadata

@celery_app.task
def process_photo_task(photo_id: str, file_path: str, thumb_path:str):

    get_thumbnail(file_path, thumb_path)
    date_taken, lat, lon, camera, raw_data = get_advanced_metadata(file_path)

    db = SessionLocal()
    try:
        photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()

        if photo:
            photo.thumbnail_path = thumb_path
            photo.captured_at = date_taken
            photo.latitude = lat
            photo.longitude = lon
            photo.camera_model = camera
            photo.exif_raw = raw_data

            db.commit()
    except Exception as e:
        db.rollback()
        print(f"Blad podczas aktualizacji rekordu {photo_id}: {e}")
    finally:
        db.close()

    return {"status": "success", "photo_id": photo_id}


@celery_app.task
def delete_physical_file_task(file_paths: list):
    deleted = 0
    for path in file_paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
                deleted += 1
            except Exception as e:
                print(f"Błąd podczas usuwania pliku {path}: {e}")
                
    print(f"Celery: Pomyślnie usunięto {deleted} plików z dysku.")
    return {"status": "success", "deleted_files": deleted}    
