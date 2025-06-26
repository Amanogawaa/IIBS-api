# Update your upload endpoint to return Syncfusion-compatible response
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
from typing import Optional
from PIL import Image
from uuid import uuid4
import shutil

from api.schema.image import ImageResponse, VideoResponse

IMAGE_UPLOAD_DIR = "uploads/editor/"
os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)

def upload_image(file: Optional[UploadFile] = File(None)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    try:
        allowed_extensions = {"jpg", "jpeg", "png", "gif"}
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid image file type")
        
        unique_filename = f"{uuid4().hex}.{file_ext}"
        image_path = os.path.join(IMAGE_UPLOAD_DIR, unique_filename)
        
        # Save the file temporarily
        temp_path = image_path + ".temp"
        with open(temp_path, "wb") as buffer:
            file.file.seek(0)
            shutil.copyfileobj(file.file, buffer)
        
        # Validate and process image
        img = Image.open(temp_path)
        img.verify()
        
        img = Image.open(temp_path)
        max_size = (800, 800)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(image_path, quality=85, optimize=True)
        
        # Clean up temp file
        os.remove(temp_path)
        
        # Create response using ImageResponse schema
        response = ImageResponse(
            image_path=f"uploads/editor/{unique_filename}",
            name=unique_filename,
            size=os.path.getsize(image_path),
            type=f"image/{file_ext}",
            # url=""  # url will be computed by the computed_field
        )
        
        return response
        
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        file.file.close()

VIDEO_UPLOAD_DIR = "uploads/video/"
os.makedirs(VIDEO_UPLOAD_DIR, exist_ok=True)    

def upload_video(file: UploadFile = File(...)):
    video_path = None

    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    try:
        allowed_extensions = {"mp4", "webm", "mov", "mkv"}  # Add supported video formats
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid video file type")

        unique_filename = f"{uuid4().hex}.{file_ext}"   
        video_path = os.path.join(VIDEO_UPLOAD_DIR, file.filename)
        
        # Save the file
        with open(video_path, "wb") as buffer:
            file.file.seek(0)
            shutil.copyfileobj(file.file, buffer)
        
        # Create response
        response = VideoResponse(
            video_path=f"uploads/video/{file.filename}",
            name=file.filename,
            size=os.path.getsize(video_path),
            type=f"video/{file_ext}",   
        )
        
        return response
        
    except Exception as e:
        if os.path.exists(video_path):
            os.remove(video_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        file.file.close()