from flask import Flask, request, jsonify
import os
import cv2
import torch
from ultralytics import YOLO

app = Flask(__name__)

# Load the pre-trained YOLOv8 model
model = YOLO('yolov8n.pt')  # Adjust path if necessary

# Directory to save output images
output_dir = '/app/output'
os.makedirs(output_dir, exist_ok=True)

@app.route('/detect', methods=['POST'])
def detect_objects():
    data = request.json
    image_path = data.get('image_path')
    target_classes = data.get('target_classes', [])

    if not image_path or not os.path.exists(image_path):
        return jsonify({"status": "error", "message": "Invalid image path"}), 400

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        return jsonify({"status": "error", "message": "Failed to load image"}), 400

    # Perform object detection
    results = model(image)

    # Filter results by target classes
    filtered_results = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)  # Class ID
            confidence = float(box.conf)  # Confidence score
            if len(target_classes) == 0 or model.names[class_id] in target_classes:
                # Append the box with its coordinates and other information
                filtered_results.append({
                    "class_id": class_id,
                    "label": model.names[class_id],
                    "confidence": confidence,
                    "coordinates": box.xyxy.cpu().numpy().tolist()
                })

    # Draw bounding boxes and save the image
    for item in filtered_results:
        x1, y1, x2, y2 = map(int, item['coordinates'][0])
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{item['label']} {item['confidence']:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    output_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(output_path, image)

    return jsonify({"status": "success", "output_path": output_path})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
