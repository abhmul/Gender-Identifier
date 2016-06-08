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



def genderize(fileNamesdir, genderedListMaledir, genderedListFemaledir, ungenderedListdir, threshold=0.9):

    count = 0

    genderedListMale = open(genderedListMaledir, 'r')
    genderedListFemale = open(genderedListFemaledir, 'r')
    ungenderedList = open(ungenderedListdir, 'r')

    listMale = genderedListMale.read().split("\n")
    listFemale = genderedListFemale.read().split("\n")
    listUngendered = ungenderedList.read().split("\n")

    maleNames = set([(fileName.split("_"))[0] for fileName in listMale])
    femaleNames = set([(fileName.split("_"))[0] for fileName in listFemale])
    ungenderedNames = set([(fileName.split("_"))[0] for fileName in listUngendered])

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

            genderedListMale = open(genderedListMaledir, 'a')
            genderedListFemale = open(genderedListFemaledir, 'a')
            ungenderedList = open(ungenderedListdir, 'a')



            if fileSplit[0] in maleNames:
                genderedListMale.write(file + "\n")
                print fileSplit[0], " placed in MALES"
                print "No Call"

            elif fileSplit[0] in femaleNames:
                genderedListFemale.write(file + "\n")
                print fileSplit[0], " placed in FEMALES"
                print "No Call"
            elif fileSplit[0] in ungenderedNames:
                ungenderedList.write(file + "\n")
                print fileSplit[0], " placed in UNGENDERED"
                print "No Call"
            else:
                result = requests.get("http://api.genderize.io?name=%s" % fileSplit[0])
                print result.headers
                result = result.json()
                print "API was called for ", fileSplit[0]
                if 'error' not in result.keys() and 'gender' in result.keys():
                    print result['probability'], "  ", result['gender']

                    if float(result['probability']) > threshold:
                        if result['gender'] == 'male':
                            genderedListMale.write(file + "\n")
                            maleNames.add(fileSplit[0])
                            print fileSplit[0], " placed in MALES"

                        elif result['gender'] == 'female':
                            genderedListFemale.write(file + "\n")
                            femaleNames.add(fileSplit[0])
                            print fileSplit[0], " placed in FEMALES"
                else:
                    try:
                        print result['name']
                        ungenderedList.write(file + "\n")
                        ungenderedNames.add(fileSplit[0])
                        print fileSplit[0], " placed in UNGENDERED"

                    except:
                        print result['error']
                        return None



            fileSet.add(file)

            print count, "\n"
            # if count > 1:
            #     return None

    genderedListMale.close()
    genderedListFemale.close()
    ungenderedList.close()

    print "All files have been genderized"

genderize(fileNamesdir, genderedListMaledir, genderedListFemaledir, ungenderedListdir)