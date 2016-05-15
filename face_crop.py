import cv2
import glob

# cascPath = "../../data/haarcascades/haarcascade_frontalface_alt.xml"
cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

files=glob.glob("*.png")
for file in files:

    # Read the image
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        # flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    print "Found {0} face(s)!".format(len(faces))

    # Crop Padding
    left = 10
    right = 10
    top = 10
    bottom = 10

    if len(faces) == 0:
        cv2.imshow('img',image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            print x, y, w, h

            # Debugging boxes
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]

        cv2.imshow('img',image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


            # image  = image[y-top:y+h+bottom, x-left:x+w+right]

            # print "cropped_{1}{0}".format(str(file),str(x))
            # cv2.imwrite("cropped_{1}_{0}".format(str(file),str(x)), image)