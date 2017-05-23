#coding=utf-8 
import os
import shutil
import time

def MainMethod():
    a = raw_input("""
If you want re-install OS please backup     --- 1
Put back save files after re-install OS     --- 2
Quit Press                                  --- Press Any Key

Please Choose:""")
    if a == "1":
        Backup()
    elif a == "2":
        PutBack()
    elif a == "aaa":
        return None
        #Custom()
    elif a == "bbb":
        #CustomFiletoFolder()
        return None
    else :
        exit(0)
    
def Backup():
    
    BackupFolderName = time.strftime("%Y%m%d",time.localtime())
    BackupFolderName = BackupFolderName + "_Backup"
    
    source2Kfolder = os.path.join(os.environ["AppData"],"2K Sports") 
    sourceKONAMI = os.path.join(os.environ["USERPROFILE"],"Documents","KONAMI")
    sourceTDU = os.path.join(os.environ["USERPROFILE"],"Documents","Test Drive Unlimited")
    sourceTencentFiles = os.path.join(os.environ["USERPROFILE"],"Documents","Tencent Files")
    
    BackupFolderName = os.path.join("D:\\",BackupFolderName)

    if (os.path.exists(BackupFolderName)):
        shutil.rmtree(BackupFolderName)
        print ("Remove the legacy folder: " + BackupFolderName +" successfully!")
        print ("============================================")
    
    os.makedirs(BackupFolderName)
    print ("Create Backup Folder: " + BackupFolderName + " successfully!")
    print ("============================================")
    CopyMyFiles(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,BackupFolderName)
    ExitOrNot()
        
def CopyMyFiles(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,BackupFolderName):
    if os.path.exists(source2Kfolder):
        Copy2K(source2Kfolder,BackupFolderName)
    else:
        print "The save files of 2K Sports didn't found on this PC and not backup"
        print ("============================================")

    if os.path.exists(sourceKONAMI):
        CopyKONAMI(sourceKONAMI,BackupFolderName)
    else:
        print "The save files of KONAMI didn't found on this PC and not backup"
        print ("============================================")

    if os.path.exists(sourceTDU):
        CopyTDU(sourceTDU,BackupFolderName)
    else:
        print "The save files of TDU didn't found on this PC and not backup"
        print ("============================================")

    if os.path.exists(sourceTencentFiles):
        CopyTencentFiles(sourceTencentFiles,BackupFolderName)
    else:
        print "The save files of TencentFiles didn't found on this PC and not backup"
        print ("============================================")


    
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

def CopyTDU(sourceTDUfolder,BackupFolderName):
    BackupFolderName = os.path.join(BackupFolderName,'Test Drive Unlimited')
    os.makedirs(BackupFolderName)  
    print time.strftime("Start Copy TDU Time :%Y-%m-%d %X",time.localtime())
    copyFiles(sourceTDUfolder,BackupFolderName)
    print ("Backup TDU Success!")
    print time.strftime("End Copy TDU Time :%Y-%m-%d %X",time.localtime())
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


"""       
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
            
"""

def PutBack():
    BackupFolderPath = raw_input ("Please input Backup Folder path:")

    source2Kfolder = os.path.join(os.environ["AppData"],"2K Sports") 
    sourceKONAMI = os.path.join(os.environ["USERPROFILE"],"Documents","KONAMI")
    sourceTDU = os.path.join(os.environ["USERPROFILE"],"Documents","Test Drive Unlimited")
    sourceTencentFiles = os.path.join(os.environ["USERPROFILE"],"Documents","Tencent Files")
    
    if os.path.exists(BackupFolderPath):
        if os.path.exists(os.path.join(BackupFolderPath,"2K Sports")):
            if os.path.exists(source2Kfolder):
                print "2K Sports folder exists, no need to put back"
                print "============================================"
            else:
                print time.strftime("Start Move 2K Time :%Y-%m-%d %X",time.localtime()) 
                shutil.move(os.path.join(BackupFolderPath,"2K Sports"), source2Kfolder)
                print ("Put Back 2K Success!")
                print time.strftime("End Copy 2K Time :%Y-%m-%d %X",time.localtime())
                print "============================================"
        
            if os.path.exists(os.path.join(BackupFolderPath,"KONAMI")):
                if os.path.exists(sourceKONAMI):
                    print "KONAMI folder exists, no need to put back"
                    print "============================================"
                else:
                    print time.strftime("Start Move KONAMI Time :%Y-%m-%d %X",time.localtime()) 
                    shutil.move(os.path.join(BackupFolderPath,"KONAMI"), sourceKONAMI)
                    print ("Put Back KONAMI Success!")
                    print time.strftime("End Copy KONAMI Time :%Y-%m-%d %X",time.localtime())
                    print "============================================"
                
            if os.path.exists(os.path.join(BackupFolderPath,"Test Drive Unlimited")):
                if os.path.exists(sourceTDU):
                    print "TDU folder exists, no need to put back"
                    print "============================================"
                else:
                    print time.strftime("Start Move TDU Time :%Y-%m-%d %X",time.localtime()) 
                    shutil.move(os.path.join(BackupFolderPath,"Test Drive Unlimited"), sourceTDU)
                    print ("Put Back TDU Success!")
                    print time.strftime("End Copy TDU Time :%Y-%m-%d %X",time.localtime())
                    print "============================================"
                
            if os.path.exists(os.path.join(BackupFolderPath,"Tencent Files")):
                if os.path.exists(sourceTencentFiles):
                    print "Tencent Files folder exists, no need to put back"
                    print "============================================"
                else:
                    print time.strftime("Start Copy Tencent Files Time :%Y-%m-%d %X",time.localtime()) 
                    shutil.move(os.path.join(BackupFolderPath,"Tencent Files"), sourceTencentFiles)
                    print ("Put Back Tencent Files Success!")
                    print time.strftime("End Copy Tencent Files Time :%Y-%m-%d %X",time.localtime())
                    print "============================================"
                   
        
    else:
        print BackupFolderPath+ " is not exists!"
        
    if not os.listdir(BackupFolderPath):
        shutil.rmtree(BackupFolderPath)
        if not os.path.exists(BackupFolderPath):
            print "All the save files has put back successfully. Now delete the root folder"
            print "============================================"
            

    ExitOrNot()
    
def ExitOrNot():
    while(True):
        cc = raw_input("Current work has finished! Back to main menu? (Y/N)")
        if cc.lower() == 'y':
            MainMethod()
            break
        elif cc.lower() == 'n':
            exit(0)
        else:
            print "You've typed a illgeal word, please select again!"
            print "============================================"    

        
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
    
        
        
    
        
        
    
