from app import celery, detect_objects_task 

if __name__ == "__main__":
    celery.start()