#coding=utf-8 
import os
import shutil
import time

def MainMethod(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat):
    Choose = raw_input("""
Backup archive files before reinstall OS      --- 1
Put back archive files after reinstall OS     --- 2
Quit Press                                  --- Press Any Key

Please Choose:""")
    if Choose == '1':
        Backup(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat)
    elif Choose == '2':
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
        print "                                "
    os.makedirs(BackupFolder)
    print "Create backup folder: " + BackupFolder + " successfully!"
    print "============================================"
    CopyMyFiles(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat,BackupFolder,IsBackup)
    print "============================================"
    ExitOrNot()
        
def CopyMyFiles(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat,BackupFolder,IsBackup):
    print time.strftime("Start time :%Y-%m-%d %X",time.localtime())
    if IsBackup == '1':
        if os.path.exists(source2Kfolder):
            Copy2K(source2Kfolder,BackupFolder,IsBackup)
        else:
            print "The archive files of 2K Sports didn't found on this PC and won't backup"
        print "                                "
            
        if os.path.exists(sourceKONAMI):
            CopyKONAMI(sourceKONAMI,BackupFolder,IsBackup)
        else:
            print "The archive files of Pro Evolution Soccer didn't found on this PC and won't backup"
        print "                                "

        if os.path.exists(sourceTDU):
            CopyTDU(sourceTDU,BackupFolder,IsBackup)
        else:
            print "The archive files of Test Drive Unlimited didn't found on this PC and won't backup"
        print "                                "

        if os.path.exists(sourceTencentFiles):
            CopyTencentFiles(sourceTencentFiles,BackupFolder,IsBackup)
        else:
            print "The archive files of Tencent Files didn't found on this PC and won't backup"
        print "                                "

        if os.path.exists(sourceBusDriver):
            CopyBusDriver(sourceBusDriver,BackupFolder,IsBackup)
        else:
            print "The archive files of Bus Driver didn't found on this PC and won't backup"
        print "                                "

        if os.path.exists(sourceWeChat):
            CopyWeChatFiles(sourceWeChat,BackupFolder,IsBackup)
        else:
            print "The archive files of WeChat Files didn't found on this PC and won't backup"
        print "                                "
    else:
        i = 0
        if os.path.exists(os.path.join(BackupFolder,'2K Sports')):
            i = i + 1      
            if not os.path.exists(source2Kfolder):
                Copy2K(source2Kfolder,BackupFolder,IsBackup)
            else:
                print "Destination path of 2K Sports " + source2Kfolder + " already exists and won't put back"
            print "                                "
                
        if os.path.exists(os.path.join(BackupFolder,'KONAMI')):
            i = i + 1 
            if not os.path.exists(sourceKONAMI):
                CopyKONAMI(sourceKONAMI,BackupFolder,IsBackup)
            else:
                print "Destination path of Pro Evolution Soccer " + sourceKONAMI + " already exists and won't put back"
            print "                                "
                
        if os.path.exists(os.path.join(BackupFolder,'Test Drive Unlimited')):
            i = i + 1  
            if not os.path.exists(sourceTDU):
                CopyTDU(sourceTDU,BackupFolder,IsBackup)
            else:
                print "Destination path of Test Drive Unlimited " + sourceTDU + " already exists and won't put back"
            print "                                "
                
        if os.path.exists(os.path.join(BackupFolder,'Tencent Files')):
            i = i + 1   
            if not os.path.exists(sourceTencentFiles):
                CopyTencentFiles(sourceTencentFiles,BackupFolder,IsBackup)
            else:
                print "Destination path of Tencent Files " + sourceTencentFiles + " already exists and won't put back"
            print "                                "

        if os.path.exists(os.path.join(BackupFolder,'Bus Driver')):
            i = i + 1    
            if not os.path.exists(sourceBusDriver):
                CopyBusDriver(sourceBusDriver,BackupFolder,IsBackup)
            else:
                print "Destination path of Bus Driver " + sourceBusDriver + " already exists and won't put back"
            print "                                "

        if os.path.exists(os.path.join(BackupFolder,'WeChat Files')):
            i = i + 1   
            if not os.path.exists(sourceWeChat):
                CopyWeChatFiles(sourceWeChat,BackupFolder,IsBackup)
            else:
               print "Destination path of WeChat Files " + sourceWeChat + " already exists and won't put back"
            print "                                "
                
        if i == 0:
            print BackupFolder + " does not contain any releated backup files, this may not a correct backup folder"

        if not os.listdir(BackupFolder):
            shutil.rmtree(BackupFolder)
            if not os.path.exists(BackupFolder):
                print "All archive files has been put back"
                print "Backup folder " + BackupFolder + " has been deleted successfully!"
                print "                                "
    print time.strftime("End time :%Y-%m-%d %X",time.localtime())

def Copy2K(source2Kfolder,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'2K Sports')
        os.makedirs(BackupFolder)  
        copyFiles(source2Kfolder,BackupFolder)
        print "Backup 2K successfully!"
    else:
        shutil.move(os.path.join(BackupFolder,"2K Sports"), source2Kfolder)
        print "Put back 2K successfully!"
      
def CopyKONAMI(sourceKONAMI,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'KONAMI')
        os.makedirs(BackupFolder)
        copyFiles(sourceKONAMI,BackupFolder)
        print "Backup KONAMI successfully!"
    else:
        shutil.move(os.path.join(BackupFolder,"KONAMI"), sourceKONAMI)
        print "Put back KONAMI successfully!"

def CopyTDU(sourceTDU,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'Test Drive Unlimited')
        os.makedirs(BackupFolder)  
        copyFiles(sourceTDU,BackupFolder)
        print "Backup Test Drive Unlimited successfully!"
    else:
        shutil.move(os.path.join(BackupFolder,"Test Drive Unlimited"), sourceTDU)
        print "Put back Test Drive Unlimited successfully!"
    
def CopyTencentFiles(sourceTencentFiles,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'Tencent Files')
        os.makedirs(BackupFolder)
        copyFiles(sourceTencentFiles,BackupFolder)
        print "Backup Tencent Files successfully!"
    else:
        shutil.move(os.path.join(BackupFolder,"Tencent Files"), sourceTencentFiles)
        print "Put back Tencent Files successfully!"

def CopyBusDriver(sourceBusDriver,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'Bus Driver')
        os.makedirs(BackupFolder)
        copyFiles(sourceBusDriver,BackupFolder)
        print "Backup Bus Driver successfully!" 
    else:
        shutil.move(os.path.join(BackupFolder,"Bus Driver"), sourceBusDriver)
        print "Put back Bus Driver successfully!"

def CopyWeChatFiles(sourceWeChat,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'WeChat Files')
        os.makedirs(BackupFolder)
        copyFiles(sourceWeChat,BackupFolder)
        print "Backup WeChat Files successfully!"
    else:
        shutil.move(os.path.join(BackupFolder,"WeChat Files"), sourceWeChat)
        print "Put back WeChat Files successfully!"

def PutBack(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat):
    BackupFolder = raw_input ("Please input back up folder path:")
    print "============================================"
    if BackupFolder.strip():
        if os.path.exists(BackupFolder):
            IsBackup = '2'
            CopyMyFiles(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat,BackupFolder,IsBackup)
        else:
            print BackupFolder + " is not exists!"
    else:
        print "Please do not input the empty infos"
    print "============================================"
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
    source2Kfolder = os.path.join(os.environ['AppData'],'2K Sports') 
    sourceKONAMI = os.path.join(os.environ['USERPROFILE'],'Documents','KONAMI')
    sourceTDU = os.path.join(os.environ['USERPROFILE'],'Documents','Test Drive Unlimited')
    sourceTencentFiles = os.path.join(os.environ['USERPROFILE'],'Documents','Tencent Files')
    sourceBusDriver = os.path.join(os.environ['USERPROFILE'],'Documents','Bus Driver')
    sourceWeChat = os.path.join(os.environ['USERPROFILE'],'Documents','WeChat Files')
    
    MainMethod(source2Kfolder,sourceKONAMI,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat)
