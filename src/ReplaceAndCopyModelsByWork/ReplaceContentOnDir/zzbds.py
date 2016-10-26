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
def abcd():
    subject1 = 'NuCommands.OpenDocumentCmd'
    subject = 'RP=Fusion/Test/Dataset/Sketch/Simple.f3d'
    match = re.search(r'^([a-zA-Z]:|//[a-zA-Z0-9_.$ -]+/[a-z0-9_.$ -]+)?((?:/|^)(?:[^//:*?"<>|\r\n]+/)+)', subject)
    extname = re.findall(r'\[^.\\/:*?"<>|\r\n]+$', subject)
    filename = re.findall(r'[^\\/:*?"<>|\r\n]+$' , subject)

    if "RP" in subject:
        if match:  
            filepath = match.group(2)  
        else:  
            filepath = ""  
  
        print filepath[3:]
        #print extname
        print filename[0] #get the name without [''] on list

        FusionPath = r"C:\Users\t_zhanj\AppData\Local\Autodesk\webdeploy\dev\974cd21d54914e17c495fe6325b8de15ddb73294" # Your Fusion Path
        ModelPath = os.path.join (FusionPath,filepath[3:],filename[0])
        #print ModelPath

        #modelpath = os.path.join (FusionPath, filename[0])
        if os.path.exists(ModelPath):
            print "exists!"
        else:
            print ModelPath + "not exists!"

        targetFolder = "C:\\Users\\t_zhanj\\Desktop\\Cases\\ModelTest"
        if not os.path.exists (targetFolder):
            os.mkdir (targetFolder)

        copyFiles(ModelPath, targetFolder)

        NewModelPath = os.path.join(targetFolder,filename[0])
        if os.path.exists(NewModelPath):
            print "Copy Success!"
        
def copyFiles(sourceDir, targetDir): 
    if sourceDir.find(".svn") > 0: 
        return 
    
    files = []
    i = 0
    while(1):
        try:
            files = os.listdir(sourceDir)
            break
        except OSError, e:
            print e
            if i >= 10:
                raise Exception('Cannot connect to resource more than 10 times: ' + '"' + sourceDir + '"')
            i = i + 1
            time.sleep(2)
        
    for file in files: 
        sourceFile = os.path.join(sourceDir, file) 
        targetFile = os.path.join(targetDir, file) 
        if os.path.isfile(sourceFile): 
            if not os.path.exists(targetDir):  
                os.makedirs(targetDir)  
            if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):  
                open(targetFile, "wb").write(open(sourceFile, "rb").read()) 
        if os.path.isdir(sourceFile): 
            copyFiles(sourceFile, targetFile)

if __name__=='__main__':
    abcd()
    

    
    

