'''
Created on Jan 25, 2017

@author: t_zhanj
'''
import os
import shutil
import time
import platform

def MainMethod():
    ChooseOS()
    
  
def ChooseOS():
    OS = raw_input(
    """
    Which OS do you want choose?
       1 -- Windows
       2 -- Mac
    """)
    OSName =''
    
    if OS == '1':
        OSName = "Win"
        
    elif OS == '2':
        OSName = "Mac"

    ChooseFusionVersion(OSName)



def ChooseFusionVersion(OSName):
    FusionVersionName = ""
    FusionVersionName_Perfix = ""
    FusionVersion = raw_input(
    """
    Which Fusion Version do you want choose?
       1 -- Main
       2 -- RC
       3 -- CU
    """)
    
    if FusionVersion == '1':
        FusionVersionName = 'dev'    
        FusionVersionName_Perfix = 'All'
    elif FusionVersion == '2':   
        FusionVersionName = 'prod'
        FusionVersionName_Perfix = 'proAll'
    elif FusionVersion == '3':
        FusionVersionName = 'cu'
        FusionVersionName_Perfix = 'cuAll'
       
    ChooseOSbuild(OSName,FusionVersionName,FusionVersionName_Perfix)
 

def ChooseOSbuild(OSName,FusionVersionName,FusionVersionName_Perfix):
    OSVersionName = ''
    if OSName == 'Win':
        OSVersion = raw_input(
    """
    Which OS Version do you want choose?
       1 -- Win 7
       2 -- Win 8.1
       3 -- Win 10
    """)
    
    else:
        OSVersion = raw_input(
    """
    Which OS Version do you want choose?
       1 -- Yosemite
       2 -- EI Capitan
       3 -- Sierra
    """)
        
    
    if OSVersion == '1':
        if OSName == 'Win':
            OSVersionName = 'Win7'
        else:
            OSVersionName = 'Yosemite'
    elif OSVersion == '2':     
        if OSName == 'Win':
            OSVersionName = 'Win8.1'
        else:
            OSVersionName = 'El.Capitan'
    elif OSVersion == '3':
        if OSName == 'Win':
            OSVersionName = 'Win10'
        else:
            OSVersionName = 'Sierra'
    
    TypeBuildVersion(OSName,FusionVersionName,FusionVersionName_Perfix,OSVersionName)
    
def TypeBuildVersion(OSName,FusionVersionName,FusionVersionName_Perfix,OSVersionName):
    BuildVersion = raw_input("Please type the build version here: ")
    PrintYourChoosed(OSName,FusionVersionName,FusionVersionName_Perfix,OSVersionName,BuildVersion)
            
def PrintYourChoosed(OSName,FusionVersionName,FusionVersionName_Perfix,OSVersionName,BuildVersion):
    FailedNTPPath = ''
    CurrentOS = platform.system()
    NetPath = r'\\eptserver\Freeway\FusionAutomation\AutomationResult'
    if CurrentOS == 'Windows':
        if OSName == 'Win':
            FailedNTPPath = os.path.join(NetPath,FusionVersionName,OSVersionName,FusionVersionName_Perfix+'_'+BuildVersion+'.ntp-'+OSVersionName+'-'+'FailedCases.ntp')
        
        else: #Mac
            FailedNTPPath = os.path.join(NetPath,FusionVersionName_Perfix+'_'+BuildVersion+'.ntp-'+OSVersionName+'-'+'FailedCases.ntp')
    elif CurrentOS == 'Darwin':
        MountFolder = os.path.join (os.environ['HOME'],'Desktop','Mount')
        if OSName == 'Win':
            NetPath = NetPath[2:]
            NetPath = NetPath.replace('\\','/')
            if not os.path.exists(MountFolder):
                os.makedirs(MountFolder)

            os.system ('mount_smbfs //svc_q_fusion360:AdP6bc4Y@{0} "{1}"' .format(NetPath,MountFolder))
            print 'Mount Success!'
            #FailedNTPPath 
        
        else: #Mac
            #FailedNTPPath = 
            return None

    #FailedNTPPath.replace('\\', '\\\\')
    if os.path.exists(FailedNTPPath):
        CopyNTPFile(OSName,FailedNTPPath)
    else:
        print "File not found!"
    
    
def get_desktop():
    import _winreg
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,\
                          r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',)
    return _winreg.QueryValueEx(key, "Desktop")[0]  
      

def CopyNTPFile(OSName,FailedNTPPath):
    CurrentOS = platform.system()
    DesktopPath = ''
    TodayFolder = time.strftime("%Y%m%d",time.localtime())
    NTPName = FailedNTPPath.split("\\")[-1]
    if CurrentOS == 'Windows':
        DesktopPath = get_desktop()
    #print FailedNTPPath
        
        OutputFilePath = os.path.join(DesktopPath,'John Folder','Failed Cases','2017', TodayFolder , NTPName)
        OutputPath = os.path.join(DesktopPath,'John Folder','Failed Cases','2017', TodayFolder)

    elif CurrentOS == 'Darwin':
        OutputFilePath = os.path.join (os.environ['HOME'],'Desktop','AutomationTriage',TodayFolder,NTPName)
        OutputPath = os.path.join (os.environ['HOME'],'Desktop','AutomationTriage',TodayFolder)


    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)
    
    if os.path.exists(OutputFilePath):
        os.remove(OutputFilePath)
        print "Delete " + NTPName + "  Success!"
    
    shutil.copyfile(FailedNTPPath, OutputFilePath)
    print NTPName + "  has copied to folder " + OutputPath + " Successfully!" 
        
    
        
    


    
if __name__ == '__main__':
    MainMethod()