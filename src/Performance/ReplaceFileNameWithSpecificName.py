import os

def ReplaceFileNameWithSpecificName(PerfResultDir,FindContent,ReplaceContent): 
    for root,dirs,filenames in os.walk(PerfResultDir):
        for myFile in filenames:
            if 'xml' in myFile:
                #print myFile
                if FindContent in myFile:
                    OldNameFile = os.path.join(root,myFile)
                    myFile = myFile.replace (FindContent,ReplaceContent)
                    NewNameFile = os.path.join(root,myFile)
                    #print OldNameFile
                    #print NewNameFile
                    #print "========================================"
                    os.rename (OldNameFile,NewNameFile)
                    print ("ReplaceSuccess!")
                    


if __name__ == '__main__':
    PerfResultDir = raw_input ("Please input folder: ")
    FindContent = raw_input("What word do you want find?")
    ReplaceContent = raw_input("What word do you want replace?")
    ReplaceFileNameWithSpecificName(PerfResultDir,FindContent,ReplaceContent)
                
