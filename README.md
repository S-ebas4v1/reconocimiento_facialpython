# Reconocimiento Facial con OpenCV y Python

Proyecto de reconocimiento facial en tiempo real desarrollado en Python utilizando OpenCV y la librería face_recognition.

El sistema permite:
- Detectar rostros desde la cámara en tiempo real.
- Reconocer múltiples personas a partir de imágenes almacenadas.
- Mostrar el nombre de la persona detectada en pantalla.

Tecnologías utilizadas:
- Python 3.10
- OpenCV
- face_recognition (dlib)
- NumPy

Características:
- Conversión correcta de imágenes a formato RGB.
- Manejo de errores en carga de imágenes.
- Lectura de imágenes desde carpeta ("photos").
- Optimización del rendimiento reduciendo el tamaño de los frames.
- Cierre seguro de la cámara mediante teclado.

Estructura del proyecto:
- program.py
- photos/
  - jobs.png
  - mark.png
  - tesla.png

Uso:
1. Colocar imágenes de referencia en la carpeta "photos".
2. Ejecutar:
   python program.py
3. Presionar "q" para cerrar la cámara.

Autor:
Sebastian Vallejo Moreno