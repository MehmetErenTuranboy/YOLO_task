import os
import cv2
from ultralytics import YOLO

# YOLO v8 model
model = YOLO('yolov8n.pt')

# output conf
output_dir = './output'
os.makedirs(output_dir, exist_ok=True)

def process_image_with_yolo(image_path, target_classes):
    image = cv2.imread(image_path)
    if image is None:
        return None, "Failed to load image"

    results = model(image)
    filtered_results = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            confidence = float(box.conf)
            if len(target_classes) == 0 or model.names[class_id] in target_classes:
                filtered_results.append({
                    "class_id": class_id,
                    "label": model.names[class_id],
                    "confidence": confidence,
                    "coordinates": box.xyxy.cpu().numpy().tolist()
                })

    for item in filtered_results:
        x1, y1, x2, y2 = map(int, item['coordinates'][0])
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image, f"{item['label']} {item['confidence']:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    output_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(output_path, image)

    return output_path, None
