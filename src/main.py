import cv2
import subprocess
from modules.hand_control import HandRecognizer

def main():
#camera's init
    recognizer = HandRecognizer()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = recognizer.recognize_hands(frame)
        
        cv2.imshow("Signify Gesture Recognition", frame)

# q for exit program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()