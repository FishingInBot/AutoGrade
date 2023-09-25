import os
from zipfile import ZipFile
import glob
import shutil
import errno

#Class level things
defaultLocation = "Desktop\Grading"
#note that this assumes you want C:\Users\[current user]\ BEFORE this text.

IDEALocation = os.path.join(os.environ['USERPROFILE'], "IdeaProjects\Grading")
#This should be the location where you want the src folder to be in.

standardNaming = True
#this means that folders in the submission folder have the standard naming scheme for canvas. This ought to look like "name_some-ID_some-ID_name-of-file"
#the important part is the name is first, and is followed by a '_' character.

def setFileLocation():
    # Take some input as the where submissions are (probably want a default spot)
    fileLocation = input("Enter location of submission files (nothing for default): \n")
    if (fileLocation == ""):
        fileLocation = os.path.join(os.path.join(os.environ['USERPROFILE']), defaultLocation)

    return fileLocation

def unzip(location):
    #Unzip any submissions
    #TODO maybe combine ones with same name?
    files = glob.glob(location+".*(\.zip)")
    for file in files:
        filename = file.replace(location,"")
        filename = filename.replace(".zip", "")
        with ZipFile(file) as zipper:
            zipper.extractall(path=location+filename)
        os.remove(file)

def openSubmissions(location):
    for dir, subdir, file in os.walk(IDEALocation):
        if "src" in subdir:
            shutil.rmtree(os.path.join(IDEALocation,"src"))

    submissions = next(os.walk(location))[1]
    for submission in submissions:
        if ".zip" in submission:
            submissions.remove(submission)
        proceed = ""
        srcFolder = ""

        for dirpath, subdirs, files in os.walk(os.path.join(location,submission)):
            for x in subdirs:
                if "src" in x and "MACOSX" not in dirpath:
                    srcFolder = os.path.join(dirpath, x)
        if srcFolder == "":
            print("Unable to find src folder in directory: " + submission)
            proceed = "yes"
            os.mkdir(os.path.join(IDEALocation,"src"))

        else:
            shutil.copytree(srcFolder, os.path.join(IDEALocation,os.path.basename(srcFolder)))
            print("Now looking at submission: " + srcFolder.replace(location+"\\", "").replace("\\src", ""))

        while proceed != "yes":
            proceed = input("Type yes to continue: ")
        
        #Now to reset for next submission
        shutil.rmtree(os.path.join(IDEALocation,"src"))

def main():
    fileLocation = setFileLocation()
    unzip(fileLocation)
    openSubmissions(fileLocation)
    print("\n")
    print("-----DONE GRADING-----\n")

if __name__ == "__main__":
    main()