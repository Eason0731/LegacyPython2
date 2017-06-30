#coding=utf-8 
import os
import shutil
import time

def MainMethod(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat):
    a = raw_input("""
If you want re-install OS please backup     --- 1
Put back save files after re-install OS     --- 2
Quit Press                                  --- Press Any Key

Please Choose:""")
    if a == "1":
        Backup(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat)
    elif a == "2":
        PutBack(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat)
    else:
        exit(0)
    
def Backup(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat):
    IsBackup = '1'
    BackupFolder = time.strftime("%Y%m%d",time.localtime())
    BackupFolder = BackupFolder + "_Backup"
    BackupFolder = os.path.join("D:\\",BackupFolder)
    if os.path.exists(BackupFolder):
        shutil.rmtree(BackupFolder)
        print "Delete the legacy backup folder: " + BackupFolder +" successfully!"
        print "============================================"
    os.makedirs(BackupFolder)
    print "Create backup folder: " + BackupFolder + " successfully!"
    print "============================================"
    CopyMyFiles(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat,BackupFolder,IsBackup)
    ExitOrNot()
        
def CopyMyFiles(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat,BackupFolder,IsBackup):
    if IsBackup == '1':
        if os.path.exists(source2Kfolder):
            Copy2K(source2Kfolder,BackupFolder,IsBackup)
        else:
            print "The archive files of 2K Sports didn't found on this PC and won't backup"
            print "============================================"
            
        if os.path.exists(sourceKONAMI):
            CopyKONAMI(sourceKONAMI,BackupFolder,IsBackup)
        else:
            print "The archive files of Pro Evolution Soccer didn't found on this PC and won't backup"
            print "============================================"

        if os.path.exists(sourceTDU):
            CopyTDU(sourceTDU,BackupFolder,IsBackup)
        else:
            print "The archive files of Test Drive Unlimited didn't found on this PC and won't backup"
            print "============================================"

        if os.path.exists(sourceTencentFiles):
            CopyTencentFiles(sourceTencentFiles,BackupFolder,IsBackup)
        else:
            print "The archive files of Tencent Files didn't found on this PC and won't backup"
            print "============================================"

        if os.path.exists(sourceBusDriver):
            CopyBusDriver(sourceBusDriver,BackupFolder,IsBackup)
        else:
            print "The archive files of Bus Driver didn't found on this PC and won't backup"
            print "============================================"

        if os.path.exists(sourceWeChat):
            CopyWeChatFiles(sourceWeChat,BackupFolder,IsBackup)
        else:
            print "The archive files of WeChat Files didn't found on this PC and won't backup"
            print "============================================"
    else:
        i = 0
        if os.path.exists(BackupFolder):
            if os.path.exists(os.path.join(BackupFolder,"2K Sports")):
                i = i + 1      
                if os.path.exists(source2Kfolder):
                    print "The archive files of 2K already exists on origin path and won't put back"
                else:
                    Copy2K(source2Kfolder,BackupFolder,IsBackup)
                print "============================================"
                
            if os.path.exists(os.path.join(BackupFolder,"KONAMI")):
                i = i + 1 
                if os.path.exists(sourceKONAMI):
                    print "The archive files of Pro Evolution Soccer already exists on origin path and won't put back"
                else:
                    CopyKONAMI(sourceKONAMI,BackupFolder,IsBackup)
                print "============================================"
                
            if os.path.exists(os.path.join(BackupFolder,"Test Drive Unlimited")):
                i = i + 1
                if os.path.exists(sourceTDU):
                    print "The archive files of Test Drive Unlimited already exists on origin path and won't put back"
                else:
                    CopyTDU(sourceTDU,BackupFolder,IsBackup)
                print "============================================"
                
            if os.path.exists(os.path.join(BackupFolder,"Tencent Files")):
                i = i + 1
                if os.path.exists(sourceTencentFiles):
                    print "The archive files of Tencent Files already exists on origin path and won't put back"
                else:
                    CopyTencentFiles(sourceTencentFiles,BackupFolder,IsBackup)
                print "============================================"

            if os.path.exists(os.path.join(BackupFolder,"Bus Driver")):
                i = i + 1
                if os.path.exists(sourceBusDriver):
                    print "The archive files of Bus Driver already exists on origin path and won't put back"
                else:
                    CopyBusDriver(sourceBusDriver,BackupFolder,IsBackup)
                print "============================================"

            if os.path.exists(os.path.join(BackupFolder,"WeChat Files")):
                i = i + 1
                if os.path.exists(sourceWeChat):
                    print "The archive files of WeChat Files already exists on origin path and won't put back"
                else:
                    CopyWeChatFiles(sourceWeChat,BackupFolder,IsBackup)
                print "============================================"
                
            if i == 0:
                print BackupFolder + " does not contain any releated backup files, this may not a correct backup folder"

            if not os.listdir(BackupFolder):
                shutil.rmtree(BackupFolder)
                if not os.path.exists(BackupFolder):
                    print "All the save files has been put back"
                    print "Backup folder " + BackupFolder + " has been deleted successfully!"
                    print "============================================"  
        else:
            print BackupFolder + " is not exists!"
        return i
  
def Copy2K(source2Kfolder,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'2K Sports')
        print BackupFolder
        os.makedirs(BackupFolder)  
        print time.strftime("Start time :%Y-%m-%d %X",time.localtime()) 
        copyFiles(source2Kfolder,BackupFolder)
        print "Backup 2K successfully!"
        print time.strftime("End time :%Y-%m-%d %X",time.localtime())
    else:
        print time.strftime("Start time :%Y-%m-%d %X",time.localtime()) 
        shutil.move(os.path.join(BackupFolder,"2K Sports"), source2Kfolder)
        print "Put back 2K successfully!"
        print time.strftime("End time :%Y-%m-%d %X",time.localtime())   
    print "============================================"
      
def CopyKONAMI(sourceKONAMI,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'KONAMI')
        print BackupFolder
        os.makedirs(BackupFolder)
        print time.strftime("Start time :%Y-%m-%d %X",time.localtime())
        copyFiles(sourceKONAMI,BackupFolder)
        print "Backup KONAMI successfully!"
        print time.strftime("End time :%Y-%m-%d %X",time.localtime())
    else:
        print time.strftime("Start time :%Y-%m-%d %X",time.localtime()) 
        shutil.move(os.path.join(BackupFolder,"KONAMI"), sourceKONAMI)
        print "Put back KONAMI successfully!"
        print time.strftime("End time :%Y-%m-%d %X",time.localtime())
    print "============================================"

def CopyTDU(sourceTDU,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'Test Drive Unlimited')
        os.makedirs(BackupFolder)  
        print time.strftime("Start time :%Y-%m-%d %X",time.localtime())
        copyFiles(sourceTDU,BackupFolder)
        print "Backup Test Drive Unlimited successfully!"
        print time.strftime("End time :%Y-%m-%d %X",time.localtime())
    else:
        print time.strftime("Start time :%Y-%m-%d %X",time.localtime()) 
        shutil.move(os.path.join(BackupFolder,"Test Drive Unlimited"), sourceTDU)
        print "Put back Test Drive Unlimited successfully!"
        print time.strftime("End time :%Y-%m-%d %X",time.localtime())
    print "============================================"
    
def CopyTencentFiles(sourceTencentFiles,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'Tencent Files')
        print BackupFolder
        os.makedirs(BackupFolder)
        print time.strftime("Start time :%Y-%m-%d %X",time.localtime())
        copyFiles(sourceTencentFiles,BackupFolder)
        print "Backup Tencent Files successfully!"
        print time.strftime("End time :%Y-%m-%d %X",time.localtime())       
    else:
        print time.strftime("Start time :%Y-%m-%d %X",time.localtime()) 
        shutil.move(os.path.join(BackupFolder,"Tencent Files"), sourceTencentFiles)
        print "Put back Tencent Files successfully!"
        print time.strftime("End time :%Y-%m-%d %X",time.localtime())   
    print "============================================"

def CopyBusDriver(sourceBusDriver,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'Bus Driver')
        print BackupFolder
        os.makedirs(BackupFolder)
        print time.strftime("Start time :%Y-%m-%d %X",time.localtime())
        copyFiles(sourceBusDriver,BackupFolder)
        print "Backup Bus Driver successfully!"
        print time.strftime("End time :%Y-%m-%d %X",time.localtime())       
    else:
        print time.strftime("Start time :%Y-%m-%d %X",time.localtime()) 
        shutil.move(os.path.join(BackupFolder,"Bus Driver"), sourceBusDriver)
        print "Put back Bus Driver successfully!"
        print time.strftime("End time :%Y-%m-%d %X",time.localtime())
    print "============================================"

def CopyWeChatFiles(sourceWeChat,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'WeChat Files')
        print BackupFolder
        os.makedirs(BackupFolder)
        print time.strftime("Start time :%Y-%m-%d %X",time.localtime())
        copyFiles(sourceWeChat,BackupFolder)
        print "Backup WeChat Files successfully!"
        print time.strftime("End time :%Y-%m-%d %X",time.localtime())       
    else:
        print time.strftime("Start time :%Y-%m-%d %X",time.localtime()) 
        shutil.move(os.path.join(BackupFolder,"WeChat Files"), sourceWeChat)
        print "Put back WeChat Files successfully!"
        print time.strftime("End time :%Y-%m-%d %X",time.localtime())
    print "============================================"

def PutBack(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat):
    BackupFolder = raw_input ("Please input back up folder path:")
    IsBackup = '2'
    print "Start to put back archive files!"
    print "============================================"
    CopyMyFiles(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat,BackupFolder,IsBackup)
    ExitOrNot()

def ExitOrNot():
    while(True):
        cc = raw_input("Back to main menu? (Y/N)")
        if cc.lower() == 'y':
            MainMethod(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat)
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
    source2Kfolder = os.path.join(os.environ["AppData"],"2K Sports") 
    sourceKONAMI = os.path.join(os.environ["USERPROFILE"],"Documents","KONAMI")
    sourceTDU = os.path.join(os.environ["USERPROFILE"],"Documents","Test Drive Unlimited")
    sourceTencentFiles = os.path.join(os.environ["USERPROFILE"],"Documents","Tencent Files")
    sourceBusDriver = os.path.join(os.environ["USERPROFILE"],"Documents","Bus Driver")
    sourceWeChat = os.path.join(os.environ["USERPROFILE"],"Documents","WeChat Files")
    
    MainMethod(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat)
