import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Get screen size
screen_width, screen_height = pyautogui.size()

# Initialize smoothing parameters
prev_x, prev_y = 0, 0
smoothening = 7

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmark.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            mp_draw.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)

            # Index finger tip is id 8
            index_tip = lm_list[8][1:]
            # Thumb tip is id 4
            thumb_tip = lm_list[4][1:]

            x3 = np.interp(index_tip[0], [0, w], [0, screen_width])
            y3 = np.interp(index_tip[1], [0, h], [0, screen_height])

            curr_x = prev_x + (x3 - prev_x) / smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            pyautogui.moveTo(screen_width - curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # Calculate distance between index finger tip and thumb tip
            distance = np.linalg.norm(np.array(index_tip) - np.array(thumb_tip))

            if distance < 40:
                pyautogui.click(button="left")
                cv2.circle(img, index_tip, 15, (0, 255, 0), cv2.FILLED)
            else:
                # Detect fist by checking if other fingertips are folded
                fingers_folded = []
                tip_ids = [8, 12, 16, 20]
                pip_ids = [6, 10, 14, 18]
                for tip, pip in zip(tip_ids, pip_ids):
                    if lm_list[tip][2] > lm_list[pip][2]:
                        fingers_folded.append(True)
                    else:
                        fingers_folded.append(False)
                if all(fingers_folded):
                    pyautogui.click(button="right")

    cv2.imshow("Finger Mouse", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
