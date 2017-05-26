#coding=utf-8
import os
import re
import sys
import getopt
import urllib2
import platform
import time

import socket
import struct
import subprocess

import string
import codecs, stat

import Settings
import MyLog
import Trigger

Config = None

LOG = MyLog.LOG('Install.py', os.path.join(os.getcwd(), 'runinfo.log'))

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

def copyDir(sourceDir, targetDir): 
    if os.name == 'posix':
        print 'cp -f -R -p \"{0}\" \"{1}\"'.format(sourceDir, targetDir)
        os.system('cp -f -R -p \"{0}\" \"{1}\"'.format(sourceDir, targetDir))

    if os.name == 'nt':
        print "ROBOCOPY /e "+sourceDir+" "+targetDir
        os.system('ROBOCOPY /e '+sourceDir+' '+targetDir)  


def GetStreamerUrl(buildName, OS):
    buildtype = Config.GetBuildTypeByNameandOS(buildName, OS)
    if buildtype == None:
        sys.exit(1)
        
    return buildtype.DownloaderURL

def GetExeName(buildName, OS):
    buildtype = Config.GetBuildTypeByNameandOS(buildName, OS)
    if buildtype == None:
        sys.exit(1)
        
    return buildtype.EXEName

def GetRelatedProcesses(buildName, OS):
    buildtype = Config.GetBuildTypeByNameandOS(buildName, OS)
    if buildtype == None:
        sys.exit(1)
        
    return buildtype.RelatedProcesses

def DownloadStreamer(sourceLink, workSpace):
    streamer = None
    if os.name == 'nt':     
        streamer = os.path.join(workSpace, "Streamer.exe")
    elif os.name == 'posix':
        streamer = os.path.join(workSpace, "Streamer.dmg")
    else:
        return
    
    if streamer != None and os.path.exists(streamer):
        os.remove(streamer)
    
    i = 0
    while(i<20):
        # use urllib2 replace urllib due to system proxy cannot be used in urllib by default
        #urllib.urlretrieve(sourceLink, streamer)
        f = urllib2.urlopen(sourceLink) 
        downloader = open(streamer, "wb")
        downloader.write(f.read())
        downloader.close()
        filesize = os.path.getsize(streamer)
        if filesize > 1*1024*1024L:
            return streamer

def CheckLabel(configFile, label, product, OS):
    Trigger.configFilePath = configFile
    buildlabel = Trigger.GetVersionFromJson(product, OS)

    return buildlabel == label

def SetEnvironmentVariables():
    os.environ['NEUTRON_CHROME_DEVTOOLS']="YES"# Set environment variables

    os.environ['NEUTRON_BUILD']="Debug"
    os.environ['NEUTRON_START_CLOUD']="NO"
    os.environ['NEUTRON_LIVE_UPDATE']="DISABLE"
    os.environ['BUILD_MACHINE']="YES"
    os.environ['SKIP_ENTITLEMENT']="YES"

def KillRelatedProcess(processes):
    for process in processes:
        if os.name == 'nt':
            os.system('taskkill /f /im \"' + process + '*\"')
            os.system('tskill \"' + process + '*\"')
        elif os.name == 'posix':
            os.system('killall -9 \"' + process + '\"')

def RemoveWebdeployDir():
    dirList = ['webdeploy', 'Common/Material Library', 'Common/Exchange Archives', 'Autodesk Fusion 360', 'Web Services']

    if os.name == 'nt':
        rootPath = os.path.join(os.environ['localappdata'], 'Autodesk')
        os.system('tskill explorer')
        os.system('taskkill /im explorer')
        for dir in dirList:
           os.system('RD /s /q "' + os.path.join(rootPath, dir) + '"')
        os.system('explorer')
            
    elif os.name == 'posix':
        rootPath = os.path.join(os.environ['HOME'], 'Library/Application Support/Autodesk')
        for dir in dirList:
            os.system('rm -r -f \"' + os.path.join(rootPath, dir) + '\"')

def MountandInstall(dmgPath, destiPath):
    os.system('mkdir -p ' + destiPath)
    # Mount this point first
    os.system('hdiutil  mount -mountpoint ' + destiPath + ' ' +  dmgPath)
    
    #os.system('open -W ./' + destiPath + '/Double\ Click\ to\ Install.app')
    os.system('open -W ./' + destiPath + '/Right-click\ \>\ Open\ to\ Install.app')
    
    # Unmount the point
    os.system('hdiutil unmount ' + destiPath)

def SubSTWebdeploy(executeFile):
    if os.name == 'posix':
        return
    
    os.system('subst R: /D')
    foldername = 'Autodesk'
    index = executeFile.index(foldername)
    folder = executeFile[:index + len(foldername)]
    os.system('subst R: ' + folder)
    return executeFile.replace(folder, 'R:')


def MountSMBS(netpath, mountpoint):
    os.system('mkdir -p {0}'.format(mountpoint))
    
    netpath = netpath[2:]
    netpath = netpath.replace('\\', '/')
    os.system('mount_smbfs //svc_q_fusion360:AdP6bc4Y@{0} {1}'.format(netpath, mountpoint))

def UmountSMBS(mountpoint):
    os.system('umount ' + mountpoint)

def SearchFilebyName(filename, rootDir):
    if os.path.islink(rootDir) or rootDir[-4:] == 'meta' or rootDir[-6:] == 'shared':
        return None
    candidate = os.path.join(rootDir, filename)
    if os.path.exists(candidate):
        return os.path.abspath(candidate)
        
    list_dirs = os.walk(rootDir) 
    for root, dirs, files in list_dirs: 
        for d in dirs:
            print 'result Mark' 
            if len(d) >= 39:
                result = SearchFilebyName(filename, os.path.join(root, d))
                print 'result =' 
                print result
                if result != None:
                    return result

def GetVersionFromPropertyFile(filePath):
    if not os.path.exists(filePath):
        open(filePath, 'w').close()
        return
    
    labelFile = open(filePath, "r")
    labelString = labelFile.readline()
    prefixString = "BUILDLABEL="
    index = labelString.find(prefixString)
    labelFile.close()
    
    if index != -1:
        return labelString[len(prefixString):]

def SetVersionToPrepertyFile(filePath, buildlabel):
    LOG.LogInfo('Record build {0} into file: [{1}]'.format(buildlabel, filePath))
    writeFile = open(filePath, 'w')
    prefixString = "BUILDLABEL="
    writeFile.write(prefixString + buildlabel)
    writeFile.close()     

def ReplaceCfgXML(source, target):
    Fusion360XML = os.path.join(target, "Fusion360.xml")
    if os.path.exists(Fusion360XML):
        os.remove(Fusion360XML)
    if os.name == 'nt':
        copyFiles(source, target)
    elif os.name == 'posix':
        copyDir(source+'/', target) 

import ctypes
class OSVERSIONINFOEXW(ctypes.Structure):
    _fields_ = [('dwOSVersionInfoSize', ctypes.c_ulong),
                ('dwMajorVersion', ctypes.c_ulong),
                ('dwMinorVersion', ctypes.c_ulong),
                ('dwBuildNumber', ctypes.c_ulong),
                ('dwPlatformId', ctypes.c_ulong),
                ('szCSDVersion', ctypes.c_wchar*128),
                ('wServicePackMajor', ctypes.c_ushort),
                ('wServicePackMinor', ctypes.c_ushort),
                ('wSuiteMask', ctypes.c_ushort),
                ('wProductType', ctypes.c_byte),
                ('wReserved', ctypes.c_byte)]

def get_os_version():
    """
    Get's the OS major and minor versions.  Returns a tuple of
    (OS_MAJOR, OS_MINOR).
    """
    os_version = OSVERSIONINFOEXW()
    os_version.dwOSVersionInfoSize = ctypes.sizeof(os_version)
    retcode = ctypes.windll.Ntdll.RtlGetVersion(ctypes.byref(os_version))
    if retcode != 0:
        raise Exception("Failed to get OS version")

    return os_version.dwMajorVersion, os_version.dwMinorVersion


def ModifyRuntimeConfig(runtimeCfg, label, productName, productBranch):
    if not os.path.exists(runtimeCfg):
        LOG.LogError('Cannot find the ntest runtime configration file: ' + runtimeCfg)
    else:
        LOG.LogInfo('Modify ntest runtime configration file: ' + runtimeCfg)
        fsrc = open(runtimeCfg, "r")
        lines = fsrc.readlines()
        fsrc.close()

        os.remove(runtimeCfg)
        fdst = open(runtimeCfg, "w")
        for line in lines:
            if  -1 != line.find('<product_info name="unknow" branch="unknow" buildversion="unknow">'):
                fdst.write('<product_info name="{0}" branch="{1}" buildversion="{2}">'.format(productName, productBranch, label))
            elif -1 != line.find('<os type="unknow" version="unknow" arch="unknow" language="unknow" build="unknow" sp="unknow"></os>'):
                if os.name == 'posix':
                    osname = ''
                    if -1 != platform.mac_ver()[0].find('10.8'):
                        osname = "MountainLion"
                    elif -1 != platform.mac_ver()[0].find('10.9'):
                        osname = "Mavericks"
                    elif -1 != platform.mac_ver()[0].find('10.10'):
                        osname = "Yosemite"
                    fdst.write('<os type="{0}" version="{1}" arch="{2}" language="{3}" build="unknow" sp="unknow"></os>'.format("Darwin", osname, "64bit", "English"))
                elif os.name == 'nt':
                    osname = ''
                    ver = get_os_version()
                    if ver[0] == 6L:
                        if ver[1] == 1L:
                            osname = "7"
                        elif ver[1] == 2L:
                            osname = "8"
                        elif ver[1] == 3L:
                            osname = "8.1"
                        elif ver[1] == 4L:
                            osname = "10"
                        
                    fdst.write('<os type="{0}" version="{1}" arch="{2}" language="{3}" build="unknow" sp="unknow"></os>'.format("Windows", osname, "64bit", "English"))
            else:
                fdst.write(line)
        fdst.close()

def runApplication(text, product):
    exeFile = ''
    exeFileName = ''
    webdeployPath = ''
    if os.name == 'nt':
        OS = 'Win'
        exeFileName = GetExeName(product, OS) + '.exe'
        webdeployPath = os.path.join(os.environ['localappdata'], 'Autodesk', 'webdeploy')
        exeFile = SearchFilebyName(exeFileName, webdeployPath)
    elif os.name == 'posix':
        OS = 'Mac'
        exeFileName = GetExeName(product, OS) + '.app'
        exeFile = '{0}/Applications/{1}'.format(os.environ['HOME'], exeFileName)

    cmd = ''
    if os.name == "nt":
        cmd = exeFile + " -execute " + text
    elif os.name == "posix":
        cmd = "open -W \"" + exeFile + "\" --args nothing -execute " + text 
    print(cmd)
    child = subprocess.Popen(cmd,shell = True, close_fds = None,stdout = None,stderr = None, preexec_fn = None)
    #child = subprocess.Popen(cmd)
    return child

def send_request(sock,req):
    req_len= struct.pack("i",len(req));
    encoded_req = bytearray();
    encoded_req.extend(req_len);
    encoded_req.extend(req.encode());
    sock.send(encoded_req)
    return encoded_req;


def recv_resposne(sock):
    full_response = bytearray()

    response = sock.recv(4096);
    res_total_len = struct.unpack("i",response[0:4])[0]

    bytes_remaining = res_total_len - len(response)+4

    full_response.extend(response[4:]);

    while bytes_remaining > 0:
        if bytes_remaining < 4096:
            buffer = sock.recv(bytes_remaining);
            bytes_remaining = 0;
        else:
            buffer = sock.recv(4096);
            bytes_remaining = bytes_remaining-4096
        full_response.extend(buffer);

    print 'in recieve...'
    print(full_response.decode('utf-8'));
    return full_response.decode('utf-8')
def SendTxtCmdToFusion(txtCmd):    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    feedback = ''
    try:
        sock.connect((socket.gethostname(),5800))
        print("connected to neutron server")
        # Any text command can be sent to Fusion/Neutron to run
        send_request(sock,txtCmd)
        # Error message can be obtained in following function
        feedback = recv_resposne(sock)

    except Exception as err:
        print(err);
    
    try:
        sock.close()
        
    except Exception as err:
        print(err);

    return feedback



def Usage():
    print 'Install.py usage:'
    print '-h, --help: print help message.'
    print '-p, --product: The product will be installed. '
    print '-v, --version: The version of build will be installed. '
    print '-r, --remote: The directory stores some shared stuff. '

if __name__=='__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:v:r:', ['help', 'product=', 'version=', 'remote='])
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)
    
    workSpace = os.path.split(os.path.realpath(__file__))[0]
    sharePoint = os.path.join(os.path.dirname(workSpace), 'sharepoint')
    product = ''
    label = ''
    remoteDir = ''
    for o, a in opts:
        if o in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif o in ('-p', '--product',):
            product = a
        elif o in ('-v', '--version',):
            label = a
        elif o in ('-r', '--remote',):
            remoteDir = a
        else:
            LOG.LogError('unhandled option')
            sys.exit(2)
         
    if product == '' or label == '' or remoteDir == '':
        LOG.LogError('Please input required arguments!\n')
        Usage()
        sys.exit(1)
    # Wait 15mins to install 
    #time.sleep(60*15)

    if os.name == 'posix':
        LOG.LogInfo('Mount the remote direcotry [{0}]'.format(remoteDir))
        MountSMBS(remoteDir, sharePoint)
        remoteDir = sharePoint
    if not os.path.isdir(remoteDir):
        LOG.LogError('Cannot access remote directory: ' + remoteDir)
        sys.exit(1)
    
    labelFilePath = os.path.join(os.path.dirname(workSpace), 'installedLabel.txt')
    existBuild = GetVersionFromPropertyFile(labelFilePath)
    if existBuild != None and existBuild == label:
        LOG.LogInfo('Build {0} has installed already.'.format(label))
        sys.exit()
    
    configFilePath = os.path.join(workSpace, 'Config.xml')
    Config = Settings.Parameters(configFilePath)
    
    exeFileName = ''
    webdeployPath = ''
    runtimeFileName = "runtimeinfo.xml"
    if os.name == 'nt':
        OS = 'Win'
        exeFileName = GetExeName(product, OS) + '.exe'
        webdeployPath = os.path.join(os.environ['localappdata'], 'Autodesk', 'webdeploy')
    elif os.name == 'posix':
        OS = 'Mac'
        exeFileName = GetExeName(product, OS) + '.app'
        webdeployPath = os.path.join(os.environ['HOME'], 'Library/Application Support/Autodesk/webdeploy')
        
    killProcesses = GetRelatedProcesses(product, OS)
    killProcesses.insert(0, GetExeName(product, OS))
    
    KillRelatedProcess(killProcesses)
    
    LOG.LogInfo('Check if this machine can get expected label to install.')
    for i in range(20):
        if CheckLabel(configFilePath, label, product, OS):
            break
        elif i == 19:
            LOG.LogError('Cannot get build: {0} from this machine.'.format(label))
            sys.exit(1)
        else:
            LOG.LogInfo('Continue check...')
            time.sleep(60*3)

    LOG.LogInfo('Remove legacy builds on the machine.')
    # Set label to null first
    SetVersionToPrepertyFile(labelFilePath, 'null')
    # Remove some legacy files
    RemoveWebdeployDir()
    if os.name == "nt":
        os.system('RD /s /q "C:\ProgramData\Autodesk\FusDoc"')
        
    
    # Start to install
    streamerUrl = GetStreamerUrl(product, OS)
    if streamerUrl != None and streamerUrl != '':
        tmpDir = os.path.join(workSpace, 'Temp')
        if not os.path.exists(tmpDir):
            os.mkdir(tmpDir)
        streamer = DownloadStreamer(streamerUrl, tmpDir)
        if streamer != None and streamer != '':
            LOG.LogInfo('Install build by streamer: [{0}]'.format(streamerUrl))
            if os.name == 'nt':
                os.system(streamer)
            elif os.name == 'posix':
                MountandInstall(streamer, 'test_mountpoint')
            
    KillRelatedProcess(killProcesses)
    
    installPath = ''
    cfgFilePath = ''
    if os.name == 'nt':
        exePath = SearchFilebyName(exeFileName, webdeployPath)
        installPath = os.path.split(exePath)[0]
        installPath = SubSTWebdeploy(installPath)
        # Copy NTest stuff
        LOG.LogInfo('Start to copy NText files to local.')
        copyFiles(r'{0}\builds\{1}\{2}\NTest'.format(remoteDir, label, OS), installPath)
        # As fusion doc samples need keep the file property, so will recopy the fusion doc cases file samples
        copyDir(r'{0}\builds\{1}\{2}\NTest\FusionDoc\Test\DocTests\Dataset'.format(remoteDir, label, OS),os.path.join(installPath,'FusionDoc\Test\DocTests\Dataset'))
        
        LOG.LogInfo('Update the fusion.xml.')
        ReplaceCfgXML(os.path.join(remoteDir, 'Scripts', 'FusionXML'), os.path.join(installPath, r"Applications\Fusion\Fusion360App"))
        
        # Replace the login state cache in Web Services directory
        LOG.LogInfo('Start to replace the login state cache file.')
        copyFiles(r'Cache\{0}'.format(product.lower()), os.path.join(os.path.dirname(webdeployPath), 'Web Services'))
        
        # Replace the python33.dll temporarily on Win 7
        if -1 != platform.win32_ver()[0].find('7'):
            dllpath = os.path.join(installPath, "python33.dll")
            if os.path.exists(dllpath):
               os.remove(dllpath)
            copyFiles(os.path.join(remoteDir, 'Scripts', 'dll'), installPath)
        
        # Copy Regression stuff
        #LOG.LogInfo('Start to copy Regression test model and other stuff.')
        #copyFiles(r'{0}\builds\{1}\Regression'.format(remoteDir, label), os.path.join(installPath, r'Neutron\Test\Sample\Regression'))
        cfgFilePath = os.path.join(installPath, r'Neutron\NTest\UI\NTestUI\Resources\RunTime', runtimeFileName)
        
    elif os.name == 'posix':
        installPath = '{0}/Applications/{1}/Contents/Libraries'.format(os.environ['HOME'], exeFileName)

        LOG.LogInfo('Current directory is: ' + os.getcwd())
        # Copy NTest stuff
        LOG.LogInfo('Start to copy NTest files to local.')
        copyDir('{0}/builds/{1}/{2}/NTest/NTest'.format(sharePoint, label, OS), os.path.join(installPath, 'Applications/NTest'))
        
        #Copy Tests case
        LOG.LogInfo('Start to copy test files on different test directories to local')
        
        if product.lower() == 'dev':
            copyDir('{0}/builds/{1}/{2}/NTest/Neutron'.format(sharePoint, label, OS), os.path.join(installPath, 'Neutron'))

            #If note the below method that 'Fusion', 'Animation', 'FusionDoc', 'NeuCAM','Simulation' cannot be copied to Path
            testDirList = ['Fusion', 'Animation', 'FusionDoc', 'NeuCAM','Simulation']
            for testDir in testDirList:
                testPath = os.path.join(installPath, 'Neutron', testDir)
                if not os.path.exists(testPath):
                    print('mkdir -p /"{0}/"'.format(testPath))
                    os.system('mkdir -p /"{0}/"'.format(testPath))
                copyDir('{0}/builds/{1}/{2}/NTest/{3}'.format(sharePoint, label, OS, testDir), os.path.join(installPath, 'Neutron'))
            
        else: #For RC and CU builds to copy test case
            #copyDir('{0}/builds/{1}/{2}/NTest/Neutron'.format(sharePoint, label, OS), os.path.join(installPath, 'Neutron/Neutron/Test'))
            testDirList = ['Fusion', 'Animation', 'FusionDoc', 'NeuCAM', 'Neutron', 'Simulation']
            for testDir in testDirList:
                testPath = os.path.join(installPath, 'Neutron', testDir)
                if not os.path.exists(testPath):
                    print('mkdir -p /"{0}/"'.format(testPath))
                    os.system('mkdir -p /"{0}/"'.format(testPath))
                copyDir('{0}/builds/{1}/{2}/NTest/{3}'.format(sharePoint, label, OS, testDir), os.path.join(testPath, 'Test'))  
        
        LOG.LogInfo('Update the fusion.xml.')
        # ReplaceCfgXML(os.path.join(sharePoint, 'Scripts', 'FusionXML'), os.path.join(installPath, 'Applications/Fusion/Configuration'))
        ReplaceCfgXML(os.path.join(os.getcwd(), 'FusionXML'), os.path.join(installPath, 'Applications/Fusion/Configuration'))
        
        # Replace the login state cache in Web Services directory
        LOG.LogInfo('Start to replace the login state cache file.')
        copyDir('Cache/{0}'.format(product.lower()), os.path.join(os.path.dirname(webdeployPath), 'Web Services'))
        
        # Copy Regression stuff
        #LOG.LogInfo('Start to copy Regression test model and other stuff.')
        #copyDir('{0}/builds/{1}/Regression'.format(sharePoint, label), os.path.join(installPath, 'Neutron/Test/Sample/Regression'))
        cfgFilePath = os.path.join(installPath, 'Applications/NTest/NTest/UI/NTestUI/Resources/RunTime', runtimeFileName)
        
        LOG.LogInfo('Umount the remote direcotry [{0}]'.format(remoteDir))
        UmountSMBS(sharePoint)

    productName = 'Fusion360'
    productBranch = 'main'
    if product.lower() == 'prod':
        productBranch = 'prod'
    ModifyRuntimeConfig(cfgFilePath, label, productName, productBranch)

    #check if the installed version is the correct one
    SetEnvironmentVariables()
    #fusion = runApplication("IPC.startTCPServer", product)
    #print(fusion.pid)

    #Sleep two mins to wait Fusion launch
    time.sleep(60*2)
    #buildNoStr = SendTxtCmdToFusion('Application.SoftwareVersion')
    #buildNo = buildNoStr.split(',')[0]
    #if buildNo != label:
    #    print('Installed wrong build: {0} instead of {1}'.format(buildNo, label))
    #    sys.exit(2)

    KillRelatedProcess(killProcesses)
    SetVersionToPrepertyFile(labelFilePath, label)

