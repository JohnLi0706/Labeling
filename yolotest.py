import cv2
import csv
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")

# Open the video file
video_path = "/Users/zexianli/Desktop/project1/person-bicycle-car-detection.mp4"
cap = cv2.VideoCapture(video_path)

# Define the CSV file path
csv_file_path = "/Users/zexianli/Desktop/temp/tracking_results.csv"

# Open the CSV file for writing
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["image", "xmin", "ymin", "xmax", "ymax", "label"])

    frame_number = 0

    # Loop through the video frames
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            frame_number += 1
            # Generate the image filename
            image_filename = f"output_frame_{frame_number:04d}.png"
            
            # Run YOLOv8 tracking on the frame with ByteTrack
            results = model.track(frame, tracker="bytetrack.yaml", persist=True)

            # Class mapping: adjust indices according to your model's classes
            class_map = {
                0: "pedestrian",
                1: "twowheelvehicle",
                2: "fourwheelvehicle",
                3: "twowheelvehicle"
            }

            for result in results[0].boxes:
                # Extract bounding box coordinates
                x1, y1, x2, y2 = result.xyxy[0].cpu().numpy()
                
                # Extract class index separately
                cls_idx = int(result.cls.cpu().numpy())

                # Generate the object ID and label
                object_id = int(result.id.cpu().numpy()) if result.id is not None else -1
                label = class_map.get(cls_idx, "unknown") + str(object_id)  # Map class index to label
                
                # Write the result to the CSV file
                writer.writerow([image_filename, x1, y1, x2, y2, label])

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Tracking with ByteTrack", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
