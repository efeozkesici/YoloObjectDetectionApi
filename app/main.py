from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.yolo import load_model, prepare_image, run_inference
from app.utils import save_image, create_temp_file, remove_temp_file

app = FastAPI()

model = load_model()

@app.post("/detect/")
async def detect_objects_in_image(file: UploadFile = File(...), target_classes: str = ""):
    
    target_classes_list = [cls.strip() for cls in target_classes.split(',') if cls.strip()]

    if not file.filename.endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only jpg, jpeg, and png are allowed.")
    
    temp_image_path = create_temp_file(file)
    image_tensor = prepare_image(temp_image_path)

    try:
        results = await run_inference(model, image_tensor, target_classes_list)

        output_path = f"output/{file.filename}"
        save_image(temp_image_path, results, output_path)

        return JSONResponse(content={"message": "Detection complete", "output_image": output_path}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        remove_temp_file(temp_image_path)