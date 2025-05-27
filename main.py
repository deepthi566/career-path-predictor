import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time
from mediapipe.python.solutions.drawing_styles import get_default_face_mesh_tesselation_style

# Voice alert setup
engine = pyttsx3.init(driverName='sapi5')
engine.setProperty('rate', 160)
last_voice_time = 0
voice_cooldown = 5  # seconds

# Log posture violations
def log_violation(student_id, message):
    with open("violations_log.txt", "a") as log_file:
        log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Student {student_id}: {message}\n")

# Voice alert (with cooldown)
def voice_alert(message):
    global last_voice_time
    if time.time() - last_voice_time > voice_cooldown:
        try:
            engine.say(message)
            engine.runAndWait()
            last_voice_time = time.time()
        except Exception as e:
            print(f"Voice alert error: {e}")

# Posture monitoring function
def posture_monitoring(image, landmarks, frameWidth, frameHeight, student_id):
    chin = landmarks[152]
    forehead = landmarks[10]
    chin_y = int(chin.y * frameHeight)
    forehead_y = int(forehead.y * frameHeight)
    vertical_distance = abs(chin_y - forehead_y)

    posture_threshold = 180  # Adjust this threshold as needed

    if vertical_distance < posture_threshold:
        cv2.putText(image, f"Slouching! Sit Up Straight (ID: {student_id})", (int(frameWidth / 3), 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        voice_alert(f"Student {student_id}, Slouching! Sit up straight.")
        log_violation(student_id, "Slouching")

# Orientation check function
def orientation_check(image, landmarks, frameWidth, frameHeight, student_id):
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    nose_tip = landmarks[1]

    eye_distance = abs(left_eye.x - right_eye.x)
    nose_x = nose_tip.x

    if not (min(left_eye.x, right_eye.x) < nose_x < max(left_eye.x, right_eye.x)):
        cv2.putText(image, f"Face the Screen! (ID: {student_id})", (int(frameWidth / 3), 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        voice_alert(f"Student {student_id}, Please face the screen.")
        log_violation(student_id, "Looking Away")

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use your camera or multiple cameras
frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=5,  # Detect up to 5 students at once
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

hands = mp_hands.Hands(
    static_image_mode=False,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2
)

student_id = 0  # Unique ID for each detected student (you can generate this dynamically)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty frame.")
        continue

    image = cv2.flip(image, 1)
    image.flags.writeable = False
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results_face = face_mesh.process(image_rgb)
    results_hands = hands.process(image_rgb)

    image.flags.writeable = True
    image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    if results_face.multi_face_landmarks:
        for i, face_landmarks in enumerate(results_face.multi_face_landmarks):
            student_id = i + 1  # Assign a unique student ID (or use a tracker)
            posture_monitoring(image, face_landmarks.landmark, frameWidth, frameHeight, student_id)
            orientation_check(image, face_landmarks.landmark, frameWidth, frameHeight, student_id)

            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=get_default_face_mesh_tesselation_style()
            )

    if results_hands.multi_hand_landmarks:
        for hand in results_hands.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

    cv2.putText(image, "Press 'Esc' or 'Q' to Quit", (10, int(frameHeight) - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 100), 1, cv2.LINE_AA)

    cv2.imshow('Posture Monitoring System', image)

    key = cv2.waitKey(10) & 0xFF
    if key == 27 or key == ord('q'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()




