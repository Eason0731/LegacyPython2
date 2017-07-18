import os #Load the related python modules
import sys
import getopt
import shutil
import codecs
import string
import xmlconvert
import platform
import PerformanceRun

if os.name == 'nt':
    import _winreg

import re
import Settings

Config = None

def copyFiles(sourceDir,  targetDir): 
    if sourceDir.find(".svn") > 0: 
        return 
    for file in os.listdir(sourceDir): 
        sourceFile = os.path.join(sourceDir, file) 
        targetFile = os.path.join(targetDir, file) 
        if os.path.isfile(sourceFile): 
            if not os.path.exists(targetDir):  
                os.makedirs(targetDir)  
            if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):  
                open(targetFile, "wb").write(open(sourceFile, "rb").read()) 
        if os.path.isdir(sourceFile): 
            copyFiles(sourceFile, targetFile)
            
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
    
def SearchFilebyName(filename, rootDir):
    if os.path.islink(rootDir) or rootDir[-4:] == 'meta' or rootDir[-6:] == 'shared':
        return None
    candidate = os.path.join(rootDir, filename)
    if os.path.exists(candidate):
        if os.path.islink(candidate):
            return None
        return os.path.abspath(candidate)
        
    list_dirs = os.walk(rootDir) 
    for root, dirs, files in list_dirs: 
        for d in dirs:
            result = SearchFilebyName(filename, os.path.join(root, d))
            if result != None:
                return result

def ParseResult(filepath):
    file = open(filepath)
    
    pattern = re.compile(".*>(?P<result>\d+ run, \d+ passed, \d+ failed).*")
    casePattern = re.compile('.*;">(?P<result>\d+)<\/span>.*')
    
    for line in file:
        match = pattern.match(line)
        if match:
            print("Run Result=" + match.group('result'))
        
        matchCase = casePattern.match(line)
        if matchCase:
            print("Total Cases=" + matchCase.group('result'))
    
    file.close()

def SetEnvironmentVariables():
    os.environ['NEUTRON_BUILD']="Debug"# Set environment variables
    os.environ['NEUTRON_START_CLOUD']="NO"
    os.environ['NEUTRON_LIVE_UPDATE']="DISABLE"
    os.environ['BUILD_MACHINE']="YES"
    os.environ['SKIP_ENTITLEMENT']="YES"

def SubSTWebdeploy(executeFile):
    if os.name == 'posix':
        return
    
    os.system('subst R: /D')
    foldername = 'Autodesk'
    index = executeFile.index(foldername)
    folder = executeFile[:index + len(foldername)]
    os.system('subst R: ' + folder)
    return executeFile.replace(folder, 'R:')

def GetPreparedNTPFile(workSpace, executeFile, ntpProject, label):
    finalFilePath = ''
    
    ntpFile = Config.GetNTPFilebyName(ntpProject)
    
    if ntpFile == None or ntpFile == '':
        print 'Cannot find matched NTest project file for project [{0}]'.format(ntpProject)
        return
    
    ntpFilePath = os.path.join(workSpace, 'NTPFiles', ntpFile)
    if not os.path.exists(ntpFilePath):
        print 'Cannot find NTest project file [{0}]'.format(ntpFilePath)
        return
    
    tmpDir = os.path.join(workSpace, 'Temp')
    if not os.path.exists(tmpDir):
        os.mkdir(tmpDir)
    
    fileName = os.path.splitext(os.path.basename(ntpFilePath))[0]
    finalFilePath = os.path.join(tmpDir, '{0}_{1}.ntp'.format(fileName, label))
    
    installPath = os.path.split(executeFile)[0]
    if os.name == 'posix':
        installPath = executeFile + '/Contents/Frameworks/Neutron.framework'
    
    file = codecs.open(ntpFilePath, 'r', 'utf-16')
    allString = file.read()
    allString = string.replace(allString,"__StreamerFusionPath__", installPath)
    allString = string.replace(allString,"__ExeFile__", executeFile)
    file.close()

    ntpfile = codecs.open(finalFilePath, 'w', 'utf-16')
    ntpfile.write(allString)
    ntpfile.close()
    
    return finalFilePath

def MountSMBS(netpath, mountpoint):
    os.system('mkdir -p {0}'.format(mountpoint))
    
    netpath = netpath[2:]
    netpath = netpath.replace('\\', '/')
    os.system('mount_smbfs //svc_q_fusion360:AdP6bc4Y@{0} {1}'.format(netpath, mountpoint))
    return mountpoint

def UmountSMBS(mountpoint):
    os.system('umount ' + mountpoint)
   
def UploadResult(sourceFile, targetDir):
    if not os.path.exists(targetDir):  
        os.makedirs(targetDir)
        
    targetFile = os.path.join(targetDir, os.path.split(sourceFile)[1])
    shutil.copyfile(sourceFile, targetFile)

def Convert2JnuitResult(xmlPath, targetDir):
    conPath = os.path.join(targetDir, "NFusionTest.xml")
    
    (alldata, caseList) = xmlconvert.load_xml_result(xmlPath)
    unitresult = xmlconvert.convert_unit_result(alldata)
    unitresult.write(conPath)
 
def Run(workSpace, executeFile, ntpProject, label, jobname, processes):
    SetEnvironmentVariables()
    
    #Remove the JUnit result first
    if os.path.exists(os.path.join(workSpace, 'JUnitResult', 'NFusionTest.xml')):
        os.remove(os.path.join(workSpace, 'JUnitResult', 'NFusionTest.xml'))

    appFile = None
    ntpFile = None
    if os.name == 'nt':
        executeFile = SubSTWebdeploy(executeFile)
        ntpFile = GetPreparedNTPFile(workSpace, executeFile, ntpProject, label)
    if os.name == 'posix':
        webdeployPath = os.path.join(os.environ['HOME'], 'Library', 'Application Support', 'Autodesk', 'webdeploy')
        appFile = SearchFilebyName(os.path.basename(executeFile), webdeployPath)
        ntpFile = GetPreparedNTPFile(workSpace, appFile, ntpProject, label)
    
    if ntpFile == None or ntpFile == '':
        return False
    
    outputDir = os.path.join(workSpace, 'Results', label)
    if os.path.exists(outputDir):
        shutil.rmtree(outputDir)
    os.makedirs(outputDir)
    
    OS = ''
    if os.name == 'nt':
        if -1 != platform.win32_ver()[0].find('7'):
            OS = "Win7"
        elif -1 != platform.win32_ver()[0].find('8'):
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion')
            version, type = _winreg.QueryValueEx(key, "CurrentVersion")
            if version == '6.2':
                OS = "Win8"
            elif version == '6.3':
                OS = "Win8.1"
                productname, type = _winreg.QueryValueEx(key, "ProductName")
                if -1 != productname.lower().find('windows 10'):
                    OS = "Win10"
    elif os.name == 'posix':
        if -1 != platform.mac_ver()[0].find('10.8'):
            OS = "MountainLion"
        elif -1 != platform.mac_ver()[0].find('10.9'):
            OS = "Mavericks"
        elif -1 != platform.mac_ver()[0].find('10.10'):
            OS = "Yosemite"
        elif -1 != platform.mac_ver()[0].find('10.11'):
            OS = "El.Capitan"
        elif -1 != platform.mac_ver()[0].find('10.12'):
            OS = "Sierra"
    
    outputName = '{0}_{1}_{2}'.format(label, OS, ntpProject)
    if jobname != '':
        outputName = outputName + '_' + jobname
    outputFile = os.path.join(outputDir, outputName)
    outputFilehtm = os.path.join(outputDir, '{0}.htm'.format(outputName))
    outputFilexml = os.path.join(outputDir, '{0}.xml'.format(outputName))
    
    IsUploadToQAPortal = True
    IsUPloadPerfDir = False
    if -1 != ntpProject.lower().find('perf'):
        IsUploadToQAPortal = False
        IsUPloadPerfDir = True
    elif -1 != ntpProject.lower().find('largeassembly'):
        IsUploadToQAPortal = False
        IsUPloadPerfDir = True    

    os.system(r'copy /Y "C:\CI\workspace\Perf_Stag_Fusion_Win7\Cache\NGlobalOptions.xml" "C:\Users\zhujin\AppData\Roaming\Autodesk\Neutron Platform\Options\NGlobalOptions.xml"')
    
    # Start to run performance test cases
    if os.name == 'nt':
        PerformanceRun.RunMgr(executeFile, ntpFile, processes,label,ntpProject )
    elif os.name == 'posix':
        PerformanceRun.RunMgr(appFile, ntpFile, processes,label,ntpProject)
    
    uploadTarget = Config.GetUploadDirectory()
    
    print 'Start to output result url'
    print os.path.join(uploadTarget, 'Performance', os.path.splitext(os.path.basename(outputFilehtm))[0])
    
    if os.name == 'posix':
        uploadTarget = MountSMBS(uploadTarget, os.path.join(os.path.dirname(workSpace), 'upload_point'))

    # Upload performance directory to server if it's performance run
    if IsUPloadPerfDir:
        PerfTypeDir = ''
        if ntpProject.lower() == "largeassembly":
            PerfTypeDir = 'Capacity'
        else:
            PerfTypeDir = 'Performance'
            
        if os.name == 'nt':
            if 'dev' in executeFile or 'staging' in executeFile or 'continusupdate' in executeFile:
                sourceResultDir = os.path.join(os.path.dirname(executeFile), 'Result', 'Neutron', 'Test', PerfTypeDir)
            else:
                sourceResultDir = os.path.join(os.path.dirname(executeFile), 'Neutron', 'Test', PerfTypeDir)
            copyFiles(sourceResultDir, os.path.join(os.path.join(uploadTarget, 'Performance'), os.path.basename(outputFile)))
            
        elif os.name == 'posix':
            if 'dev' in appFile or 'staging' in appFile or 'continusupdate' in appFile:
                sourceResultDir = os.path.join(os.path.dirname(appFile), 'Libraries', 'Neutron', 'Result', 'Neutron', 'Test', PerfTypeDir)
            else:
                sourceResultDir = os.path.join(os.path.dirname(appFile), 'Libraries', 'Neutron', 'Neutron', 'Test', PerfTypeDir)
            print 'Start to upload performance results to server: {0}'.format(sourceResultDir)
            print 'Destiny folder: {0}'.format(os.path.join(os.path.join(uploadTarget, 'Performance'), os.path.basename(outputFile)))
            copyFiles(sourceResultDir, os.path.join(os.path.join(uploadTarget, 'Performance'), os.path.basename(outputFile)))
            
    print("Finished copy results")
     
    if os.name == 'posix':
        UmountSMBS('upload_point')
    return True

def Usage():
    print 'RunCase.py usage:'
    print '-h, --help: print help message.'
    print '-p, --product: The product installed on system. '
    print '-v, --version: The version of build has been installed. '
    print '-f, --exefile: The exe file of this product. It will find exe file in current system by default'
    print '-n, --ntpproject: The NTest project file. '
    print '-j, --jobname: The job name in Jenkins'

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:v:f:n:j:', ['help', 'product=', 'version=', 'exefile=', 'ntpproject=', 'jobname='])
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)
    
    pyFile = os.path.abspath(sys.argv[0])
    workSpace = os.path.split(pyFile)[0]
    product = ''
    ntpProject = ''
    label = ''
    exeFile = ''
    jobname = ''
    for o, a in opts:
        if o in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif o in ('-p', '--product',):
            product = a
        elif o in ('-n', '--ntpproject',):
            ntpProject = a
        elif o in ('-v', '--version',):
            label = a
        elif o in ('-f', '--exefile',):
            exeFile = a
        elif o in ('-j', '--jobname',):
            jobname = a
        else:
            print 'unhandled option'
            sys.exit(2)
         
    if ntpProject == '' or label == '':
        print 'Please input required arguments!\n'
        Usage()
        sys.exit(1)
    
    configFilePath = os.path.join(workSpace, 'Config.xml')
    Config = Settings.Parameters(configFilePath) 
    
    OS = ''
    if exeFile == '' and product != '':
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
    else:
        print 'Please provide exe file path or product name.'
        sys.exit(1)
        
    if exeFile[0] == '~':
        exeFile = os.environ['HOME'] + exeFile[1:]
    
    processes = GetRelatedProcesses(product, OS)
    processes.insert(0, GetExeName(product, OS))
    if os.path.exists(exeFile): 
        if not Run(workSpace, exeFile, ntpProject, label, jobname, processes):
            print 'Failed to Run test cases.'
            sys.exit(1)
        else:
            print 'Finished Run all test cases'
    else:
        print 'Cannot find the execute file [{0}]'.format(exeFile)
        sys.exit(1)
