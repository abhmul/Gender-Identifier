import cv2
import glob
import os

# cascPath = "../../data/haarcascades/haarcascade_frontalface_alt.xml"
cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

files=glob.glob("*.png")
for file in files:

    # Read the image
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = []
    deg = 0
    scale_factors = [1.02, 1.05, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0]

    # Keep on rotating picture until face is found
    while len(faces)!=1 and deg <= 360:

        # Rotate the image
        if deg != 0:
            rows,cols, ch = image.shape
            M = cv2.getRotationMatrix2D((cols/2,rows/2),deg,1)
            dst = cv2.warpAffine(image,M,(cols,rows))

            # Show the image
            # cv2.imshow('img',dst)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

        for scale_factor in scale_factors:
            # Detect faces in the image
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=scale_factor,
                minNeighbors=5,
                minSize=(30, 30)
                # flags = cv2.cv.CV_HAAR_SCALE_IMAGE
            )

            if len(faces) == 1:
                break

        # Increment degree by 15 for each iteration
        deg += 10


    print "Found {0} face(s)!".format(len(faces))

    # Use dst as image if it was rotated
    if deg > 10:
        image = dst

    # Crop Padding
    left = 0
    right = 0
    top = 0
    bottom = 0

    if len(faces) == 0:
        # cv2.imshow('img',image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        with open('NoFaces.txt', 'a') as f:
            f.write(os.path.basename(file) + '\n')

    else:
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            print x, y, w, h

            # Debugging boxes
            # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # roi_gray = gray[y:y+h, x:x+w]
            # roi_color = image[y:y+h, x:x+w]

            # cv2.imshow('img',image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            image = image[y-top:y+h+bottom, x-left:x+w+right]

            print "cropped_{1}{0}".format(str(file),str(x))
            cv2.imwrite("cropped_{1}_{0}".format(str(file),str(x)), image)

            # cv2.imshow('img',image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

        if len(faces) > 1:
            with open('MultipleFaces.txt', 'a') as f:
                f.write(os.path.basename(file) + '\n')
