import cv2
import numpy as np
import mysql.connector
import smtplib
from keras.models import load_model

# Cargar el modelo entrenado
model = load_model('C:/Users/Usuario/Desktop/Gondola Inteligente/keras_model.h5')

# Abre la cámara
cap = cv2.VideoCapture(0)
labels = open('C:/Users/Usuario/Desktop/Gondola Inteligente/Tests/labels.txt', 'r').readlines()

# Inicializa el conteo de botellas a 0
bottle_count = 0

while True:
    # Obtiene un frame de la cámara
    _, frame = cap.read() 
    
    # Preprocesa el frame para que sea compatible con el modelo
    frame_small = cv2.resize(frame, (224, 224))
    frame_small = np.expand_dims(frame_small, axis=0)
    
    # Realiza la predicción con el modelo
    prediction = model.predict(frame_small)
    
    # Si la predicción es mayor al 50% de certeza, se considera una botella
    if prediction[0][0] > 0.5:
        bottle_count += 1
    
    # Muestra el conteo actual en la pantalla
    cv2.putText(frame, f'Bottle count: {bottle_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Muestra el frame en la pantalla
    frame = cv2.resize(frame, (800, 600))
    cv2.imshow('Bottle counter', frame)
    
    # Si se presiona la tecla 'q', se sale del ciclo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
