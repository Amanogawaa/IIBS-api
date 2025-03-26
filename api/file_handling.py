import json
import shutil
import os
from typing import List, Optional, Union
from PIL import Image
from fastapi import HTTPException, UploadFile

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def file_handling(extension_name: str, files: List[UploadFile]):
    file_path = os.path.join(UPLOAD_FOLDER, extension_name)
    os.makedirs(file_path, exist_ok=True) 

    files_dict = {}
    for file in files:
        if file:
            file_location = os.path.join(file_path, file.filename)

            try:
                with open(file_location, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                files_dict[file.filename] = file_location
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
    return json.dumps(files_dict) if files_dict else None