#coding=utf-8 
import os
import shutil
import time

def MainMethod():
    a = raw_input("""
If you want re-install OS please backup Press --- 1
Want to Customed your path please Press       --- 2
Want to Copy File to Folder please Press      --- 3
Quit Press                                    --- Press Any Key

Please Choose:""")
    if a == "1":
        Backup()
    elif a == "2":
        Custom()
    elif a == "3":
        CustomFiletoFolder()
    else :
        exit(0)
    
def Backup():
    
    BackupFolderName = time.strftime("%Y%m%d",time.localtime())
    BackupFolderName = BackupFolderName + " Backup"
    
    source2Kfolder = os.path.join(os.environ["AppData"],"2K Sports")
    
    sourceKONAMI = os.path.join(os.environ["USERPROFILE"],"Documents","KONAMI") 
   
    sourceTencentFiles = os.path.join(os.environ["USERPROFILE"],"Documents","Tencent Files")

    sourceTencent = r'C:\Users\Public\Documents\Tencent'

    
    BackupFolderName = os.path.join("D:\\",BackupFolderName)
    if (os.path.exists(BackupFolderName)):
        
        Copy2K(source2Kfolder,BackupFolderName)
        CopyKONAMI(sourceKONAMI,BackupFolderName)
        CopyTencentFiles(sourceTencentFiles,BackupFolderName)
        CopyTencent(sourceTencent,BackupFolderName)
        
    else:
        os.makedirs(BackupFolderName)
        print ("Create Folder :  " + BackupFolderName + " Success!")
        Backup()
        
def Copy2K(source2Kfolder,BackupFolderName):
    BackupFolderName = os.path.join(BackupFolderName,'2K Sports')
    os.makedirs(BackupFolderName)  
    print time.strftime("Start Copy 2K Time :%Y-%m-%d %X",time.localtime())
    copyFiles(source2Kfolder,BackupFolderName)
    print ("Backup 2K Success!")
    print time.strftime("End Copy 2K Time :%Y-%m-%d %X",time.localtime())
    print ("============================================")
    
    
def CopyKONAMI(sourceKONAMI,BackupFolderName):
    BackupFolderName = os.path.join(BackupFolderName,'KONAMI')
    print BackupFolderName
    os.makedirs(BackupFolderName)
    print time.strftime("Start Copy KONAMI Time :%Y-%m-%d %X",time.localtime())
    copyFiles(sourceKONAMI,BackupFolderName)
    print ("Backup KONAMI Success!")
    print time.strftime("End Copy KONAMI Time :%Y-%m-%d %X",time.localtime())
    print ("============================================")

def CopyTencentFiles(sourceTencentFiles,BackupFolderName):
    BackupFolderName = os.path.join(BackupFolderName,'Tencent Files')
    print BackupFolderName
    os.makedirs(BackupFolderName)
    print time.strftime("Start Copy Tencent Files Time :%Y-%m-%d %X",time.localtime())
    copyFiles(sourceTencentFiles,BackupFolderName)
    print ("Backup Tencent Success!")
    print time.strftime("End Copy Tencent Files Time :%Y-%m-%d %X",time.localtime())
    print ("============================================")

def CopyTencent(sourceTencent,BackupFolderName):
    BackupFolderName = os.path.join(BackupFolderName,'Tencent')
    print BackupFolderName
    os.makedirs(BackupFolderName)
    print time.strftime("Start CopyTencent Time :%Y-%m-%d %X",time.localtime())
    copyFiles(sourceTencent,BackupFolderName)
    print ("Backup Tencent Success!")
    print time.strftime("End CopyTencent Time :%Y-%m-%d %X",time.localtime())
    print ("============================================")
        
def CopyCustomed(sourceCustomed,TargetCustomed):
    if (os.path.exists(sourceCustomed)):
        os.makedirs(TargetCustomed)
    else :
        print ("{0} is NOT Exist!" .format(sourceCustomed))

    if (os.path.isdir(TargetCustomed)):
        print ("TargetFolder is : {0} " .format(TargetCustomed))
        print time.strftime("Start Copy Time :%Y-%m-%d %X",time.localtime())
        copyFiles(sourceCustomed,TargetCustomed)
        print ("Copy Success!")
        print time.strftime("End Copy Time :%Y-%m-%d %X",time.localtime())
        print ("============================================")
    else :
        print ("{0} is NOT Exist!" .format(TargetCustomed))

    Continue()

def Continue():
    while(1):
        cc = raw_input ("continue or back? (y/n)")
        if cc.lower() == "y":
            Custom()
        elif cc.lower() == "n":
            MainMethod()
        else:
            print ("you have typed wrong word")
            continue
        
        
def Custom():
    sourceCustomed = raw_input ("please input sourceFolder: ")
    TargetCustomed = raw_input ("please input TargetFolder: ")
    CopyCustomed(sourceCustomed,TargetCustomed)

def CustomFiletoFolder():
    sourceFile = raw_input ("Please input File path:")
    TargetFolder = raw_input ("Please input Target Folder:")
    pathname,filename = os.path.split (sourceFile)

    print time.strftime("Start Copy Time :%Y-%m-%d %X",time.localtime())
    if (os.path.exists(sourceFile)):
        if (not os.path.exists(TargetFolder)):
            os.makedirs(TargetFolder)      
        shutil.copy (sourceFile,TargetFolder) #Copy File to Folder method
        print ("Copy File Success!")
        print time.strftime("End Copy Time :%Y-%m-%d %X",time.localtime())
        print ("============================================")
    else:
        print ("You File {0} is NOT Exist!" .format(sourceFile))
        
    Continue()
            
        

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


if __name__ == "__main__":
    MainMethod()
    
        
        
    
        
        
    
