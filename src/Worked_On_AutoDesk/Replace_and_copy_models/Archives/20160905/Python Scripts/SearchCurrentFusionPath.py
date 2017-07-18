import os

def SearchFusionPath():
    Dir = os.path.join (os.environ['localappdata'],'Autodesk','webdeploy')

    if os.path.exists(Dir):
        for root,dirs,filenames in os.walk(Dir):
            for myFile in filenames:
                if 'Fusion360.exe' in myFile:
                    FusionPath = root
                    #print "FusionPath is: " + FusionPath
                    #print "Filename is " + myFile
                    #print "The Full Path of Fusion on your disk is: " + os.path.join(FusionPath,myFile)
                    return FusionPath
    else:
        print "Your Computer didn't install Fusion"

if __name__ == '__main__':
    print SearchFusionPath()
    
    
