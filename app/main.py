from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.yolo import load_model, detect_objects
from app.utils import save_image
from typing import List
import os
import shutil

app = FastAPI()

model = load_model()

@app.post("/detect/")
async def detect_objects_in_image(file: UploadFile = File(...), target_classes: str = ""):
    if not file.filename.endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only jpg, jpeg, and png are allowed.")
    
    try:
        temp_image_path = f"temp/{file.filename}"
        with open(temp_image_path, "wb") as temp_image:
            shutil.copyfileobj(file.file, temp_image)

        target_classes_list = [cls.strip() for cls in target_classes.split(',') if cls.strip()]

        results = detect_objects(model, temp_image_path, target_classes_list)

        output_path = f"output/{file.filename}"
        save_image(temp_image_path, results, output_path)

        os.remove(temp_image_path)

        return JSONResponse(content={"message": "Detection complete", "output_image": output_path}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
