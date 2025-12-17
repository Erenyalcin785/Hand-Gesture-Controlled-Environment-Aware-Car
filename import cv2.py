import cv2
import mediapipe as mp
import serial
import time

arduino = serial.Serial('COM4', 9600)
time.sleep(2)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

last_command = "empty"
confirmed_command = "empty"
candidate_command = "empty"
candidate_start_time = 0
STABLE_DURATION = 0.5  # Komut sabit kalma süresi

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Kamera açılırken hata oluştu.")
        break

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    current_time = time.time()
    detected_command = "Empty"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            index_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            middle_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            ring_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
            pinky_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

            index_mcp_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
            middle_mcp_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
            ring_mcp_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y
            pinky_mcp_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y

            if (pinky_tip_y < thumb_tip_y and 
                pinky_tip_y < index_tip_y and 
                pinky_tip_y < middle_tip_y and 
                pinky_tip_y < ring_tip_y and 
                index_tip_y > thumb_tip_y and 
                middle_tip_y > thumb_tip_y and 
                ring_tip_y > thumb_tip_y):
                detected_command = "RIGHT"
            elif (index_tip_y < thumb_tip_y and 
                  index_tip_y < middle_tip_y and 
                  index_tip_y < ring_tip_y and 
                  index_tip_y < pinky_tip_y and 
                  pinky_tip_y > thumb_tip_y and 
                  middle_tip_y > thumb_tip_y and 
                  ring_tip_y > thumb_tip_y):
                detected_command = "LEFT"
            elif (index_tip_y < thumb_tip_y and 
                  middle_tip_y < thumb_tip_y and 
                  ring_tip_y < thumb_tip_y and 
                  pinky_tip_y < thumb_tip_y and 
                  index_tip_y < middle_tip_y):
                detected_command = "STOP"
            elif (index_mcp_y < thumb_tip_y and 
                  middle_mcp_y < thumb_tip_y and 
                  ring_mcp_y < thumb_tip_y and 
                  pinky_mcp_y < thumb_tip_y):
                detected_command = "FORWARD"
            elif (index_mcp_y > thumb_tip_y and 
                  middle_mcp_y > thumb_tip_y and 
                  ring_mcp_y > thumb_tip_y and 
                  pinky_mcp_y > thumb_tip_y):
                detected_command = "BACK"
            break

    # Kararlılık kontrolü
    if detected_command != candidate_command:
        candidate_command = detected_command
        candidate_start_time = current_time
    else:
        if (current_time - candidate_start_time) >= STABLE_DURATION and candidate_command != confirmed_command:
            confirmed_command = candidate_command

            if confirmed_command == "FORWARD":
                arduino.write(b'F')
            elif confirmed_command == "LEFT":
                arduino.write(b'L')
            elif confirmed_command == "RIGHT":
                arduino.write(b'R')
            elif confirmed_command == "BACK":
                arduino.write(b'B')
            elif confirmed_command == "STOP":
                arduino.write(b'S')

            print(f"Gönderilen komut: {confirmed_command}")
            last_command = confirmed_command

    # Görselleştir
    cv2.putText(image, f'Command: {confirmed_command}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('El Tespiti', image)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
