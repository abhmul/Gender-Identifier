import cPickle as pickle
import gzip
import numpy as np
from PIL import Image
import os

size = (128,128)
num_pics = 3896

def im2array(img):
    return np.divide(np.array(img.getdata(), np.uint8), 255.0)


def pickle_images(size, num_pics, train_percent=.7, val_percent=.15):

    train_size = int(round(train_percent*num_pics))
    val_size = int(round(val_percent*num_pics))
    test_size = num_pics - train_size - val_size

    training_images = np.empty(train_size)
    training_outputs = np.empty(train_size)
    validation_images = np.empty(val_size)
    validation_outputs = np.empty(val_size)
    test_images = np.empty(test_size)
    test_outputs = np.empty(test_size)

    count = 0

    for i in os.listdir(os.getcwd()):
        if i.endswith(".png"):
            img = Image.open(i).convert('L')
            img = img.resize(size)
            # REMEMBER to add outputs to list
            img = im2array(img)
            if count <= train_size:
                np.append(training_images, img)
            elif count <= train_size + val_size:
                np.append(validation_images, img)
            else:
                np.append(test_images, img)
            count += 1



