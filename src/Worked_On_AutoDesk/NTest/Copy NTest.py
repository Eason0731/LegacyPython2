import os
import time
remoteDir=r'\\shacng839w11s\CIext'
label=r'2.1.3621'
OS=r'Win'

print time.strftime("Start Time:%Y-%m-%d %X",time.localtime()) 
installPath=r'C:\Users\t_zhanj\AppData\Local\Autodesk\webdeploy\dev\1ad3d94d72b616c9860aa3c2ae958c238ad9ef4e'
os.system("ROBOCOPY /e "+r'{0}\builds\{1}\{2}\NTest'.format(remoteDir, label, OS)+" "+installPath)
print("Copy NTest Successful");

remoteDir2=r'\\eptserver\dropbox\John'
filename=r'Fusion360.xml'
targetpath= installPath + r'\Applications\Fusion\Fusion360App'
os.system("XCOPY /r /y "+r'{0}\{1}'.format(remoteDir2, filename)+" "+targetpath)
print("Update Fusion360.xml Successful");
print time.strftime("Complete Time:%Y-%m-%d %X",time.localtime()) 
