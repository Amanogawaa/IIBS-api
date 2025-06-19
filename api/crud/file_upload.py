import os
from typing import Optional
from PIL import Image
from uuid import uuid4
import shutil
from fastapi import HTTPException, UploadFile
from api.schema.image import ImageResponse

UPLOAD_DIR = "uploads/editor/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_image(file: Optional[UploadFile] = None) -> ImageResponse:
    image_path = None
    if file:
        allowed_extensions = {"jpg", "jpeg", "png", "gif"}
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid image_file type")
        
        unique_filename = f"{uuid4().hex}.{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, unique_filename)

        temp_path = image_path + ".temp"
        with open(temp_path, "wb") as buffer:
            file.file.seek(0)
            shutil.copyfileobj(file.file, buffer)
        
        try:
            img = Image.open(temp_path)
            img.verify()

            img = Image.open(temp_path)

            max_size = (800, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            img.save(image_path, quality=85, optimize=True)
            os.remove(temp_path) 

        except Exception as e:
            os.remove(temp_path)
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        finally:
            file.file.close()

    return ImageResponse(image_path=image_path) if image_path else None