# Save the text as a py file. e.g.qa.py
import os #Load the related python modules
import platform

os.environ['NEUTRON_BUILD']="Debug"# Set environment variables
os.environ['NEUTRON_START_CLOUD']="NO"
os.environ['NEUTRON_LIVE_UPDATE']="DISABLE"
os.environ['BUILD_MACHINE']="Yes"
os.environ['SKIP_ENTITLEMENT']="Yes"

def LaunchFusion():
    SearchFusionPath()
         
def SearchFusionPath():
    if platform.system() == 'Windows':
        Dir = os.path.join (os.environ['localappdata'],'Autodesk','webdeploy')
        if os.path.exists(Dir):
            for root,dirs,filenames in os.walk(Dir):
                for myFile in filenames:
                    if 'Fusion360.exe' in myFile:
                        FusionPath = root
                        Version = getFileVersion(os.path.join(FusionPath,myFile))
                        if 'dev' in FusionPath:
                            print "Main Build "+ Version +" exists on your PC"
                      
                        elif 'staging' in FusionPath:
                            print "RC Build "+ Version +" exists on your PC"
                       
                        elif 'continuousupdate' in FusionPath:
                            print "CU Build "+ Version +" exists on your PC"
                    
                        elif 'production' in FusionPath:
                            print "Production Build "+ Version +" exists on your PC"
                        
                        OpenMultipleFusionBuilds(FusionPath,myFile)
                    
                    '''
                    print "FusionPath is: " + FusionPath
                    print "Filename is " + myFile
                    print "The Full Path of Fusion on your disk is: " + os.path.join(FusionPath,myFile)
                    return os.path.join(FusionPath,myFile)
                    '''
        else:
            print "Your Windows PC didn't install Fusion"
    
    elif platform.system() == 'Darwin':
        Dir = os.path.join(os.environ['HOME'], 'Library','Application Support','Autodesk','webdeploy')
        MacPath = ""
        #Dir = os.path.join (os.environ['localappdata'],'Autodesk','webdeploy')
        if os.path.exists(Dir):
            for root,dirs,filenames in os.walk(Dir):
                for myFile in filenames:
                    FusionPath = root
                    
                    if os.path.join('Autodesk Fusion 360 [dev].app','Contents','Info.plist') in os.path.join(root,myFile):
                        #if 'dev' in FusionPath:
                        FullPath = os.path.join(FusionPath,myFile)
                        Version = getFileVersion(FullPath)
                        print "Main Build " + Version +" exists on your Mac"
                        #print "FusionPath is: " + FusionPath
                        #print "Filename is " + myFile
                        #print "The Full Path of Fusion on your disk is: " + FullPath

                        #MacPath = os.path.join('~', 'Applications', 'Autodesk\ Fusion\ 360\ [dev].app')
                        MacPath = (('/').join(FusionPath.split("/")[:-1])).replace(' ','\ ') #Use '\ ' to replace space, which take effect!
                        OpenMultipleFusionBuilds(MacPath,'')
                        #rint "Open Path is: " +  (('/').join(FusionPath.split("/")[:-1])).replace(' ','\ ')
                        
                        
                                          
                    elif os.path.join('Autodesk Fusion 360 [staging].app','Contents','Info.plist') in os.path.join(root,myFile):
                        FullPath = os.path.join(FusionPath,myFile)
                        Version = getFileVersion(FullPath)
                        print "RC Build " + Version +" exists on your Mac"
                        #print "FusionPath is: " + FusionPath
                        #print "Filename is " + myFile
                        #print "The Full Path of Fusion on your disk is: " + FullPath
                        #MacPath = os.path.join('~', 'Applications', 'Autodesk\ Fusion\ 360\ [staging].app')
                        MacPath = (('/').join(FusionPath.split("/")[:-1])).replace(' ','\ ')
                        OpenMultipleFusionBuilds(MacPath,'')
                        #print "Open Path is: " +  ('/').join(FusionPath.split("/")[:-1])
                                               
                    elif os.path.join('Autodesk Fusion 360 [continuousupdate].app','Contents','Info.plist') in os.path.join(root,myFile):
                        FullPath = os.path.join(FusionPath,myFile)
                        Version = getFileVersion(FullPath)
                        print "CU Build " + Version +" exists on your Mac"
                        #print "FusionPath is: " + FusionPath
                        #print "Filename is " + myFile
                        #print "The Full Path of Fusion on your disk is: " + FullPath
                        #MacPath = os.path.join('~', 'Applications', 'Autodesk\ Fusion\ 360\ [continuousupdate].app')
                        MacPath = (('/').join(FusionPath.split("/")[:-1])).replace(' ','\ ')
                        OpenMultipleFusionBuilds(MacPath,'')
                        #print "Open Path is: " +  ('/').join(FusionPath.split("/")[:-1])
                    
                    elif os.path.join('Autodesk Fusion 360.app','Contents','Info.plist') in os.path.join(root,myFile):
                        FullPath = os.path.join(FusionPath,myFile)
                        Version = getFileVersion(FullPath)
                        print "Production Build " + Version +" exists on your Mac"
                        #print "FusionPath is: " + FusionPath
                        #print "Filename is " + myFile
                        #print "The Full Path of Fusion on your disk is: " + FullPath
                        #MacPath = os.path.join('~', 'Applications', 'Autodesk\ Fusion\ 360.app')
                        MacPath = (('/').join(FusionPath.split("/")[:-1])).replace(' ','\ ')
                        OpenMultipleFusionBuilds(MacPath,'')
                        #print "Open Path is: " +  ('/').join(FusionPath.split("/")[:-1])        
        else:
            print "Your MAC didn't install Fusion"    
        
def OpenMultipleFusionBuilds(FusionPath,myFile):
    #print "FusionPath is: " + FusionPath
    #print "Filename is " + myFile
    #print "The Full Path of Fusion on your disk is: " + os.path.join(FusionPath,myFile)    
    cc = raw_input ("Would you want to open this build?(Y/N)")
    if (cc.lower() == 'y'):
        FusionLocalPath = os.path.join(FusionPath,myFile)
        if platform.system() == 'Windows':
            os.system(r'start '+ FusionLocalPath + '')
        elif platform.system() == 'Darwin':
            os.system('open '+ FusionLocalPath + '')
        print FusionLocalPath
    elif (cc.lower() == 'n'):
        print "You've canceled this operation"
    else:
        print "You've typed a wrong word!"
    #return os.path.join(FusionPath,myFile)


def getFileVersion(file_name):   
    
    if platform.system() == 'Windows': #Windows
        import win32api
        info = win32api.GetFileVersionInfo(file_name, os.sep)
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version = '%d.%d.%d' % (win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.HIWORD(ms))
        return version
    
    elif platform.system() == 'Darwin': #Mac
        import plistlib
        p1 = plistlib.readPlist(file_name)
        BundleVersion = p1["CFBundleVersion"]
        return BundleVersion

if __name__ == '__main__':
   LaunchFusion()

   
