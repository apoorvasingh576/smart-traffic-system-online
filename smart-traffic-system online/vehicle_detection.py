from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("yolov8n.pt")

def count_vehicles(image_path):

    image = cv2.imread(image_path)

    if image is None:
        print("Image not found")
        return 0

    results = model(image, conf=0.25)

    count = 0

    vehicle_classes = [
        "car",
        "motorcycle",
        "bus",
        "truck"
    ]

    annotated = image.copy()

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            if class_name in vehicle_classes:

                count += 1

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                cv2.rectangle(
                    annotated,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    annotated,
                    class_name,
                    (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (0, 255, 0),
                    1
                )

    cv2.imwrite(
        "static/detected_traffic.jpg",
        annotated
    )

    return count