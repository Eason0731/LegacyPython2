# -*- coding: utf-8 -*-
import os
os.environ['NEUTRON_BUILD']="Debug"# Set environment variables
os.environ['NEUTRON_START_CLOUD']="NO"
os.environ['NEUTRON_LIVE_UPDATE']="DISABLE"
os.environ['BUILD_MACHINE']="Yes"
os.environ['SKIP_ENTITLEMENT']="Yes"

def SearchFusionPath():
    Dir = os.path.join (os.environ['localappdata'],'Autodesk','webdeploy')
    if os.path.exists(Dir):
        for root,dirs,filenames in os.walk(Dir):
            for myFile in filenames:
                if 'Fusion360.exe' in myFile:
                    FusionPath = root
                    if 'dev' in FusionPath:
                        print "Main Build exists on your PC"
                      
                    elif 'staging' in FusionPath:
                        print "RC Build exists on your PC"
                       
                        
                    elif 'continuousupdate' in FusionPath:
                        print "CU Build exists on your PC"
                        
                    OpenMultipleFusionBuilds(FusionPath,myFile)
                    
                    '''
                    print "FusionPath is: " + FusionPath
                    print "Filename is " + myFile
                    print "The Full Path of Fusion on your disk is: " + os.path.join(FusionPath,myFile)
                    return os.path.join(FusionPath,myFile)
                    '''
    else:
        print "Your Windows PC didn't install Fusion"
        
def OpenMultipleFusionBuilds(FusionPath,myFile):
    cc = raw_input ("Would you want to open this build?(Y/N)")
    if (cc.lower() == 'y'):
        os.system(r'start '+ os.path.join(FusionPath,myFile) + '')
    elif (cc.lower() == 'n'):
        print "You've canceled this operation"
    else:
        print "You've typed a wrong word!"
    

if __name__ == '__main__':
    SearchFusionPath()
