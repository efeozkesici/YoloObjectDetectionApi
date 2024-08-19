import torch

def load_model(model_path: str = '/models/yolov5s.pt'):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
    return model

def detect_objects(model, image_path: str, target_classes: list):
    results = model(image_path)
    if target_classes:
        filtered_results = results.pandas().xyxy[0][results.pandas().xyxy[0]['name'].isin(target_classes)]
        return filtered_results
    return results.pandas().xyxy[0]
