import shutil
import os
from typing import List, Optional, Union
from PIL import Image
from fastapi import UploadFile

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def file_handling(extension_name: str, files: List[UploadFile]):
    file_path = os.path.join(UPLOAD_FOLDER, extension_name)
    os.makedirs(file_path, exist_ok=True) 

    responses = []
    
    for file in files:
        file_location = os.path.join(file_path, file.filename)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        responses.append({"message": f"File '{file.filename}' uploaded successfully", "path": file_location})
    
    return responses  # Return after processing all files
