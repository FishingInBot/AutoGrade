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

#DON'T TOUCH
srcLocation = os.path.join(IDEALocation,"src")
outLocation = os.path.join(IDEALocation,"out")

def setFileLocation():
    # Take some input as the where submissions are (probably want a default spot)
    fileLocation = input("Enter location of submission files (nothing for default): \n")
    if (fileLocation == ""):
        fileLocation = os.path.join(os.environ['USERPROFILE'], defaultLocation)

    return fileLocation

def unzip(location):
    #Unzip any submissions
    #TODO maybe combine ones with same name?
    files = glob.glob(root_dir=location, pathname="*.zip")
    for file in files:
        source = os.path.join(location, file)
        filename = file.replace(".zip", "")
        dest = os.path.join(location,filename)
        with ZipFile(source) as zipper:
            zipper.extractall(path=dest)
        os.remove(source)

def openSubmissions(location):
    if os.path.isdir(srcLocation):
        shutil.rmtree(srcLocation)
    if os.path.isdir(outLocation):
        shutil.rmtree(outLocation)

    submissions = next(os.walk(location))[1]
    for submission in submissions:
        if ".zip" in submission:
            submissions.remove(submission)
        proceed = ""
        srcFolder = ""

        for dirpath, subdirs, files in os.walk(os.path.join(location,submission)):
            for subdir in subdirs:
                if "src" in subdir and "MACOSX" not in dirpath:
                    srcFolder = os.path.join(dirpath, subdir)

        if srcFolder == "":
            print("Unable to find src folder in directory: " + submission)
            proceed = "yes"
        else:
            shutil.copytree(srcFolder, srcLocation)
            print("Now looking at submission: " + srcFolder.replace(location+"\\", "").replace("\\src", ""))

        while proceed != "yes":
            proceed = input("Type yes to continue: ")
        
        #Now to reset for next submission
        if os.path.isdir(srcLocation): 
            shutil.rmtree(srcLocation)
        if os.path.isdir(outLocation): 
            shutil.rmtree(outLocation)

def main():
    fileLocation = setFileLocation()
    unzip(fileLocation)
    openSubmissions(fileLocation)
    print("\n")
    print("-----DONE GRADING-----\n")

if __name__ == "__main__":
    main()