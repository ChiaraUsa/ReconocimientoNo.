# Importación de Módulos y Configuración de Advertencias
import cv2
import numpy as np
from joblib import load
import warnings

# Ignorar advertencias específicas para una mejor legibilidad
warnings.filterwarnings("ignore", message="X does not have valid feature names")

# Cargar el modelo SVM, el scaler y los autovectores PCA
clf = load('../models/svc_digit_classifier_pca.joblib')
scaler = load('../models/scaler_pca.joblib')
pca_eigenvectors = np.load('../models/pca_eigenvectors.npy')

def preprocess_image(image):
    """
    Preprocesa la imagen convirtiéndola a escala de grises y aplicando umbralización binaria inversa.

    Parámetros:
    -----------
    image : array-like
        La imagen de entrada en color.

    Retorna:
    --------
    thresh : array-like
        La imagen umbralizada en escala de grises.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir la imagen a escala de grises
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)  # Aplicar umbralización binaria inversa
    return thresh

def segment_digits(image):
    """
    Segmenta los dígitos en la imagen y los redimensiona a 28x28 píxeles.

    Parámetros:
    -----------
    image : array-like
        La imagen binaria umbralizada.

    Retorna:
    --------
    digits : list of array-like
        Lista de imágenes de dígitos segmentados y redimensionados.

    positions : list of tuple
        Lista de posiciones (x, y, w, h) de cada dígito segmentado.
    """
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Encontrar contornos en la imagen
    digits = []
    positions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)  # Obtener el rectángulo delimitador de cada contorno
        if w > 5 and h > 5:  # Filtrar contornos muy pequeños
            digit = image[y:y+h, x:x+w]
            digit = cv2.resize(digit, (28, 28), interpolation=cv2.INTER_AREA)  # Redimensionar a 28x28 píxeles
            digit = digit.astype('float32') / 255  # Normalizar los valores de los píxeles
            digit = digit.reshape(1, -1)  # Ajustar a 2D
            digits.append(digit)
            positions.append((x, y, w, h))
    return digits, positions

def recognize_digits(digits, scaler, pca_eigenvectors):
    """
    Reconoce los dígitos utilizando el modelo SVM, el escalador y los autovectores PCA.

    Parámetros:
    -----------
    digits : list of array-like
        Lista de imágenes de dígitos segmentados y redimensionados.

    scaler : sklearn scaler
        El escalador entrenado para estandarizar las características.

    pca_eigenvectors : array-like
        Los autovectores del PCA.

    Retorna:
    --------
    predictions : list
        Lista de predicciones de los dígitos.
    """
    predictions = []
    if digits:
        digits_array = np.array(digits).reshape(len(digits), -1)  # Convertir la lista de dígitos a un array 2D
        standardized_digits = scaler.transform(digits_array)  # Estandarizar los dígitos
        projected_digits = np.dot(standardized_digits, pca_eigenvectors)  # Proyectar los dígitos en el espacio PCA
        predictions = clf.predict(projected_digits)  # Predecir los dígitos utilizando el modelo SVM
    return predictions

# Inicializar la captura de video desde la cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

# Obtener el tamaño del frame
ret, frame = cap.read()
height, width, _ = frame.shape

# Definir la región de interés (ROI)
roi_size = 200
roi_top_left = ((width - roi_size) // 2, (height - roi_size) // 2)
roi_bottom_right = ((width + roi_size) // 2, (height + roi_size) // 2)

# Bucle Principal y Visualización
while True:
    ret, frame = cap.read()  # Leer un frame de video

    if not ret:
        print("No se pudo recibir el frame. Saliendo...")
        break

    # Dibujar la región de interés (ROI) en el frame
    cv2.rectangle(frame, roi_top_left, roi_bottom_right, (255, 0, 0), 2)

    # Recortar la ROI del frame
    roi = frame[roi_top_left[1]:roi_bottom_right[1], roi_top_left[0]:roi_bottom_right[0]]

    # Preprocesar la imagen en la ROI
    processed_image = preprocess_image(roi)

    # Segmentar los dígitos en la imagen preprocesada y obtener sus posiciones
    digits, positions = segment_digits(processed_image)
    
    # Reconocimiento de Dígitos
    if digits:
        # Reconocer los dígitos segmentados
        recognized_digits = recognize_digits(digits, scaler, pca_eigenvectors)

        for idx, (digit, (x, y, w, h)) in enumerate(zip(recognized_digits, positions)):
            # Añadir la predicción del dígito al frame
            cv2.putText(frame, f'{digit}', (x + roi_top_left[0], y + roi_top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Mostrar el frame con las predicciones y la ROI
    cv2.imshow('frame', frame)

    # Control de bucle
    if cv2.waitKey(1) == ord('q'):
        break

# Liberar Recursos
cap.release()
cv2.destroyAllWindows()