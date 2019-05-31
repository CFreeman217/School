import io
import picamera
import cv2
import numpy

# Create a memory stream so photos don't need to be saved in a file
stream = io.BytesIO()

# Get the picture (low resolution for speed)
# Also specify picture parameters here, like rotation
with picamera.PiCamera() as camera:
    camera.resolution = (320,240)
    camera.capture(stream, format='jpeg')

# Convert the picture into a numpy array
buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

# Create an OpenCV image
image = cv2.imdecode(buff, 1)

# Load a cascade file for detecting faces
face_cascade = cv2.cascadeClassifier('/usr/share/opencv/haarcascaes/haarcascade_frontalface_alt.xml')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Look for faces in the image using the loaded cascade file
faces = face_cascade.detectMultiScale(gray, 1.1, 5)

print("Found {} faces".format(str(len(faces))))

# Draw a rectangle aroundn every found face
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x,y), (x+w, y+h),(255,0,0), 2)

# Save the result image
cv2.imwrite('result.jpg, image')