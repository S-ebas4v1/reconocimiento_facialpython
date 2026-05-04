import face_recognition
import cv2
import numpy as np
import os

# =========================
# FUNCIÓN PARA CARGAR ROSTROS (VERSIÓN CORREGIDA)
# =========================
def cargar_encoding(ruta_imagen, nombre):
    try:
        # 🔥 usar face_recognition directamente (evita TODOS los errores anteriores)
        imagen = face_recognition.load_image_file(ruta_imagen)

    except Exception as e:
        print(f"Error cargando {ruta_imagen}: {e}")
        return None

    encodings = face_recognition.face_encodings(imagen)

    if len(encodings) == 0:
        print(f"No se detectó rostro en {ruta_imagen}")
        return None

    print(f"Rostro cargado correctamente: {nombre}")
    return encodings[0]


# =========================
# RUTAS AUTOMÁTICAS
# =========================
BASE_DIR = os.path.dirname(__file__)

jobs_path = os.path.join(BASE_DIR, "photos", "jobs.png")
mark_path = os.path.join(BASE_DIR, "photos", "mark.png")
tesla_path = os.path.join(BASE_DIR, "photos", "tesla.png")

# =========================
# CARGAR PERSONAS
# =========================
known_face_encodings = []
known_face_names = []

jobs_encoding = cargar_encoding(jobs_path, "Jobs")
mark_encoding = cargar_encoding(mark_path, "Mark")
tesla_encoding = cargar_encoding(tesla_path, "Tesla")

if jobs_encoding is not None:
    known_face_encodings.append(jobs_encoding)
    known_face_names.append("Jobs")

if mark_encoding is not None:
    known_face_encodings.append(mark_encoding)
    known_face_names.append("Mark")

if tesla_encoding is not None:
    known_face_encodings.append(tesla_encoding)
    known_face_names.append("Tesla")


if len(known_face_encodings) == 0:
    print("❌ Error: no se cargó ningún rostro")
    exit()

# =========================
# INICIAR CÁMARA
# =========================
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("❌ Error: no se pudo abrir la cámara")
    exit()

print("🎥 Cámara iniciada. Presiona Q para salir.")

# =========================
# LOOP PRINCIPAL
# =========================
while True:
    ret, frame = video_capture.read()

    if not ret:
        print("Error al capturar video")
        break

    # Reducir tamaño (más rápido)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convertir BGR → RGB
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detectar rostros
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):

        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        name = "Desconocido"

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        # Escalar coordenadas
        top, right, bottom, left = face_location
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Dibujar cuadro
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Dibujar nombre
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1)

    # Mostrar ventana
    cv2.imshow("Reconocimiento Facial", frame)

    # Salir con Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =========================
# CERRAR TODO
# =========================
video_capture.release()
cv2.destroyAllWindows()