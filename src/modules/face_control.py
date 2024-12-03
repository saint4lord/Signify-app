import cv2
import mediapipe as mp
import pyautogui
import numpy as np

class EyeControl:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.screen_width, self.screen_height = pyautogui.size()

    def process_frame(self, frame):
        # Mirror the frame for natural interaction
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb_frame)

        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                h, w, _ = frame.shape

                # Extract eye regions
                left_eye = [face_landmarks.landmark[i] for i in [33, 133]]  # Indices for left eye
                right_eye = [face_landmarks.landmark[i] for i in [362, 263]]  # Indices for right eye

                # Find centers of the eyes
                left_center = self.get_eye_center(left_eye, w, h)
                right_center = self.get_eye_center(right_eye, w, h)

                if left_center and right_center:  # Ensure eye centers are detected
                    # Calculate gaze direction (average of both eyes)
                    gaze_x = (left_center[0] + right_center[0]) / 2
                    gaze_y = (left_center[1] + right_center[1]) / 2

                    # Map gaze coordinates to screen size
                    cursor_x = np.interp(gaze_x, [0, w], [0, self.screen_width])
                    cursor_y = np.interp(gaze_y, [0, h], [0, self.screen_height])

                    # Move cursor
                    pyautogui.moveTo(cursor_x, cursor_y)

                    # Draw eyes for debugging
                    cv2.circle(frame, left_center, 5, (0, 255, 0), -1)
                    cv2.circle(frame, right_center, 5, (0, 255, 0), -1)

        return frame

    def get_eye_center(self, eye_landmarks, width, height):
        # If landmarks are empty, return None
        if not eye_landmarks:
            return None
        
        # Calculate coordinates
        x_coords = [int(landmark.x * width) for landmark in eye_landmarks if 0 <= landmark.x <= 1]
        y_coords = [int(landmark.y * height) for landmark in eye_landmarks if 0 <= landmark.y <= 1]
        
        # Check if coordinates lists are not empty
        if not x_coords or not y_coords:
            return None

        return int(np.mean(x_coords)), int(np.mean(y_coords))

    def release(self):
        self.face_mesh.close()

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    eye_control = EyeControl()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = eye_control.process_frame(frame)
        cv2.imshow("Eye Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
            break
    cap.release()
    eye_control.release()
    cv2.destroyAllWindows()
