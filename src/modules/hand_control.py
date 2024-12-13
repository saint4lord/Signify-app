import cv2
import mediapipe as mp
import pyautogui
import time

class HandControl:
    def __init__(self, detection_confidence=0.7, tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.closed_fist_start_time = None
        self.click_cooldown = 0.3 
        self.last_click_time = 0
        self.last_mute_toggle_time = 0
        self.mute_toggle_cooldown = 1.0
        self.mute_gesture_active = False

    def recognize_hands(self, frame):
        # decrease frame sizer for perfomance
        small_frame = cv2.resize(frame, (640, 480))
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        # debug info
        gesture_text = "None"
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(small_frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # recognize gesture
                gesture = self.recognize_gesture(hand_landmarks)
                gesture_text = f"Gesture: {gesture}"  # current gesture

        # back size
        frame = cv2.resize(small_frame, (frame.shape[1], frame.shape[0]))

        cv2.putText(frame, gesture_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # таймер закрытия окна
        if self.closed_fist_start_time:
            time_left = 2 - (time.time() - self.closed_fist_start_time)
            if time_left > 0:
                cv2.putText(frame, f"Closing in: {time_left:.1f}s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        return frame


    def recognize_gesture(self, hand_landmarks):
        # Retrieve landmark positions for key fingers
        landmarks = hand_landmarks.landmark
        index_finger_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        middle_finger_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_finger_tip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP]

        # Get screen size and compute cursor position
        screen_width, screen_height = pyautogui.size()
        cursor_x = screen_width - int(index_finger_tip.x * screen_width)
        cursor_y = int(index_finger_tip.y * screen_height)

        # Move cursor gesture: index finger extended while others are retracted
        if (index_finger_tip.y < middle_finger_tip.y and 
            index_finger_tip.y < ring_finger_tip.y and 
            index_finger_tip.y < pinky_tip.y and
            thumb_tip.y > index_finger_tip.y):
            pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)
            self.closed_fist_start_time = None
            self.mute_gesture_active = False  # Reset mute flag if gesture changes
            return "MOVE"

        # Updated click gesture: "OK" shape with thumb and index finger touching, other fingers extended
        elif (abs(index_finger_tip.x - thumb_tip.x) < 0.02 and
            abs(index_finger_tip.y - thumb_tip.y) < 0.02 and
            middle_finger_tip.y < index_finger_tip.y and
            ring_finger_tip.y < index_finger_tip.y and
            pinky_tip.y < index_finger_tip.y):
            current_time = time.time()
            if current_time - self.last_click_time > self.click_cooldown:
                pyautogui.click()
                self.last_click_time = current_time
            self.closed_fist_start_time = None
            self.mute_gesture_active = False  # Reset mute flag if gesture changes
            return "CLICK"

        # Close application gesture: specific finger arrangement for a "close" gesture
        elif (pinky_tip.y < ring_finger_tip.y and
            thumb_tip.y < index_finger_tip.y and
            middle_finger_tip.y > index_finger_tip.y and
            ring_finger_tip.y > index_finger_tip.y):
            # Start countdown if gesture persists for 2 seconds
            if self.closed_fist_start_time is None:
                self.closed_fist_start_time = time.time()
            elif time.time() - self.closed_fist_start_time > 2:
                print("Closing application...")
                self.closed_fist_start_time = None
                pyautogui.hotkey('alt', 'f4')
            self.mute_gesture_active = False  # Reset mute flag when closing application
            return "CLOSE"

        # Mute/unmute gesture: only index and middle fingers up, others down
        elif (index_finger_tip.y < ring_finger_tip.y and
            middle_finger_tip.y < ring_finger_tip.y and
            thumb_tip.y > index_finger_tip.y and
            ring_finger_tip.y > middle_finger_tip.y and
            pinky_tip.y > middle_finger_tip.y):
            # Toggle mute/unmute only once per gesture activation
            if not self.mute_gesture_active:  # Check if mute was already toggled for this gesture
                pyautogui.press("volumemute")
                print("Mute/Unmute toggled")
                self.mute_gesture_active = True
            return "MUTE/UNMUTE"
        
        # Reset timers and flags for any other gesture
        else:
            self.closed_fist_start_time = None
            self.mute_gesture_active = False 
            return "OTHER"

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    hand_control = HandControl()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = hand_control.recognize_hands(frame)
        #cv2.imshow("Hand ontrol", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
            break
    cap.release()
   # hand_control.release()
    cv2.destroyAllWindows()
