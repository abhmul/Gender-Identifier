import cPickle as pickle
import gzip
import numpy as np
from PIL import Image
import os
import random

size = (128,128)
num_pics = 3896

def im2array(img):
    return np.divide(np.array(img.getdata(), dtype='float32'), 255)

def gzip_compress(filename):
    file = open(filename, 'rb')
    zip_filename = filename + '.gz'
    zipped = gzip.open(zip_filename, 'wb')
    zipped.writelines(file)
    zipped.close()
    file.close()



def pickle_images(size, num_pics, output_file='PictureGenders.txt', train_percent=.7, val_percent=.15, resize=True, lfw=False, genderedListMaledir="genderedMaleNamesReduced.txt", genderedListFemaledir="genderedFemaleNamesReduced.txt"):

    train_size = int(round(train_percent*num_pics))
    val_size = int(round(val_percent*num_pics))
    test_size = num_pics - train_size - val_size
    unwrapped = size[0]*size[1]

    print 'Initializing Arrays'

    training_images = np.empty([train_size, unwrapped], dtype='float32')
    training_outputs = np.empty(train_size, dtype='bool')
    validation_images = np.empty([val_size, unwrapped], dtype='float32')
    validation_outputs = np.empty(val_size, dtype='bool')
    test_images = np.empty([test_size, unwrapped], dtype='float32')
    test_outputs = np.empty(test_size, dtype='bool')

    count = 0

    print 'Writing Images into Arrays'

    if lfw:
        glmd = open(genderedListMaledir)
        glfd = open(genderedListFemaledir)
        males = set(glmd.read().split("\n")).difference({""})
        females = set(glfd.read().split("\n")).difference({""})
        glmd.close()
        glfd.close()
        files = list(males.union(females))
        random.shuffle(files)
        # print files[-1]

        for i in files:
            if i == "":
                print "WWERWERA"
            img = Image.open("../lfwcrop_grey/faces/" + i).convert('L')
            img = im2array(img)
            if count < train_size:
                training_images[count] = img
            elif count < train_size + val_size:
                validation_images[count-train_size] = img
            else:
                test_images[count-train_size-val_size] = img


            gender = (i in males)

            if count < train_size:
                training_outputs[count] = gender
            elif count < train_size + val_size:
                validation_outputs[count-train_size] = gender
            else:
                test_outputs[count-train_size-val_size] = gender
            count += 1

    else:
        for i in os.listdir(os.getcwd()):
            if i.endswith(".png"):
                img = Image.open(i).convert('L')
                if resize:
                    img = img.resize(size)
                # REMEMBER to add outputs to list
                img = im2array(img)
                if count < train_size:
                    training_images[count] = img
                elif count < train_size + val_size:
                    validation_images[count-train_size] = img
                else:
                    test_images[count-train_size-val_size] = img
                count += 1


        print 'Reading outputs file'

        file_outputs = open(output_file)

        print 'Writing Outputs into Array'

        count=0
        for line in file_outputs:
            gender = bool(int(line))
            if count < train_size:
                training_outputs[count] = gender
            elif count < train_size + val_size:
                validation_outputs[count-train_size] = gender
            else:
                test_outputs[count-train_size-val_size] = gender
            count += 1

        file_outputs.close()

    training_set = (training_images, training_outputs)
    validation_set = (validation_images, validation_outputs)
    test_set = (test_images, test_outputs)

    print 'Pickling Data Set'

    pickle.dump((training_set, validation_set, test_set), open('genders_lfw.pkl', 'wb'))

    print 'Gzip compressing pickled dataset'

    gzip_compress('genders_lfw.pkl')

size_lfw = (64,64)

genderedListMaledir = "genderedMaleNamesReduced.txt"
genderedListFemaledir = "genderedFemaleNamesReduced.txt"
ungenderedListdir = "ungenderedNames.txt"
glmd = open(genderedListMaledir)
glfd = open(genderedListFemaledir)
num_pics_lfw = len(set(glmd.read().split("\n")).union(set(glfd.read().split("\n"))).difference({""}))
glmd.close()
glfd.close()
print num_pics_lfw


pickle_images(size_lfw, num_pics_lfw, resize=False, lfw=True)

