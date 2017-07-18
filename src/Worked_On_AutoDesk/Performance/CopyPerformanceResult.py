'''
Created on Dec 6, 2016

@author: t_zhanj
'''
import os
import shutil
import time
import DeleteFailedXmls

def CopyResult(PerfResultDir,OutputFolder):
    for root,dirs,filenames in os.walk(PerfResultDir):
        for myFile in filenames:
            if 'xml' in myFile:
                ActualResultDir = root.split('\\')[-1]
                copyFiles(root, os.path.join(OutputFolder,ActualResultDir))

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

if __name__ == '__main__':
    PerfResultDir = raw_input ("Please input the Performance Result folder:")
    if os.path.exists(PerfResultDir):
        OutputFolder = PerfResultDir
        print "================================="
        print "Deleting Failed xml files......"
        DeleteFailedXmls.DeleteFailedXmlFiles(PerfResultDir)
        print "================================="
        print "Coping files......"
        CopyResult(PerfResultDir,OutputFolder)
        print "Deleting Modeling and Visual......"
        shutil.rmtree(os.path.join(PerfResultDir,'Modeling')) #os.rmdir can delete folders
        shutil.rmtree(os.path.join(PerfResultDir,'Visual'))
        print "================================="
        print "All work done!"

    else:
        print "The Performance result Folder is not exist!"
        
        
    
      
    
