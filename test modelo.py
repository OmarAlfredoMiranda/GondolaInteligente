import tensorflow as tf
import cv2
import gspread
import numpy as np
import smtplib
import imutils
import mysql.connector
from keras.models import load_model

# Load the model
model = load_model('C:/Users/Usuario/Desktop/Gondola Inteligente/keras_model.h5')

# CAMERA can be 0 or 1 based on default camera of your computer.
camera = cv2.VideoCapture("192.168.100.36")

# Grab the labels from the labels.txt file. This will be used later.
labels = open('C:/Users/Usuario/Desktop/Gondola Inteligente/labels.txt', 'r').readlines()

# Inicializar los contadores de stock y el frame anterior
stock = {}
prev_frame = None

# Connect to the MySQL database
#cnx = mysql.connector.connect(user='username', password='password', host='127.0.0.1', database='gondola')
#cursor = cnx.cursor()


while True:
    # Grab the webcameras image.
    ret, image = camera.read()
    ret, image2 = camera.read()
    # Resize the raw image into (224-height,224-width) pixels.
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    
    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Have the model predict what the current image is. Model.predict
    # returns an array of percentages. Example:[0.2,0.8] meaning its 20% sure
    # it is the first label and 80% sure its the second label.
    prediction = model.predict(image)

    # Print what the highest value probabilitie label
    print(labels[np.argmax(prediction)])
    #donde guarda el resultado de lo que esta viendo con mayor porcentaje y la IA
    resultado = labels[np.argmax(prediction)]
    
    # Show the image in a window
    #image2 = cv2.resize(image2, (224, 224))
    cv2.putText(image2, resultado, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    cv2.imshow('Webcam Image', image2),
            

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)
    
    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
