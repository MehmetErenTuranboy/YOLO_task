import requests
import time
from threading import Thread

def submit_request(image_path, target_classes):
    url = 'http://localhost:5001/detect'
    data = {
        "image_path": image_path,
        "target_classes": target_classes
    }
    response = requests.post(url, json=data)
    task_id = response.json().get("task_id")
    print(f"Task submitted for {image_path}. Task ID: {task_id}")
    
    if task_id:
        check_status(task_id)

def check_status(task_id):
    status_url = f"http://localhost:5001/result/{task_id}"
    
    while True:
        status_response = requests.get(status_url)
        status_data = status_response.json()
        print(f"Task ID: {task_id}, Status: {status_data['status']}")
        
        if status_data['status'] == 'success':
            print(f"Output Path: {status_data['output_path']}")
            break
        elif status_data['status'] == 'error':
            print(f"Error: {status_data['message']}")
            break
        else:
            print("Task is still processing. Waiting for completion...")
            time.sleep(5)  # Wait for 5 seconds before checking again

# simulate multiple req
images_to_process = [
    {"image_path": "testanimal.jpg", "target_classes": ["zebra"]},
    {"image_path": "Albert_Einstein_Head.jpg", "target_classes": ["person"]},
    {"image_path": "testa.jpg", "target_classes": ["person"]},
    {"image_path": "testb.png", "target_classes": ["person"]},
    {"image_path": "test.jpg", "target_classes": ["bus"]},
]

# threads for each request
threads = []
for image_data in images_to_process:
    thread = Thread(target=submit_request, args=(image_data["image_path"], image_data["target_classes"]))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()
