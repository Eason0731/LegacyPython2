# Save the text as a py file. e.g.qa.py
import os #Load the related python modules

os.environ['NEUTRON_BUILD']="Debug"# Set environment variables
os.environ['NEUTRON_START_CLOUD']="NO"
os.environ['NEUTRON_LIVE_UPDATE']="DISABLE"
os.environ['BUILD_MACHINE']="Yes"
os.environ['SKIP_ENTITLEMENT']="Yes"


if os.name == "nt": #OS name is "nt", then it should be Windows
   os.system(r'start C:\Users\t_zhanj\AppData\Local\Autodesk\webdeploy\dev\62eaebf62854eb8e29a617d46edd30de064209be\Fusion360.exe')
else: # then assume it's Mac
   os.system('open "/Users/Main/Library/Application Support/Autodesk/webdeploy/dev/e978c96f76e0efcd76ee90df595063eb337a1983/Autodesk Fusion 360 [dev].app"')

   
