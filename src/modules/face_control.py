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

                # Extract eye regions directly in pixels
                left_eye_coords = self.get_eye_coords(face_landmarks, [33, 133], w, h)
                right_eye_coords = self.get_eye_coords(face_landmarks, [362, 263], w, h)

                if left_eye_coords and right_eye_coords:
                    # Calculate gaze position based on eye landmarks
                    left_gaze = self.get_gaze_position(left_eye_coords)
                    right_gaze = self.get_gaze_position(right_eye_coords)

                    # Calculate the center of the gaze direction
                    if left_gaze and right_gaze:
                        gaze_x = (left_gaze[0] + right_gaze[0]) / 2
                        gaze_y = (left_gaze[1] + right_gaze[1]) / 2

                        # Map gaze coordinates to screen size
                        cursor_x = np.interp(gaze_x, [0, w], [0, self.screen_width])
                        cursor_y = np.interp(gaze_y, [0, h], [0, self.screen_height])

                        # Move cursor
                        pyautogui.moveTo(cursor_x, cursor_y)

                        # Draw eyes for debugging
                        cv2.circle(frame, left_gaze, 5, (0, 255, 0), -1)
                        cv2.circle(frame, right_gaze, 5, (0, 255, 0), -1)

                # Detect head tilt (left, right, up, down)
                tilt = self.detect_head_tilt(face_landmarks, w, h)
                if tilt == "left":
                    pyautogui.scroll(500)  # Scroll up
                elif tilt == "right":
                    pyautogui.scroll(-500)  # Scroll down

                # Check if the mouth is open for a click action
                if self.is_mouth_open(face_landmarks, w, h):
                    pyautogui.click()  # Perform click

        return frame

    def detect_head_tilt(self, face_landmarks, width, height):
        # Extract key points for head tilt detection
        nose_tip = face_landmarks.landmark[1]  # Nose tip
        left_eye = face_landmarks.landmark[33]  # Left eye corner
        right_eye = face_landmarks.landmark[263]  # Right eye corner

        # Convert normalized landmarks to pixel coordinates
        nose_x, nose_y = int(nose_tip.x * width), int(nose_tip.y * height)
        left_eye_x, left_eye_y = int(left_eye.x * width), int(left_eye.y * height)
        right_eye_x, right_eye_y = int(right_eye.x * width), int(right_eye.y * height)

        # Detect tilt based on relative positions
        if left_eye_y < right_eye_y - 10:  # Head tilted to the left
            return "left"
        elif right_eye_y < left_eye_y - 10:  # Head tilted to the right
            return "right"
        return None

    def is_mouth_open(self, face_landmarks, width, height):
        # Extract coordinates of the upper and lower lips
        upper_lip = face_landmarks.landmark[13]  # Upper lip
        lower_lip = face_landmarks.landmark[14]  # Lower lip

        # Convert normalized landmarks to pixel coordinates
        upper_lip_y = int(upper_lip.y * height)
        lower_lip_y = int(lower_lip.y * height)

        # Check if the mouth is open by measuring the distance between the lips
        mouth_distance = abs(upper_lip_y - lower_lip_y)
        if mouth_distance > 20:  # Adjust the threshold based on testing
            return True
        return False

    def get_eye_coords(self, face_landmarks, eye_indices, width, height):
        # Extract the eye landmarks and convert to pixel coordinates
        eye_landmarks = [face_landmarks.landmark[i] for i in eye_indices]
        x_coords = [int(landmark.x * width) for landmark in eye_landmarks if 0 <= landmark.x <= 1]
        y_coords = [int(landmark.y * height) for landmark in eye_landmarks if 0 <= landmark.y <= 1]

        # Return the center point of the eye
        if x_coords and y_coords:
            return int(np.mean(x_coords)), int(np.mean(y_coords))
        return None

    def get_gaze_position(self, eye_coords):
        # In this case, we simply return the center of the eye, which is used for gaze
        return eye_coords

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
        if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit (just for test cases)
            break
    cap.release()
    eye_control.release()
    cv2.destroyAllWindows()
