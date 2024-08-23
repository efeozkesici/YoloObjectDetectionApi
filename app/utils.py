import os
import shutil
from PIL import Image, ImageDraw, UnidentifiedImageError
from fastapi import UploadFile, HTTPException

def create_temp_file(file: UploadFile) -> str:
    try:
        temp_image_path = f"temp/{file.filename}"
        os.makedirs(os.path.dirname(temp_image_path), exist_ok=True)
        with open(temp_image_path, "wb") as temp_image:
            shutil.copyfileobj(file.file, temp_image)
        return temp_image_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create temporary file: {str(e)}")

def remove_temp_file(path: str) -> None:
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove temporary file: {str(e)}")

def save_image(input_image_path: str, detection_results: list, output_path: str) -> None:
    try:
        image = Image.open(input_image_path)
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to open image: {str(e)}")

    try:
        for result in detection_results:
            draw_bounding_box(image, result)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")

def draw_bounding_box(image: Image, result: dict) -> None:
    try:
        draw = ImageDraw.Draw(image)
        bbox = result['bbox']
        label = result['label']
        confidence = result['confidence']
        
        draw.rectangle(bbox, outline="red", width=2)
        
        text = f"{label} ({confidence:.2f})"
        text_size = draw.textsize(text)
        
        text_background = [bbox[0], bbox[1] - text_size[1], bbox[0] + text_size[0], bbox[1]]
        draw.rectangle(text_background, fill="red")
        
        draw.text((bbox[0], bbox[1] - text_size[1]), text, fill="white")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to draw bounding box: {str(e)}")
