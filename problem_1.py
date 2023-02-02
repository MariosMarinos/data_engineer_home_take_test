import cv2
import numpy as np
from PIL import Image
import os
import imghdr
import sys


def detect_faces(image_path, save_dir):
    # Load the cascade classifier from OpenCV's library
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # Read the input image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image)
    # Save the headshots of the detected faces
    count = 1
    for (x, y, w, h) in faces:
        # faces contains the coordinates of each face.
        face = image[y : y + h, x : x + w]
        # resized and converted from BGR to RBG so it's easier to visualize.
        face = cv2.resize(face, (224, 224))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        # This way we can save it using PIL library as .jpg.
        face = Image.fromarray(face)
        face.save(os.path.join(save_dir, "face_{}.jpg".format(count)))
        count += 1

    return len(faces)


# Test the script with an example image
if __name__ == "__main__":
    # image_path = "example.png"
    # save_dir = "headshots"
    if len(sys.argv) < 3:
        print("Usage: python script.py [image_path] [save_dir_path]")
        sys.exit(1)
    image_path = sys.argv[1]
    save_dir = sys.argv[2]
    # if the
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    num_faces = detect_faces(image_path, save_dir)
    print("Number of faces detected in the image:", num_faces)
