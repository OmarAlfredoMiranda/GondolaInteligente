import cv2
import tensorflow
import numpy as np
import mysql.connector
import smtplib
from keras.models import load_model



# Cargar el modelo de OpenCV
#model = cv2.dnn.readNetFromTensorflow('C:/Users/Usuario/Desktop/Gondola Inteligente/Tests/keras_model.h5')
model = load_model('C:/Users/Usuario/Desktop/Gondola Inteligente/Tests/keras_model.h5')

# Abrir la conexión con la cámara web
camera = cv2.VideoCapture(0)
labels = open('C:/Users/Usuario/Desktop/Gondola Inteligente/Tests/labels.txt', 'r').readlines()

# Connect to the MySQL database
#cnx = mysql.connector.connect(user='username', password='password', host='127.0.0.1', database='gondola')
#cursor = cnx.cursor()



while True:
  # Capture frame-by-frame
    _, frame = frame.read()

  # Redimensionar el frame a (224, 224) píxeles
    frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
  
  # Create a 4D blob from a frame.
    blob = cv2.dnn.blobFromImage(frame, size=(224, 224), ddepth=cv2.CV_8U)

  # Run the model on the frame.
    model.setInput(blob)
    prediction = model.forward()

  # Get the class with the highest probability.
    index = np.argmax(prediction)
    label = labels[index]
    label = label.strip()

  # Display the label and the probability.
    label_text = "{}: {:.2f}%".format(label, prediction[0][index] * 100)
    cv2.putText(frame, label_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

  # Show the image in a window
    cv2.imshow('Webcam', frame)

  # Check if the user pressed the 'Esc' key.
    if cv2.waitKey(1) == 27:
        break

# Release the camera and destroy all windows.
camera.release()
cv2.destroyAllWindows()
