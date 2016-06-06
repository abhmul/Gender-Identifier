import os
import requests

__author__ = 'Abhijeet Mulgund & Philip Masek'

genderedListMaledir = "genderedNamesMale.txt"
genderedListFemaledir = "genderedNamesFemale.txt"
ungenderedListdir = "ungenderedNames.txt"
fileNamesdir = "fileNames.txt"

rootdir = "../lfwcrop_grey/faces"
maleFolder = "../lfwcrop_grey/male"
femaleFolder = "../lfwcrop_grey/female"


def build_name_text(rootdir, fileNamesdir):

    fileNames = open(fileNamesdir, 'a')

    for root, subFolders, files in os.walk(rootdir):
        for file in files:
            fileNames.write(file + "\n")

    fileNames.close()


def build_gender_text(genderedListMaledir, genderedListFemaledir, maleFolder, femaleFolder):


    genderedListMale = open(genderedListMaledir, 'a')
    genderedListFemale = open(genderedListFemaledir, 'a')


    for root, subFolders, files in os.walk(maleFolder):
        for file in files:
            genderedListMale.write(file)
            genderedListMale.write("\n")

    for root, subFolders, files in os.walk(femaleFolder):
        for file in files:
            genderedListFemale.write(file)
            genderedListFemale.write("\n")


    genderedListMale.close()
    genderedListFemale.close()



def genderize(fileNamesdir, genderedListMaledir, genderedListFemaledir, ungenderedListdir):

    count = 0
    tmp = ""

    genderedListMale = open(genderedListMaledir, 'r')
    genderedListFemale = open(genderedListFemaledir, 'r')
    ungenderedList = open(ungenderedListdir, 'r')

    listMale = genderedListMale.read().split("\n")
    listFemale = genderedListFemale.read().split("\n")
    listUngendered = ungenderedList.read().split("\n")

    genderedListMale.close()
    genderedListFemale.close()
    ungenderedList.close()

    fileSet = set(listMale + listFemale + listUngendered)

    fileNames = open(fileNamesdir, 'r')

    files = fileNames.read().split("\n")

    fileNames.close()

    for file in files:
        fileSplit = file.split("_")

        if file not in fileSet:
            count += 1

            if tmp != fileSplit[0]:
                result = requests.get("http://api.genderize.io?name=%s" % fileSplit[0])
                result = result.json()
                tmp = fileSplit[0]
            else:
                tmp = fileSplit[0]

            genderedListMale = open(genderedListMaledir, 'a')
            genderedListFemale = open(genderedListFemaledir, 'a')
            ungenderedList = open(ungenderedListdir, 'a')

            try:
                if float(result['probability']) > 0.9:
                    if result['gender'] == 'male':
                        genderedListMale.write(file + "\n")
                    elif result['gender'] == 'female':
                        genderedListFemale.write(file + "\n")
                    fileSet.add(file)
            except Exception as e:
                if 'error' in result.keys():
                    print result['error']
                    return None
                print result['name']
                ungenderedList.write(file + "\n")

            print count

    genderedListMale.close()
    genderedListFemale.close()
    ungenderedList.close()

    print "All files have been genderized"

genderize(fileNamesdir, genderedListMaledir, genderedListFemaledir, ungenderedListdir)