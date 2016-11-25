# Save the text as a py file. e.g.qa.py
import os #Load the related python modules

os.environ['NEUTRON_BUILD']="Debug"# Set environment variables
os.environ['NEUTRON_START_CLOUD']="NO"
os.environ['NEUTRON_LIVE_UPDATE']="DISABLE"
os.environ['BUILD_MACHINE']="Yes"
os.environ['SKIP_ENTITLEMENT']="Yes"

def LaunchFusion():
   if os.name == "nt": #OS name is "nt", then it should be Windows
       SearchFusionPath()
   else: # then assume it's Mac
      Fus = raw_input ("""Which Fusion Build installed on your Mac OS?
  1 -- Main
  2 -- RC
  3 -- CU
  4 -- Prodution
      
  Please Choose: """)

      if Fus == "1":
        MacPath = os.path.join('~', 'Applications', 'Autodesk\ Fusion\ 360\ [dev].app')
        os.system('open ' + MacPath)
      elif Fus == "2":
        MacPath = os.path.join('~', 'Applications', 'Autodesk\ Fusion\ 360\ [staging].app')
        os.system('open ' + MacPath)
      elif Fus == "3":
        MacPath = os.path.join('~', 'Applications', 'Autodesk\ Fusion\ 360\ [continuousupdate].app')
        os.system('open ' + MacPath)
      elif Fus == "4":
        MacPath = os.path.join('~', 'Applications', 'Autodesk\ Fusion\ 360.app')
        os.system('open ' + MacPath)

      
      else :
        print "Your have typed a wrong number!"

         
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
    #print "FusionPath is: " + FusionPath
    #print "Filename is " + myFile
    #print "The Full Path of Fusion on your disk is: " + os.path.join(FusionPath,myFile)
    cc = raw_input ("Would you want to open this build?(Y/N)")
    if (cc.lower() == 'y'):
        FusionLocalPath = os.path.join(FusionPath,myFile)
        os.system(r'start '+ FusionLocalPath + '')
        print FusionLocalPath
    elif (cc.lower() == 'n'):
        print "You've canceled this operation"
    else:
        print "You've typed a wrong word!"
    #return os.path.join(FusionPath,myFile)

if __name__ == '__main__':
   LaunchFusion()

   
