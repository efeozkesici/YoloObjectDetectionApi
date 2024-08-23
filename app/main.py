import torch
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
from utils import create_temp_file, remove_temp_file, save_image

app = FastAPI()

try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to load YOLO model: {str(e)}")

class DetectionRequest(BaseModel):
    target_classes: List[str]

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...), request: DetectionRequest = None):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file format")

    temp_image_path = create_temp_file(file)
    
    try:
        try:
            image = model(temp_image_path)
            results = image.pandas().xyxy[0].to_dict(orient="records")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to perform object detection: {str(e)}")

        try:
            filtered_results = [
                {
                    'bbox': [result['xmin'], result['ymin'], result['xmax'], result['ymax']],
                    'label': result['name'],
                    'confidence': result['confidence']
                }
                for result in results if result['name'] in request.target_classes
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to filter results: {str(e)}")

        output_image_path = f"output/{file.filename}"
        save_image(temp_image_path, filtered_results, output_image_path)
        
    finally:
        remove_temp_file(temp_image_path)

    return {"output_image_path": output_image_path}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
