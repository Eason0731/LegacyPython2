import re
import os
import time
import shutil

def MainFunction():
    #TestCasesDir = raw_input ("Please Input your folder Path: ")
    #s = raw_input ("Please Input what words you want to find: ")
    s= 'RP'
    #s = s.upper()
    #p = raw_input ("Please Input what words you want to replace: ")
    TestCasesDir = "C:\\Users\\t_zhanj\\Desktop\\Demo"
    if os.path.exists(TestCasesDir):
        FindMyModels(TestCasesDir,s)
    else:
        print "This folder not exist!"
        

def FindMyModels(TestCasesDir,s):
    Dir = os.listdir(TestCasesDir)       
    for myFile in Dir:
        TxtFile = os.path.join(TestCasesDir,myFile)
        
        if "txt" in myFile:
            i=0
            print "=============Start on Copy Sample Files================="
            print myFile+ " is reading"   
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
        
                if s in eachline:
                    if match:
                        filepath = match.group(2)
                        #print "Match"
                    else:  
                        filepath = ""
                        #print "Not Match"

                    search = 'RP'
                    start = 0
                    index = eachline.find(search, start)
                    index +=3 
                    #print index
                    
                    #print "file path is " + filepath[index:]
                    SubFolder = filepath[index:].split('/')[-2]
                    #print "file name is " + filename[0]
                    #print "SubFolder is " +SubFolder
                    
                    myFusionPath = r'C:\\Users\\t_zhanj\\AppData\\Local\\Autodesk\\webdeploy\\dev\\70f3c4c6ffa63f9c51e83d924d85542ac308a9bc'
                    ModelPath = os.path.join (myFusionPath,filepath[index:],filename[0])
                    #print "ModelPath is " + ModelPath

                    if os.path.exists(ModelPath):

                        TargetFolder = r'C:\\Users\\t_zhanj\\Desktop\\Cases\\ModelTestingFolder'
                        TargetFolder = os.path.join(TargetFolder,SubFolder)

                        
                        if os.path.exists(TargetFolder):         
                            print TargetFolder + " existed!"
                        else:
                            os.makedirs(TargetFolder)
                            print TargetFolder + " create success!"

                        # Copy Files use shutil copy method
                        # shutil (sourceFolder,TargetFolder)
                        CopiedModelPath = os.path.join(TargetFolder,filename[0])
                        print CopiedModelPath
                        
                        if os.path.exists(CopiedModelPath):
                            print filename[0] + " has been copied,do not need copy again!"
                            
                        else:
                            shutil.copy (ModelPath,TargetFolder)
                            #print "CopiedModelPath is " + CopiedModelPath
                            print "Copy " + filename[0]+ "  Success! "
                            
                           

                    else:
                        print "Model path " + ModelPath + " not existed!"
                        

                    
        """
            if i == 0:
                print s + " didn't found on " + myFile
            elif i == 1:
                print s + " has been found for " + str(i) + " time on " + myFile
            else:
                print s + " have been found for " + str(i) + " times on " + myFile
           """         
                
        files.close()
    print "=============Finish on Copy Sample Files================="
            


if __name__=='__main__':
    MainFunction()
