# MADE BY 601-

import cv2
import subprocess
from hand_recognition import HandRecognizer

def main():
    # run ascii loading
    subprocess.run(["python", "ascii_intro.py"])
    
    # camera's init
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

