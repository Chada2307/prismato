
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
from datetime import datetime
from exiftool import ExifToolHelper
import models as models

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

def get_thumbnail(file_path: str, thumb_path: str, max_size: tuple = (1080, 1080)):
        try:
            with Image.open(file_path) as img:
                img = ImageOps.exif_transpose(img)
            
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            img.save(thumb_path, format="WEBP", quality=80, method=4)

            return True

        except Exception as e:
            print(f"Błąd generowania miniatury: {e}")
            return False
