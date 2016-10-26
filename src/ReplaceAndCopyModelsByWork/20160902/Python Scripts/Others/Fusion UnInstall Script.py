import os

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

if __name__=='__main__':
    # Remove legacy files
    RemoveWebdeployDir()
    if os.name == 'nt':
        os.system('RD /s /q "C:\ProgramData\Autodesk\FusDoc"')
    
