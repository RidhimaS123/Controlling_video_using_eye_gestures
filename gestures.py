import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe solutions
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Variables for blink detection
last_eye_state = None

# Constants
BLINK_THRESHOLD = 0.3
EYE_CLOSED_THRESHOLD = 0.02
gesture_cooldown = 1  # seconds
last_gesture_time = time.time()

# Finger tip landmarks
FINGER_TIPS = [8, 12, 16, 20]

# Blink detection
def check_eye_status(landmarks):
    left_eye_top = landmarks[159]
    left_eye_bottom = landmarks[145]
    right_eye_top = landmarks[386]
    right_eye_bottom = landmarks[374]
    
    left_eye_height = abs(left_eye_top.y - left_eye_bottom.y)
    right_eye_height = abs(right_eye_top.y - right_eye_bottom.y)

    if left_eye_height < EYE_CLOSED_THRESHOLD and right_eye_height < EYE_CLOSED_THRESHOLD:
        return "closed"
    else:
        return "open"

# Count raised fingers
def count_raised_fingers(hand_landmarks):
    count = 0
    for tip in FINGER_TIPS:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
    return count

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result_face = face_mesh.process(rgb_frame)
    result_hands = hands.process(rgb_frame)

    # Blink Detection
    if result_face.multi_face_landmarks:
        for landmarks in result_face.multi_face_landmarks:
            eye_state = check_eye_status(landmarks.landmark)

            if eye_state == "closed" and last_eye_state != "closed":
                pyautogui.press('space')
                last_eye_state = "closed"
                cv2.putText(frame, "Video Paused", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif eye_state == "open" and last_eye_state != "open":
                pyautogui.press('space')
                last_eye_state = "open"
                cv2.putText(frame, "Video Playing", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Hand Gesture Detection
    if result_hands.multi_hand_landmarks:
        for hand_landmarks in result_hands.multi_hand_landmarks:
            fingers = count_raised_fingers(hand_landmarks)
            current_time = time.time()

            if current_time - last_gesture_time > gesture_cooldown:
                if fingers == 1:
                    pyautogui.press('volumeup')
                    cv2.putText(frame, "Volume Up", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                elif fingers == 2:
                    pyautogui.press('volumedown')
                    cv2.putText(frame, "Volume Down", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                elif fingers == 3:
                    pyautogui.press('right')  # Skip forward
                    cv2.putText(frame, "Skip Forward", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                elif fingers == 4:
                    pyautogui.press('left')  # Skip backward
                    cv2.putText(frame, "Skip Backward", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                last_gesture_time = current_time

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Hand and Blink Gesture Control - YouTube Chrome', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
