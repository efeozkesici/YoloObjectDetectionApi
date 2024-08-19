from PIL import Image
import cv2

def save_image(input_path: str, detections, output_path: str):
    image = cv2.imread(input_path)
    
    for _, row in detections.iterrows():
        xmin, ymin, xmax, ymax, name, confidence = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax']), row['name'], row['confidence']
        label = f'{name} {confidence:.2f}'
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=(0, 255, 0), thickness=2)
        cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imwrite(output_path, image)
