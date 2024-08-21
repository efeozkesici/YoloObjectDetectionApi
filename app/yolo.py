import torch
from torchvision import transforms
from PIL import Image

def load_model(model_path: str = "models/yolov5s.pt"):
    model = torch.load(model_path)
    model.eval()  # Inference moduna alıyoruz
    return model

def prepare_image(image_path: str, input_size: int = 640):
    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((input_size, input_size)),
        transforms.ToTensor(),
    ])
    return transform(image).unsqueeze(0)  # Batch boyutunu ekliyoruz

def run_inference(model, image_tensor, target_classes: list):
    with torch.no_grad():
        outputs = model(image_tensor)[0]

    filtered_results = []
    for i in range(len(outputs['boxes'])):
        label = model.names[outputs['labels'][i]]
        if label in target_classes or not target_classes:
            filtered_results.append({
                'label': label,
                'confidence': outputs['scores'][i].item(),
                'bbox': outputs['boxes'][i].tolist()
            })
    return filtered_results
