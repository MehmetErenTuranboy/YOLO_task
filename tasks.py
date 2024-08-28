from celery_app import celery
from yolo_utils import process_image_with_yolo

@celery.task(name='tasks.detect_objects_task')
def detect_objects_task(image_path, target_classes):
    output_path, error = process_image_with_yolo(image_path, target_classes)
    if error:
        return {"status": "error", "message": error}
    return {"status": "success", "output_path": output_path}
