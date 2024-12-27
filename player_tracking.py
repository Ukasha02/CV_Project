import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLO model
yolo_model = YOLO("soccer-video-analytics/yolov5x.pt")

# Scaling factor for pixels to meters (hypothetical)
PIXELS_TO_METERS = 1  # Adjust as needed

def detect_and_track(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))  # Adjust FPS as needed

    players_data = {}  # Store player data (position, distance, speed)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))  # Frame rate of the video

    frame_id = 0  # Track the frame index
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process every nth frame to reduce CPU load
        if frame_id % 2 != 0:  # Skip alternate frames
            frame_id += 1
            continue

        results = yolo_model.predict(frame, device='cpu')  # Ensure running on CPU
        detections = results[0].boxes  # Detected bounding boxes

        for box in detections:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            cls = int(box.cls[0])  # Class ID

            if cls == 0:  # Only process 'person' class
                center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
                player_id = assign_player_id(center_x, center_y, players_data)

                # Calculate distance
                if "prev_position" in players_data[player_id]:
                    prev_x, prev_y = players_data[player_id]["prev_position"]
                    pixel_distance = np.sqrt((center_x - prev_x) ** 2 + (center_y - prev_y) ** 2)
                    meter_distance = pixel_distance * PIXELS_TO_METERS
                    players_data[player_id]["distance"] += meter_distance

                    # Calculate speed (distance per second)
                    players_data[player_id]["speed"] = meter_distance * (frame_rate / 2)  # Adjust for skipped frames

                # Update player position
                players_data[player_id]["prev_position"] = (center_x, center_y)

                # Display ID, distance, and speed
                id_text = f"ID:{player_id}"
                distance_text = f"Dist:{players_data[player_id]['distance']:.2f} m"
                speed_text = f"Speed:{players_data[player_id]['speed']:.2f} m/s"

                # Draw annotations
                cv2.putText(frame, id_text, (center_x - 20, center_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                cv2.putText(frame, distance_text, (center_x - 20, center_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(frame, speed_text, (center_x - 20, center_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

        # Write frame to output video
        out.write(frame)
        frame_id += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def assign_player_id(x, y, players_data):
    """Assign or match player IDs based on proximity."""
    for player_id, data in players_data.items():
        px, py = data["prev_position"]
        if np.sqrt((px - x) ** 2 + (py - y) ** 2) < 50:  # Threshold for matching
            return player_id
    new_id = len(players_data) + 1
    players_data[new_id] = {"distance": 0, "prev_position": (x, y), "speed": 0}
    return new_id


# Run the updated module
detect_and_track("videos/soccer_possession.mp4", "output_with_speed_distance_cpu.mp4")
