import os

def ReplaceFileNameWithSpecificName(PerfResultDir,FindContent,ReplaceContent): 
    for root,dirs,filenames in os.walk(PerfResultDir):
        for myFile in filenames:
            myFile = myFile.lower() #Convert the root path to lower  
            if FindContent in myFile:
                OldNameFile = os.path.join(root,myFile)
                myFile = myFile.replace (FindContent,ReplaceContent)
                NewNameFile = os.path.join(root,myFile)
                os.rename (OldNameFile,NewNameFile) #rename function
                if os.path.exists(NewNameFile):
                    print OldNameFile +" has been replaced as " + NewNameFile + " Successfully!"
                    print "========================================"
            else:
                print "Didn't found target content: " + FindContent
                    


if __name__ == '__main__':
    PerfResultDir = raw_input ("Please input folder: ")
    FindContent = raw_input("What word do you want find?")
    FindContent = FindContent.lower() #Convert the FindContent path to lower
    ReplaceContent = raw_input("What word do you want replace?")
    ReplaceFileNameWithSpecificName(PerfResultDir,FindContent,ReplaceContent)
                
