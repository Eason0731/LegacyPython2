"""<pre name="code" class="python">1. Regular Expression  
^([a-zA-Z]:|/\\[a-zA-Z0-9_.$ -]+\\[a-z0-9_.$ -]+)?((?:\\|^)(?:[^//:*?"<>|\r\n]+\\)+)  
  
eg.  
c:\folder\subfolder\file.ext  
  
Extract:  
\folder\subfolder\  
  
\\server\share\folder\subfolder\file.ext  
  
Extract:  
\folder\subfolder\  


#2. Python code  Demo 
import re  
subject = 'c:\\folder\\subfolder\\subfolder2\\file.ext'
#abc = "ASASASSASAS FDFDFDDF SDDSSDDSDS 922 RP=Fusion/Test/Dataset/Abc.f3d"
match = re.search(r'^^([a-zA-Z]:|/\\[a-zA-Z0-9_.$ -]+\\[a-z0-9_.$ -]+)?((?:\\|^)(?:[^//:*?"<>|\r\n]+\\)+)', subject)
#extname = re.findall(r'\[^.\\/:*?"<>|\r\n]+$', subject)
filename = re.findall(r'[^\\/:*?"<>|\r\n]+$', subject)
#match = re.search(r'^([a-zA-Z]:|//[a-zA-Z0-9_.$ -]+/[a-z0-9_.$ -]+)?((?:/|^)(?:[^//:*?"<>|\r\n]+/)+)', subject)
if match:  
    filepath = match.group(2)  
else:  
    filepath = ""  
  
print filepath
#print extname
print filename
"""
#3. RP Open Model
import re
import os
import time
import shutil

def CopySampleFiles():
    #subject1 = 'NuCommands.OpenDocumentCmd'
    #subject = 'Commands.SetFileString infoOpenFile "RP=Fusion/Test/Dataset/Smoke/Airplane.DXF"'
    txtfile = r'C:\\Users\\t_zhanj\\Desktop\\Demo\\models.txt'
    subject = open(txtfile,'r')
    subject = subject.read()
    #Remove " for search RP
    subject = subject.replace('"','')
    
    print subject
    print "======================================================================="
    match = re.search(r'^([a-zA-Z]:|//[a-zA-Z0-9_.$ -]+/[a-z0-9_.$ -]+)?((?:/|^)(?:[^//:*?"<>|\r\n]+/)+)', subject)
    extname = re.findall(r'\[^.\\/:*?"<>|\r\n]+$', subject)
    filename = re.findall(r'[^\\/:*?"<>|\r\n]+$' , subject)

    #myString = "RP"
    #myString = myString.lower()
    
    #for subject in subjects:
    #for c in subject:
    if 'RP' in subject:
        if match:
            filepath = match.group(2)  
        else:  
            filepath = ""

        #Use method find to find the index of what you want to search.Here I found word:RP
        search = 'RP'
        start = 0
        
        index = subject.find(search, start) 
        #print( "%s found at index %d"  % (search, index) )

        #print filepath[3:]
        #Should add 3 to get the real path of model,RP in 27,should get it start after "RP=" that add 3 index
        index +=3 

        #print filepath[index:]

        #Use split to get the model from which type
        TypeFolder = filepath[index:].split('/')[-2]

        #print "Subfolder name is: " + TypeFolder
        #get the name without [''] on list
        #print filename[0] 
        #print filename
        
        FusionPath = r"C:\Users\t_zhanj\AppData\Local\Autodesk\webdeploy\dev\951cd82a7a1d4800ad6002e13cca5a13dedde56d" # Your Fusion Path
        ModelPath = os.path.join (FusionPath,filepath[index:],filename[0]) #filename[0]
        ModelPath = ModelPath.replace("\\",'/')

        #print "ModelPath: " +ModelPath

        #modelpath = os.path.join (FusionPath, filename[0])
        if os.path.exists(ModelPath):
            print "exists!"
        else:
            print ModelPath + " not exists!"

        targetFolder = "C:\\Users\\t_zhanj\\Desktop\\Cases\\ModelTest"
        targetFolder = os.path.join(targetFolder,TypeFolder)
        #targetFolder = targetFolder.replace ("\\",'/')
        print targetFolder
        
        if not os.path.exists (targetFolder):
            #Makedirs can create multi level folder
            #mkdir only crate one level folder
            os.makedirs (targetFolder)

        shutil.copy(ModelPath, targetFolder)        
        NewModelPath = os.path.join(targetFolder,filename[0])
        
        if os.path.exists(NewModelPath):
            print "Copy Success!"
        else:
            print "Copy Failed"
        
                
        

if __name__=='__main__':
    CopySampleFiles()
    

    
    

