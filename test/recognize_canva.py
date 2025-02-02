# Importaciones necesarias
import cv2
import numpy as np
import mediapipe as mp
from collections import deque
from joblib import load
import warnings

# Ignorar advertencias específicas para una mejor legibilidad
warnings.filterwarnings("ignore", message="X does not have valid feature names")

# Asignar diferentes arrays para manejar puntos de color
points = [deque(maxlen=1024)]
index = 0

# El kernel a utilizar para el propósito de dilatación
kernel = np.ones((5, 5), np.uint8)

# Establecer el color a negro
color = (0, 0, 0)

# Cargar el modelo y el escalador
model = load('../models/digit_recognizer')
scaler = load('../models/scaler.joblib')

# Función para predecir el dígito
def prediction(image, model, scaler):
    img = cv2.resize(image, (28, 28))
    img = img.flatten().reshape(1, -1)
    img = scaler.transform(img)
    predict = model.predict(img)
    return predict[0]

# Configuración de la ventana de dibujo (canvas)
paintWindow = np.zeros((471, 636, 3)) + 255  # Crear una ventana blanca
paintWindow = cv2.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)  # Dibujar un rectángulo en la ventana
cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)  # Añadir texto "CLEAR"
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)  # Crear una ventana de OpenCV llamada 'Paint'

# Inicializar Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Inicializar la webcam
cap = cv2.VideoCapture(0)
ret = True
while ret:
    # Leer cada frame desde la webcam
    ret, frame = cap.read()

    x, y, c = frame.shape

    # Voltear el frame verticalmente
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir a RGB

    # Dibujar un rectángulo y añadir texto "CLEAR" en el frame
    frame = cv2.rectangle(frame, (40, 1), (140, 65), (0, 0, 0), 2)
    cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

    # Obtener la predicción de los puntos de referencia de la mano
    result = hands.process(framergb)

    # Postprocesar el resultado
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * 640)
                lmy = int(lm.y * 480)

                landmarks.append([lmx, lmy])

            # Dibujar los puntos de referencia en los frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
        fore_finger = (landmarks[8][0], landmarks[8][1])  # Coordenadas del dedo índice
        center = fore_finger
        thumb = (landmarks[4][0], landmarks[4][1])  # Coordenadas del pulgar
        cv2.circle(frame, center, 3, (0, 255, 0), -1)  # Dibujar un círculo en el dedo índice

        if (thumb[1] - center[1] < 30):
            points.append(deque(maxlen=512))
            index += 1
        elif center[1] <= 65:
            if 40 <= center[0] <= 140:  # Botón de limpieza
                points = [deque(maxlen=512)]
                index = 0
                paintWindow[67:, :, :] = 255
        else:
            points[index].appendleft(center)
    else:
        points.append(deque(maxlen=512))
        index += 1

    # Dibujar líneas en el canvas y el frame
    for j in range(len(points)):
        for k in range(1, len(points[j])):
            if points[j][k - 1] is None or points[j][k] is None:
                continue
            cv2.line(frame, points[j][k - 1], points[j][k], color, 2)
            cv2.line(paintWindow, points[j][k - 1], points[j][k], color, 2)

    # Dibujar ROI en la ventana de pintura
    bbox_size = (200, 200)
    bbox = [(int(636 // 2 - bbox_size[0] // 2), int(471 // 2 - bbox_size[1] // 2)),
            (int(636 // 2 + bbox_size[0] // 2), int(471 // 2 + bbox_size[1] // 2))]
    cv2.rectangle(frame, bbox[0], bbox[1], (0, 255, 0), 2)

    # Guardar el estado de la ventana de pintura antes de mostrar el dígito
    backup = paintWindow.copy()

    if index > 0 and len(points[index - 1]) > 1:
        img_cropped = paintWindow[bbox[0][1]:bbox[1][1], bbox[0][0]:bbox[1][0]]
        img_cropped = np.array(img_cropped, dtype=np.uint8)  # Asegurarse de que la imagen esté en formato uint8
        img_gray = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY_INV)

        digit = prediction(thresh, model, scaler)

        # Añadir la predicción del dígito a la ventana de pintura
        cv2.putText(paintWindow, f'Digit: {digit}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Paint", paintWindow)
        cv2.waitKey(500)  # Mostrar la predicción durante 500 ms

        # Restaurar el estado de la ventana de pintura
        paintWindow = backup

    cv2.imshow("Output", frame)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) == ord('q'):
        break

# Liberar la webcam y destruir todas las ventanas activas
cap.release()
cv2.destroyAllWindows()