# YOLO_task

This project implements an object detection service using the YOLOv8 model. 

Running inside Docker containers with a Flask web server.

It utilizes Celery for task processing and Redis is utilized as broker.

It provides a REST API to detect specific objects in images.
    -> JSON can be interpreted as
```bash
    '{
        "image_path": "path to target image", 
        "target_classes": ["person", "dog", etc...]
    }'
```


## Prerequisites

- Docker and Docker Compose installed on your machine.

## Getting Started

### Clone the Repository
```bash
git clone git@github.com:MehmetErenTuranboy/YOLO_task.git
```

### Instructions
- In a terminal window build and start the containers.
- In a terminal window start a celery worker. 
- Either using provided `script.py` file or provided `POST Requests`send requests to the API. If you want to customize the test cases or script feel free to add new pictures to `input` folder.
- The output results will be available in output folder.

### Build and Run Containers

To build and start the containers, run the following command in the project directory:

```bash
docker-compose up --build
```

## Stop Containers

To stop and remove all running containers, networks, and volumes, use:

```bash
docker-compose down
```

If you only want to stop the containers but keep the networks and volumes intact, you can use:
```bash
docker-compose stop
``` 


## Check the Task Status
After sending a detection request, a task_id will be received. Use it to check the status of the detection process:

```bash
curl http://localhost:5001/result/<task_id>
```

## Run Celery Worker
Following code starts a celery worker
```bash
docker-compose exec yolov8-api celery -A app.celery worker --loglevel=info
```

## Send POST Request

Once the containers are running, you can send a POST request to the `/detect` endpoint to detect objects in an image. For example:

```bash
curl -X POST http://localhost:5001/detect -H "Content-Type: application/json" -d '{"image_path": "inputs/testanimal.jpg", "target_classes": ["zebra"]}'
```

```bash
curl -X POST http://localhost:5001/detect -H "Content-Type: application/json" -d '{"image_path": "inputs/testb.png", "target_classes": ["person"]}'
```

```bash
curl -X POST http://localhost:5001/detect -H "Content-Type: application/json" -d '{"image_path": "inputs/aristo.jpg", "target_classes": ["person"]}'
```

## Running the YOLO API Container Separately

If you need to run the YOLO API container separately:

```bash
docker run -d -p 5001:5000 -v $(pwd):/app -v $(pwd)/output:/app/output yolov8-api
```

This command will run the YOLO API container in detached mode, exposing it on port 5001 and mounting the current directory and output folder into the container.

## Simulate Multiple Concurrent Requests:
Following command sends multiple requests to API in a short amount of time. Celery can handle them concurrently.
```bash
python3 script.py
```