#coding=utf-8 
import os
import shutil
import time

def MainMethod(source2Kfolder,sourcePES,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat):
    Choose = raw_input("""
=========Welcome to Backup Archive Files===========
1. Backup archive files before reinstall OS
2. Put back archive files after reinstall OS
===================================================
Press AnyKey to Exit

Please Choose:""")
    if Choose == '1':
        Backup(source2Kfolder,sourcePES,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat)
    elif Choose == '2':
        PutBack(source2Kfolder,sourcePES,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat)
    else:
        exit(0)
    
def Backup(source2Kfolder,sourcePES,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat):
    IsBackup = '1'
    BackupFolder = time.strftime("%Y%m%d",time.localtime())
    BackupFolder = BackupFolder + "_Backup"
    BackupFolder = os.path.join("D:\\",BackupFolder)
    if os.path.exists(BackupFolder):
        shutil.rmtree(BackupFolder)
        print "Old backup folder: " + BackupFolder +" has been deleted successfully!"
        print "                                "
    os.makedirs(BackupFolder)
    print "Create backup folder: " + BackupFolder + " successfully!"
    print "==================================================="
    MyFiles(source2Kfolder,sourcePES,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat,BackupFolder,IsBackup)
    print "==================================================="
    ExitOrNot()
        
def MyFiles(source2Kfolder,sourcePES,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat,BackupFolder,IsBackup):
    print time.strftime("Start time :%Y-%m-%d %X",time.localtime())
    Info = "'s archive files on this PC"
    if IsBackup == '1':
        if os.path.exists(source2Kfolder):
            My2K(source2Kfolder,BackupFolder,IsBackup)
        else:
            print "Won't back -- Not found 2K Sports" + Info
        print "                                "
            
        if os.path.exists(sourcePES):
            PES(sourcePES,BackupFolder,IsBackup)
        else:
            print "Won't back -- Not found Pro Evolution Soccer" + Info
        print "                                "

        if os.path.exists(sourceTDU):
            TDU(sourceTDU,BackupFolder,IsBackup)
        else:
            print "Won't back -- Not found Test Drive Unlimited" + Info
        print "                                "

        if os.path.exists(sourceTencentFiles):
            TencentFiles(sourceTencentFiles,BackupFolder,IsBackup)
        else:
            print "Won't back -- Not found Tencent Files" + Info
        print "                                "

        if os.path.exists(sourceBusDriver):
            BusDriver(sourceBusDriver,BackupFolder,IsBackup)
        else:
            print "Won't back -- Not found Bus Driver" + Info
        print "                                "

        if os.path.exists(sourceWeChat):
            WeChatFiles(sourceWeChat,BackupFolder,IsBackup)
        else:
            print "Won't back -- Not found WeChat Files" + Info
        print "                                "
    else:
        i = 0
        if os.path.exists(os.path.join(BackupFolder,'2K Sports')):
            i = i + 1      
            if not os.path.exists(source2Kfolder):
                My2K(source2Kfolder,BackupFolder,IsBackup)
            else:
                print "Won't put back -- Path of 2K Sports " + source2Kfolder + " had existed"
            print "                                "
                
        if os.path.exists(os.path.join(BackupFolder,'KONAMI')):
            i = i + 1 
            if not os.path.exists(sourcePES):
                PES(sourcePES,BackupFolder,IsBackup)
            else:
                print "Won't put back -- Path of Pro Evolution Soccer " + sourcePES + " had existed"
            print "                                "
                
        if os.path.exists(os.path.join(BackupFolder,'Test Drive Unlimited')):
            i = i + 1  
            if not os.path.exists(sourceTDU):
                TDU(sourceTDU,BackupFolder,IsBackup)
            else:
                print "Won't put back -- Path of Test Drive Unlimited " + sourceTDU + " had existed"
            print "                                "
                
        if os.path.exists(os.path.join(BackupFolder,'Tencent Files')):
            i = i + 1   
            if not os.path.exists(sourceTencentFiles):
                TencentFiles(sourceTencentFiles,BackupFolder,IsBackup)
            else:
                print "Won't put back -- Path of Tencent Files " + sourceTencentFiles + " had existed"
            print "                                "

        if os.path.exists(os.path.join(BackupFolder,'Bus Driver')):
            i = i + 1    
            if not os.path.exists(sourceBusDriver):
                BusDriver(sourceBusDriver,BackupFolder,IsBackup)
            else:
                print "Won't put back -- Path of Bus Driver " + sourceBusDriver + " had existed"
            print "                                "

        if os.path.exists(os.path.join(BackupFolder,'WeChat Files')):
            i = i + 1   
            if not os.path.exists(sourceWeChat):
                WeChatFiles(sourceWeChat,BackupFolder,IsBackup)
            else:
               print "Won't put back -- Path of WeChat Files " + sourceWeChat + " had existed"
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

def My2K(source2Kfolder,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'2K Sports')
        os.makedirs(BackupFolder)  
        copyFiles(source2Kfolder,BackupFolder)
        print "Backup 2K successfully!"
    else:
        shutil.move(os.path.join(BackupFolder,"2K Sports"), source2Kfolder)
        print "Put back 2K successfully!"
      
def PES(sourcePES,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'KONAMI')
        os.makedirs(BackupFolder)
        copyFiles(sourcePES,BackupFolder)
        print "Backup Pro Evolution Soccer successfully!"
    else:
        shutil.move(os.path.join(BackupFolder,"KONAMI"), sourcePES)
        print "Put back Pro Evolution Soccer successfully!"

def TDU(sourceTDU,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'Test Drive Unlimited')
        os.makedirs(BackupFolder)  
        copyFiles(sourceTDU,BackupFolder)
        print "Backup Test Drive Unlimited successfully!"
    else:
        shutil.move(os.path.join(BackupFolder,"Test Drive Unlimited"), sourceTDU)
        print "Put back Test Drive Unlimited successfully!"
    
def TencentFiles(sourceTencentFiles,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'Tencent Files')
        os.makedirs(BackupFolder)
        copyFiles(sourceTencentFiles,BackupFolder)
        print "Backup Tencent Files successfully!"
    else:
        shutil.move(os.path.join(BackupFolder,"Tencent Files"), sourceTencentFiles)
        print "Put back Tencent Files successfully!"

def BusDriver(sourceBusDriver,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'Bus Driver')
        os.makedirs(BackupFolder)
        copyFiles(sourceBusDriver,BackupFolder)
        print "Backup Bus Driver successfully!" 
    else:
        shutil.move(os.path.join(BackupFolder,"Bus Driver"), sourceBusDriver)
        print "Put back Bus Driver successfully!"

def WeChatFiles(sourceWeChat,BackupFolder,IsBackup):
    if IsBackup == '1':
        BackupFolder = os.path.join(BackupFolder,'WeChat Files')
        os.makedirs(BackupFolder)
        copyFiles(sourceWeChat,BackupFolder)
        print "Backup WeChat Files successfully!"
    else:
        shutil.move(os.path.join(BackupFolder,"WeChat Files"), sourceWeChat)
        print "Put back WeChat Files successfully!"

def PutBack(source2Kfolder,sourcePES,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat):
    BackupFolder = raw_input ("Please input backup folder path:")
    print "==================================================="
    if BackupFolder.strip():
        if os.path.exists(BackupFolder):
            IsBackup = '2'
            MyFiles(source2Kfolder,sourcePES,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat,BackupFolder,IsBackup)
        else:
            print BackupFolder + " is not exists!"
    else:
        print "Please do not input the empty infos"
    print "==================================================="
    ExitOrNot()

def ExitOrNot():
    while(True):
        cc = raw_input("Back to main menu? (Y/N)")
        if cc.lower() == 'y':
            MainMethod(source2Kfolder,sourcePES,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat)
            break
        elif cc.lower() == 'n':
            exit(0)
        else:
            print "You've typed a illgeal word, please select again!"
            print "==================================================="    
     
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
    sourcePES = os.path.join(os.environ['USERPROFILE'],'Documents','KONAMI')
    sourceTDU = os.path.join(os.environ['USERPROFILE'],'Documents','Test Drive Unlimited')
    sourceTencentFiles = os.path.join(os.environ['USERPROFILE'],'Documents','Tencent Files')
    sourceBusDriver = os.path.join(os.environ['USERPROFILE'],'Documents','Bus Driver')
    sourceWeChat = os.path.join(os.environ['USERPROFILE'],'Documents','WeChat Files')
    
    MainMethod(source2Kfolder,sourcePES,sourceTDU,sourceTencentFiles,sourceBusDriver,sourceWeChat)
