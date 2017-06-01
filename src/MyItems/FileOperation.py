# -*- coding: utf-8 -*-
import os
import re
import shutil
import time

def MainFunction():
    a = raw_input ("""
==========Welcome to File Operation==========
1. Replace Content on txt files
2. Delete File or Folder
3. Copy File or Folder
4. Move File or Folder
5. Find Contents on txt files
6. Find Files on Folder
7. Rename File or Folder
8. Replace File Name With SpecificName
=============================================
Press AnyKey to Exit
        
Please choose : """)

    if a.isdigit():
        if int(a) in range(1,9):
            if int(a) == 1:
                TestCasesDir = raw_input ("Please Input your folder Path: ")
                if os.path.exists(TestCasesDir):
                    s = raw_input("Please Input what words you want to find: ")
                    p = raw_input("Please Input what words you want to replace: ")
                    ReplaceContentOnDir(TestCasesDir,s,p)
                else:
                    print "This folder path not exist!"
                    CountineOrExit()
                
            if int(a) == 2:
                TestCasesDir = raw_input ("Please Input your folder or file path: ")
                if os.path.exists(TestCasesDir):
                    DeleteMethod(TestCasesDir)
                else:
                    print TestCasesDir + " is not exist!"
                    CountineOrExit()

            if int(a) == 3:
                sourceCustomed = raw_input ("Please Input your folder or file Path: ")
                if os.path.exists(sourceCustomed):
                    if os.path.isfile(sourceCustomed):
                         CopyFiletoFolder(sourceCustomed)
                    elif os.path.isdir(sourceCustomed):
                        CopyFoldertoFolder(sourceCustomed)
                else :
                    print "source File or Folder: {0} is NOT Exist!" .format(sourceCustomed)
                    CountineOrExit()
            
            if int(a) == 4:
                MoveFoldertoFolder()

            if int(a) == 5:
                Path  = raw_input ("Please input the folder path with txt files:")
                if os.path.exists(Path):
                    Content = raw_input ("What content you want to find on txt file?")
                    FindContentOnTxt(Path,Content)
                else:
                    print Path + " not exists!"
                    CountineOrExit()
                
            if int(a) == 6:
                Path  = raw_input ("Please input your folder path:")
                if os.path.exists(Path):
                    File = raw_input ("What file you want to find on this folder?")
                    FindFilesonDirs(Path,File)
                else:
                    print Path + " not exists!"
                    CountineOrExit()


            if int(a) == 7:
                Oname = raw_input ("Input your file or folder path: ")
                if os.path.exists(Oname):          
                    Rname = raw_input ("Input new folder name want to replace: ")
                    ReplaceName(Oname,Rname)
                else:
                    print Oname + " is not exists!"
                    CountineOrExit()


            if int(a) == 8:
                FolderDir = raw_input ("Please input folder: ")
                if os.path.exists(FolderDir):
                    FindContent = raw_input("What word do you want find?")
                    FindContent = FindContent.lower()
                    ReplaceContent = raw_input("What word do you want replace?")
                    ReplaceFileNameWithSpecificName(FolderDir,FindContent,ReplaceContent)
                else:
                    print "Target Folder path: " + FolderDir + " is not exists!"
                    CountineOrExit()
    
        else:
            print "Bye~"
            exit(1)

    else:
        print "Bye~"
        exit(1)
      

def ReplaceContentOnDir(TestCasesDir,s,p):
    i = 0
    for root,dirnames,filenames in os.walk(TestCasesDir):
        for myFile in filenames:
            TxtFile = os.path.join(root,myFile)
            if "txt" in myFile:
                i = i + 1
                print "================================ Start ================================"
                print "File on " + TxtFile   
                files = open (TxtFile,'r') 
                content = files.read()
                files.close()
                
                if s in content:
                    print "Found word: " + s + " in File " + myFile
                
                    files = open (TxtFile,'w') 
                    files.writelines(content.replace (s, p))
                    files.close()
                    print s + " has been replaced as " + p + " Success!"
                
                else:
                    print s + " Not found on File!"   
                    
                files.close()
                print "================================ Finish ==============================="
                print "                                                                       "

    if i == 0:
        print "There is no txt files under folder " + TestCasesDir
                
    CountineOrExit()

def DeleteMethod(TestCasesDir):
    print "Deleteing " + TestCasesDir + " now..."
    if os.path.isfile(TestCasesDir):
        os.remove(TestCasesDir)
    elif os.path.isdir(TestCasesDir):
        shutil.rmtree(TestCasesDir)
    
    if not os.path.exists(TestCasesDir):
        print  TestCasesDir + " has been deleted succeeded!"
    else:
        print  TestCasesDir + " has been deleted failed!"
            
    CountineOrExit()
        

def CopyFoldertoFolder(sourceCustomed):
    TargetCustomed = raw_input ("please input TargetFolder: ")
    if not os.path.exists(TargetCustomed):
        os.makedirs(TargetCustomed)
            
    Type = sourceCustomed.split("\\")[-1]
    TargetCustomed = os.path.join(TargetCustomed,Type)
    if os.path.exists(TargetCustomed):
        while(1):
            IsConver = raw_input ("There is a same folder on target folder , would you like to cover? (Y/N) ")
            if IsConver.lower() == 'y':
                break
            elif IsConver.lower() == 'n':
                CountineOrExit()
    
    print ("SourceFolder is : {0} " .format(sourceCustomed))
    print time.strftime("Start Copy Time :%Y-%m-%d %X",time.localtime())
    if not os.listdir(sourceCustomed):
        shutil.copytree(sourceCustomed,TargetCustomed)
    else:
        copyFiles(sourceCustomed,TargetCustomed)
    print sourceCustomed + " have copied successfully to folder " + TargetCustomed
    print time.strftime("End Copy Time :%Y-%m-%d %X",time.localtime())
    print "============================================"
    
    CountineOrExit()

def CopyFiletoFolder(TestCasesDir):
    sourceFile = TestCasesDir
    TargetFolder = raw_input ("Please input Target Folder:")
    pathname,filename = os.path.split (sourceFile)
    if not os.path.exists(TargetFolder):
        os.makedirs(TargetFolder)

    if os.path.exists(os.path.join(TargetFolder,sourceFile.split("\\")[-1])):
        while(1):
            IsConver = raw_input ("There is a same file on target file , would you like to cover? (Y/N) ")
            if IsConver.lower() == 'y':
                break
            elif IsConver.lower() == 'n':
                CountineOrExit()

    print time.strftime("Start Copy Time :%Y-%m-%d %X",time.localtime())
    shutil.copy (sourceFile,TargetFolder) 
    print sourceFile + " has been copied to " + TargetFolder + " successfully!"
    print time.strftime("End Copy Time :%Y-%m-%d %X",time.localtime())
    print "============================================"
   
    CountineOrExit()
            
        

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


def MoveFoldertoFolder():
    sourceFolder = raw_input ("Please input sourceFolder or Filepath:")
    targetFolder = raw_input ("Please input targetFolder:")
    if not os.path.exists(targetFolder):
        os.makedirs(targetFolder)
    
    if os.path.exists(sourceFolder):
        if os.path.isfile(sourceFolder):
            Type = sourceFolder.split("\\")[-1]
            targetFolder = os.path.join(targetFolder,Type)
            if os.path.exists(targetFolder):
                while(1):
                    IsConver = raw_input ("There is a same file on target file , would you like to cover? (Y/N) ")
                    if IsConver.lower() == 'y':
                        break
                    elif IsConver.lower() == 'n':
                        CountineOrExit()
                os.remove(targetFolder)
  
            shutil.move (sourceFolder,targetFolder)
        
        if os.path.isdir(sourceFolder):
            Type = sourceFolder.split("\\")[-1]
            targetFolder = os.path.join(targetFolder,Type)
            if os.path.exists(targetFolder):
                while(1):
                    IsConver = raw_input ("There is a same folder on target folder , would you like to cover? (Y/N) ")
                    if IsConver.lower() == 'y':
                        break
                    elif IsConver.lower() == 'n':
                        CountineOrExit()

                if not os.listdir(sourceFolder):
                    shutil.copytree(sourceFolder,targetFolder)
                else:
                    copyFiles(sourceFolder,targetFolder)   

                shutil.rmtree(sourceFolder)
        
        if os.path.exists(targetFolder):
            print sourceFolder + " have been moved to " + targetFolder + " succeeded!"
        else:
            print sourceFolder + " have been moved failed!"

    else:
        print sourceFolder +" is not exists!"
    
    CountineOrExit()


def FindContentOnTxt(Path,Content):
    j = 0
    for root,dirnames,filenames in os.walk(Path):
        for myFile in filenames:
            TxtFile = os.path.join(root,myFile)
            flag = ""
            i=0          
            if 'txt' in myFile:
                j = j + 1             
                f = open (TxtFile, 'r')
                Filecontent = f.readlines()
                for eachline in Filecontent:
                    
                    if Content.lower() in eachline.lower():
                        flag = "true"
                        i+=1
                        
                if flag == "true":
                    print Content + " found on " + myFile + " for " + str(i) + " times"
                
                else:
                    print Content + " didn't found on " + myFile
                    
                           
                f.close()

    if j == 0:
        print "There is no txt files under folder " + Path
    
    CountineOrExit()
                
def FindFilesonDirs(Path,File):
    k = 0
    for root,dirnames,filenames in os.walk(Path):
        for myFile in filenames:
            if File.lower() in myFile.lower():
                k = k + 1
                print "File: " + File + " has found on " + root               
    if k == 0:
        print "File: " + File + " didn't found on " + Path

    CountineOrExit()
            
def ReplaceName(Oname,Replacename):
    Oname=os.path.abspath(Oname)
    Replacename = os.path.join(os.path.split(Oname)[0],Replacename)    
    if os.path.exists(Replacename):
        print Oname + " has already exists, can not be renamed!"
    else:
        os.rename (Oname,Replacename)
        print Oname + " has been renamed as " + Replacename +" successfully!"
    
    CountineOrExit()

def ReplaceFileNameWithSpecificName(FolderDir,FindContent,ReplaceContent):
    w = 0
    for root,dirs,filenames in os.walk(FolderDir):
        for myFile in filenames:
            myFile = myFile.lower()  
            if FindContent in myFile:
                w = w + 1
                OldNameFile = os.path.join(root,myFile)
                myFile = myFile.replace (FindContent,ReplaceContent)
                NewNameFile = os.path.join(root,myFile)
                os.rename (OldNameFile,NewNameFile)
                if os.path.exists(NewNameFile):
                    print OldNameFile +" has been replaced as " + NewNameFile + " Successfully!"
                    print "========================================"
    if w == 0:
        print "Didn't found file named with " + FindContent + " under folder " + FolderDir
    
    CountineOrExit()              

def CountineOrExit():
    IsExit = raw_input ("Countine(Y) or Exit(N)? ")
    while(1):
        if IsExit.upper() == "Y":
            MainFunction()
        elif IsExit.upper() == "N":
            print "Bye~"
            exit(0)
        else:
            print "You have inputed the illegal character,try again!"
            CountineOrExit()
            break
            
            
            
if __name__=='__main__':
    MainFunction()

    

