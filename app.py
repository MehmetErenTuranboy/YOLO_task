from flask import Flask, request, jsonify
from celery_app import make_celery 
from tasks import detect_objects_task
import os

app = Flask(__name__)

# Celery Configuration
app.config.from_object('config.Config')

celery = make_celery(app)

# Endpoint to submit an image for object detection
@app.route('/detect', methods=['POST'])
def detect_objects():
    data = request.json
    image_path = data.get('image_path')
    target_classes = data.get('target_classes', [])

    if not image_path or not os.path.exists(image_path):
        return jsonify({"status": "error", "message": "Invalid image path"}), 404

    task = detect_objects_task.delay(image_path, target_classes)
    return jsonify({"status": "processing", "task_id": task.id}), 202


# Check the status of an object detection task
@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    task = detect_objects_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {"status": "pending"}
    elif task.state == 'FAILURE':
        response = {"status": "error", "message": str(task.info)}
    else:
        response = {"status": task.info.get('status'), "output_path": task.info.get('output_path')}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
