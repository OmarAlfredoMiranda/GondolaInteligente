# Importar las librerías necesarias
import tensorflow as tf
import cv2
from google.oauth2.credentials import Credentials
import gspread
import numpy as np
import smtplib
import imutils
import mysql.connector
from keras.models import load_model

# Autenticar la conexión a Google Sheets
#info = {
#    #"email": "kamekase222@gmail.com",
#    #"access_token": "AIzaSyDZCWRB_DLOkBe1VNDOnf0NY5WuCOEkL-k"
#}
#creds = Credentials.from_authorized_user_info(info)
#client = gspread.authorize(creds)

# Abrir la hoja de cálculo donde se almacenarán los datos
#spreadsheet = client.open("Stock de botellas")
#worksheet = spreadsheet.get_worksheet(0)

#cnx = mysql.connector.connect(
#    user='<>',
#    password='<>',
#    host='localhost',
#    database='gondola'
#)

# Cargar el modelo de detección de objetos entrenado
model = load_model('C:/Users/Usuario/Desktop/Gondola Inteligente/keras_model.h5')


# Conectar la cámara web
camera = cv2.VideoCapture(0)

# Inicializar los contadores de stock y el frame anterior
#stock = {}
prev_frame = None
_, frame = camera.read() 
# Preprocesa el frame para que sea compatible con el modelo
frame = cv2.resize(frame, (224, 224))  # <-- Redimensiona el frame
frame = np.expand_dims(frame, axis=0)  # <-- Expandir las dimensiones

# Bucle infinito
# para procesar frames de video
while True:
   # Capturar un frame de video
   ret, frame = camera.read()

   # Usar el modelo para detectar objetos en el frame
   detections = model.predict(frame)

   # Recorrer las detecciones
   #for detection in detections:
       # Si se ha detectado una botella
       #if detection["class"] == "bottle":
           # Obtener la posición de la botella en el frame
        #   x1, y1, x2, y2 = detection["box"]
        #   x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

           # Recortar la imagen de la botella
        #   bottle_image = frame[y1:y2, x1:x2]

           # Comparar la imagen de la botella con el frame anterior para ver si ha sido agregada o retirada
           #if prev_frame is not None:
           #    diff = cv2.absdiff(prev_frame, frame)
           #    mask = cv2.inRange(diff, (0, 0, 0), (50, 50, 50))
           #    mask = cv2.bitwise_not(mask)
           #    mask = cv2.dilate(mask, None, iterations=2)
           #    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
           #    cnts = imutils.grab_contours(cnts)
           #    for c in cnts:
           #        if cv2.contourArea(c) < 500:
           #            continue
                   # Si se ha detectado un cambio significativo en el frame, asumir que se ha agregado o retirado una botella
           #        change_detected = True

           # Si se ha detectado un cambio, actualizar el stock en la hoja de cálculo de Google Sheets
           #if change_detected:
               # Obtener el SKU de la botella utilizando otro modelo de inteligencia artificial entrenado para reconocimiento de imágenes
              # sku = image_recognition_model.predict(bottle_image)

               # Aument
               # de cada SKU en el stock y almacenar el tiempo de la actualización en la hoja de cálculo
              # if sku in stock:
               #    stock[sku] += 1
               #else:
               #    stock[sku] = 1
               #worksheet.update_cell(sku, 2, stock[sku])
               #worksheet.update_cell(sku, 3, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

               # Revisar si el stock de algún SKU ha llegado a un nivel mínimo o máximo y enviar una alerta si es necesario
               #check_stock_levels(stock)

           # Actualizar el frame anterior
           #prev_frame = frame

# Función para revisar si el stock de algún SKU ha llegado a un nivel mínimo o máximo y enviar una alerta si es necesario
#def check_stock_levels(stock):
#    for sku, count in stock.items():
        # Leer el stock mínimo y máximo para el SKU de la hoja de cálculo
#        min_stock = worksheet.cell(sku, 4).value
#        max_stock = worksheet.cell(sku, 5).value

        # Si el stock ha llegado a un nivel mínimo o máximo, enviar una alerta por correo electrónico
#        if count <= min_stock:
#            send_email_alert("Stock bajo para el SKU " + sku, "El stock actual es de " + str(count) + " unidades")
#        elif count >= max_stock:
#            send_email_alert("Stock alto para el SKU " + sku, "El stock actual es de " + str(count) + " unidades")

# Función para enviar una alerta por correo electrónico
#def send_email_alert(subject, message):
#    server = smtplib.SMTP("smtp.gmail.com", 587)
#    server.starttls()
#    server.login("tu_dirección@gmail.com", "tu_contraseña")
#    msg = MIMEText(message)
#    msg['Subject'] = subject
#    msg['From'] = "tu_dirección@gmail.com"
#    msg['To'] = "dirección_de_destino@gmail.com"
#    server.send_message(msg)
#    server.quit()
