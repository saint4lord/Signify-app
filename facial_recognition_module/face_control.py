import cv2
import mediapipe as mp

class FaceControl:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.drawing_utils = mp.solutions.drawing_utils
        self.drawing_spec = mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style()

    def process_frame(self, frame):
        #convert BGR to RGB for mp
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb_frame)
        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                #draw face landmarks for debug
                self.drawing_utils.draw_landmarks(
                    frame,
                    face_landmarks, 
                    mp.solutions.face_mesh.FACEMESH_TESSELATION,
                    self.drawing_spec
                )
                #extrac exmaple coordinate (nose)
                nose_tip = face_landmarks.landmark[1] #index
                h, w, _ = frame.shape
                x, y = int(nose_tip.x * w), int(nose_tip.y * h)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        return frame
    
    def release(self):
        self.face_mesh.close()

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    face_control = FaceControl()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = face_control.process_frame(frame)
        cv2.imshow("Face Control", frame)
        if cv2.waitKey(1) & 0xFF == 27: #esc to exit
            break
    cap.release()
    face_control.release()
    cv2.destroyAllWindows()
    