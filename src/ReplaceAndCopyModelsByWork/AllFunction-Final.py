import os
import re
import shutil
import time

def MainFunction():
    a = raw_input ("""
1. Replace Content on Folder
2. Copy Models

Press Any Key to Exit
        
Please choose : """)
    if (a == "1" or a == "2"):
        
        TestCasesDir = raw_input ("Please Input your folder Path: ")

        if a == "1":
            s = raw_input("Please Input what words you want to find: ")
            p = raw_input("Please Input what words you want to replace: ")

            #TestCasesDir = "C:\\Users\\t_zhanj\\Desktop\\Cases"
            if os.path.exists(TestCasesDir):
                ReplaceContentOnDir(TestCasesDir,s,p)
            else:
                print "This folder not exist!"
                CountineOrExit()
                
        if a == "2":
            s = " RP=" #s = " RP="
            if os.path.exists(TestCasesDir):
                CopyMyModels(TestCasesDir,s)
            else:
                print "This folder not exist!"
                CountineOrExit()
            
    else:
        exit(0)

def ReplaceContentOnDir(TestCasesDir,s,p):
    #Dir = os.listdir(TestCasesDir)
    """
    for myFile in Dir:
        TxtFile = os.path.join(TestCasesDir,myFile)
    """
    for root,dirnames,filenames in os.walk(TestCasesDir):
        for myFile in filenames:
            TxtFile = os.path.join(root,myFile)
            #print "root is:" + root  root is the path which your file in now
            if "txt" in myFile:       
                #print "File Path is: " + TxtFile #Show the txt file path(Should open this)
                #print "File Name is: " + myFile #Show the txt file name
                #print "the full name of the file is:" + os.path.join(parent,myFile)
                
                print "================================ Start ================================"
                print "File on " + TxtFile   
                files = open (TxtFile,'r') #read mode
                content = files.read()
                #print content
                files.close()
                # OK
                
                if s in content:
                    print "Found word: " + s + " in File " + myFile
                
                    files = open (TxtFile,'w') # write mode
                    files.writelines(content.replace (s, p))
                    files.close()
                    print s + " has been replaced as " + p + " Success!"
                
                    #f = open (TxtFile,'r')
                    #content = f.read()
                    #f.close()
                
                
                else:
                    print s + " Not found on File!"
                    
                files.close()
                print "================================ Finish ==============================="
                print "                                                                       "
                
                
    CountineOrExit()

def CopyMyModels(TestCasesDir,s):
    """Dir = os.listdir(TestCasesDir)
    for myFile in Dir:
        
        TxtFile = os.path.join(TestCasesDir,myFile)
    """
    i=0
    for root,dirnames,filenames in os.walk(TestCasesDir):
        for myFile in filenames:
            TxtFile = os.path.join(root,myFile)
            if "txt" in myFile:          
                flag = False
                print "=============Start on Copy Sample Files================="
                print "                                                        "
                print "Current file: " +TxtFile
                i+=1
                print "                                                        "
                files = open (TxtFile,'r') #read mode

                AllLines = files.readlines()
                #print AllLines,type(AllLines)

                # Use Readlines to read all content on txt file and for cycle to convert to str type 
                for eachline in AllLines:
                    #replace " as space in order to clear some noise
                    eachline = eachline.replace('"','') 
                    #print eachline
                    match = re.search(r'^([a-zA-Z]:|//[a-zA-Z0-9_.$ -]+/[a-z0-9_.$ -]+)?((?:/|^)(?:[^//:*?"<>|\r\n]+/)+)', eachline)
                    extname = re.findall(r'\[^.\\/:*?"<>|\r\n]+$', eachline)
                    filename = re.findall(r'[^\\/:*?"<>|\r\n]+$' , eachline)
                

                    if eachline.startswith('#'): #Find content start with '#' then replace it
                        eachline = eachline.replace(eachline,'---------------------')
                    
                    if s in eachline:
                        if match:
                            filepath = match.group(2)
                        
                        else:  
                            filepath = ""     
                        
                        
                        #Use method find to find the index of what you want to search.Here I found word:RP
                        search = s
                        start = 0
                        index = eachline.find(search, start)
                        #Should add 4 to get the real path of model, " RP=" (with a space) in 26,should get it start after "RP=" that add 3 index
                        index +=4 
                        

                        #Use split to get the model from which type
                        #print "file path is " + filepath[index:]
                        SubFolder = filepath[index:].split('/')[-2]
                        #print "file name is " + filename[0]
                        
                    
                        #myFusionPath = r'C:\Users\t_zhanj\AppData\Local\Autodesk\webdeploy\dev\51fa16fa02f6d2e24281c8a1a7a00720db41c203'
                        myFusionPath = SearchFusionPath()
                        #print myFusionPath
                        ModelPath = os.path.join (myFusionPath,filepath[index:],filename[0])
                        #print "ModelPath is " + ModelPath

                        if os.path.exists(ModelPath):

                            TargetFolder = r'C:\\Users\\t_zhanj\\Desktop\\John Folder\\Python Scripts\\For replace and move models\\Cases\\Modeling'
                            TargetFolder = os.path.join(TargetFolder,SubFolder)

                        
                            if os.path.exists(TargetFolder):
                                #print TargetFolder + " existed!"
                                print "                                                        "
                            else:
                                #Makedirs can create multi level folder,mkdir only crate one level folder
                                os.makedirs(TargetFolder)

                            # Copy Files use shutil copy method
                            # shutil (sourceFolder,TargetFolder)
                            CopiedModelPath = os.path.join(TargetFolder,filename[0])
                        
                            if os.path.exists(CopiedModelPath):
                                #get the name without [''] on list,so use filename[0]
                                print filename[0] + " has been copied,do not need copy again!"
                            
                            else:
                                shutil.copy (ModelPath,TargetFolder)
                                #get the name without [''] on list,so use filename[0]
                                print "Copy " + filename[0]+ " Success! "
                        
                        print "                                                         " 

                        files.close()        
                        flag = True #set the flag to true as key word RP has been found on file. That's means contain models

                if flag == False:
                    print "There is no sample model files on " + myFile

                print "=============Finish on Copy Sample Files================="
                print "                                                         "
        #print "We Detected there are " +str(i)+ " cases on this folder"
    CountineOrExit()

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

def CountineOrExit():
    IsExit = raw_input ("Countine(Y) or Exit(N)? ")
    while(1):
        if IsExit.upper() == "Y":
            MainFunction()
        elif IsExit.upper() == "N":
            exit(0)
        else:
            print "You have inputed the illegal character,try again!"
            CountineOrExit()
            break
            
            
            
if __name__=='__main__':
    MainFunction()

    

