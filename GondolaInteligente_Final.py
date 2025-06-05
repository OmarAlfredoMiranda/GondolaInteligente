# Importar las librerías necesarias
import tensorflow as tf
import cv2
import gspread
import numpy as np
import smtplib
import imutils
import mysql.connector
from keras.models import load_model

# Cargar el modelo de detección de objetos entrenado
model = load_model('C:/Users/Usuario/Desktop/Gondola Inteligente/Tests/keras_model.h5')
labels = open('C:/Users/Usuario/Desktop/Gondola Inteligente/labels.txt', 'r').readlines()
# Conectar la cámara web
camera = cv2.VideoCapture(0)

# Inicializar los contadores de stock y el frame anterior
stock = {}
prev_frame = None

# Inicializar la conexión a la base de datos
cnx = mysql.connector.connect(
    user='root',
    password='',
    host='127.0.0.1',
    database='gondola'
)
cursor = cnx.cursor()

# Bucle infinito para procesar frames de video
while True:
   # Capturar un frame de video
   ret, frame = camera.read()
   frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
   input_frame = np.asarray(frame, dtype=np.float32).reshape(1, 224, 224, 3)

   # Usar el modelo para detectar objetos en el frame
   detections = model.predict(input_frame)
   #np.expand_dims(frame, axis=0)

   # Imprimir la etiqueta con mayor probabilidad en lugar del índice de la etiqueta
   print(labels[np.argmax(detections)])

   # Recorrer las detecciones
   for detection in detections:
       # Si se ha detectado una botella
       if detection[0] == "2 beefeater de litro":
           # Obtener la posición de la botella en el frame
           x1, y1, x2, y2 = detection["box"]
           x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

           # Dibujar un recuadro alrededor del objeto detectado
           cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

           # Recortar la imagen de la botella
           bottle_image = frame[y1:y2, x1:x2]

           # Normalizar la imagen de la botella
           bottle_image = (bottle_image / 127.5) - 1

           # Valor inicial para detectar cambios en el frame
           change_detected = False

           # Comparar la imagen de la botella con el frame anterior para ver si ha sido agregada o retirada
           if prev_frame is not None:
               diff = cv2.absdiff(prev_frame, frame)
               mask = cv2.inRange(diff, (0, 0, 0), (50, 50, 50))
               mask = cv2.bitwise_not(mask)
               mask = cv2.dilate(mask, None, iterations=2)
               cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
               cnts = imutils.grab_contours(cnts)
               for c in cnts:
                   if cv2.contourArea(c) < 500:
                       continue
                   # Si se ha detectado un cambio significativo en el frame, asumir que se ha agregado o retirado una botella
                   change_detected = True

           # Si se ha detectado un cambio, actualizar el contador de stock y la base de datos
           if change_detected:
               # Incrementar o decrementar el contador de stock en función de si se ha agregado o retirado una botella
               if detection[0] in stock:
                   stock[detection[0]] += 1
               else:
                   stock[detection[0]] = 1
               # Actualizar la base de datos con el nuevo contador de stock
               update_query = "UPDATE stock SET cantidad = {} WHERE sku = '{}'".format(stock[detection[0]], detection[0])
               cursor.execute(update_query)
               cnx.commit()
           # Si no se ha detectado un cambio, simplemente añadir la botella al diccionario de stock
           else:
               if detection[0] in stock:
                   stock[detection[0]] += 1
               else:
                   stock[detection[0]] = 1

   # Mostrar el contador de stock en pantalla
   for key in stock:
       cv2.putText(frame, "{}: {}".format(key, stock[key]), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

   # Mostrar el frame en pantalla
   #frame = cv2.resize(frame, (224, 224))
   #frame = cv2.convertScaleAbs(frame)

   cv2.imshow("Frame", frame)
   key = cv2.waitKey(1) & 0xFF

   # Si se ha pulsado la tecla 'q', detener el bucle
   if key == ord("q"):
       break

   # Actualizar el frame anterior
   prev_frame = frame

# Liberar la cámara y cerrar todas las ventanas abiertas
camera.release()
cv2.destroyAllWindows()

# Cerrar la conexión a la base de datos
cursor.close()
cnx.close()
