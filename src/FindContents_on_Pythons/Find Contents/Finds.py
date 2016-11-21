import os
import shutil

def FindContent(Path,Content):
    
    for root,dirnames,filenames in os.walk(Path):
        for myFile in filenames:
            TxtFile = os.path.join(root,myFile)
            #print "root is:" + root  root is the path which your file in now
            if 'txt' in myFile:
                i=0
                #print TxtFile
                f = open (TxtFile, 'r')
                Filecontent = f.readlines()
                for eachline in Filecontent:                 
                    if Content.lower() in eachline.lower():
                        i+=1
                

                if i==0:
                    print "--------------------------------------"
                elif i==1:
                    print Content + " found on " + myFile + " for " +str(i)+ " time"
                else:
                    print Content + " found on " + myFile + " for " +str(i)+ " times"
                f.close()
            else:
                print "No txt files found on folder:" + Path
                
    

if __name__ == '__main__':
    Path  = raw_input ("Please your file path:")
    Content = raw_input ("What you want to find?")
    if os.path.exists(Path):
        FindContent(Path,Content)
    else:
        print Path + " not exists!"
    
