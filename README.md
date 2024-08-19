# YOLO Object Detection API

## Overview
This project implements a RESTful API for performing object detection on images using a pre-trained YOLO model. The API is containerized using Docker.

## Directory Structure

yolo-api-docker/
│
├── Dockerfile
├── README.md
├── app/
│ ├── main.py
│ ├── yolo.py
│ ├── utils.py
│ └── init.py
├── models/
│ └── yolov5s.pt # Pre-trained YOLO model
├── requirements.txt
└── sample/
├── input.jpg
├── output.jpg
└── test_api.py


## Setup

### 1. Build the Docker Container

``` docker build -t yolo-api . ```

### 2. Run the Docker Container

``` docker run -p 8000:8000 -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output yolo-api ```

### 3. Test the API
You can test the API using the provided script:

``` python sample/test_api.py ```

### 4. API Endpoint
- #### POST /detect/
    Detect objects in an image

    - #### Parameters
        - `file` : The image file to be processed (Type: File)
        - `target_classes` : (Optional) List of object classes to filter result (Type: Text)
    - #### Response
        - `message` : Detection status message
        - `output_image` : Path to the output image wğith detected objects

### Dependencies
- Python 3.8
- FastAPI
- Uvicorn
- Pillow
- Torch
- OpenCV

### Error Handling
- Handles invalid file types, missing files, and model errors gracefully. 
### Performance
- The YOLO model used is YOLOv5, providing a good balance between accuracy and speed.

### Concurrency
- Consider using asynchronous task queues like Celery for handling multiple requests concurrently.

### Notes
- `Dynamic Image Upload`: Images are uploaded dynamically through the POST request.
- `Dynamic Target Classes`: Object classes to detect are specified dynamically as a comma-separated string.
This documentation provides an overview of the setup, usage, and testing of the YOLO Object Detection API. If you have any questions or need further assistance, feel free to ask!

## Test API

You can find a sample script in the project's file directory.