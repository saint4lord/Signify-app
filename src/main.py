import cv2
import os
from modules.hand_control import HandControl
from modules.face_control import EyeControl

def hand_mode():
    """Hand control mode"""
    recognizer = HandControl()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = recognizer.recognize_hands(frame)

        cv2.imshow("Signify Gesture Recognition", frame)

        # Press 'q' to exit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def face_mode():
    """Face control mode"""
    eye_control = EyeControl()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = eye_control.process_frame(frame)

        cv2.imshow("Eye Control", frame)

        # Press 'q' to exit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    eye_control.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    pass
