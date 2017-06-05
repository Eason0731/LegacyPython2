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
                print "========Replace Content on txt files========"
                TestCasesDir = raw_input ("Please input the folder path: ")
                if os.path.exists(TestCasesDir):
                    ReplaceContentOnDir(TestCasesDir)
                else:
                    print "{0} is NOT Exist!" .format(TestCasesDir)
                    CountineOrExit()
                
            if int(a) == 2:
                print "===========Delete File or Folder============"
                TestCasesDir = raw_input ("Please input the folder or file path: ")
                if os.path.exists(TestCasesDir):
                    DeleteMethod(TestCasesDir)
                else:
                    print "{0} is NOT Exist!" .format(TestCasesDir)
                    CountineOrExit()

            if int(a) == 3:
                print "===========Copy File or Folder============="
                sourceCustomed = raw_input ("Please input the folder or file path: ")
                if os.path.exists(sourceCustomed):
                    if os.path.isfile(sourceCustomed):
                        CopyFiletoFolder(sourceCustomed)
                    elif os.path.isdir(sourceCustomed):
                        CopyFoldertoFolder(sourceCustomed)
                else :
                    print "source File or Folder: {0} is NOT Exist!" .format(sourceCustomed)
                    CountineOrExit()
            
            if int(a) == 4:
                print "===========Move File or Folder============="
                sourceFolder = raw_input ("Please input the source folder or file path: ")
                if os.path.exists(sourceFolder):
                    MoveFoldertoFolder(sourceFolder)
                else:
                    print "{0} is NOT Exist!" .format(sourceFolder)
                    CountineOrExit()
                    

            if int(a) == 5:
                print "=========Find Contents on txt files========"
                Path  = raw_input ("Please input the folder path: ")
                if os.path.exists(Path):   
                    FindContentOnTxt(Path)
                else:
                    print "{0} is NOT Exist!" .format(Path)
                    CountineOrExit()
                
            if int(a) == 6:
                print "============Find Files on Folder==========="
                Path  = raw_input ("Please input the folder path: ")
                if os.path.exists(Path):
                    FindFilesonDirs(Path)
                else:
                    print "{0} is NOT Exist!" .format(Path)
                    CountineOrExit()


            if int(a) == 7:
                print "===========Rename File or Folder==========="
                Oname = raw_input ("Please input the folder or file path: ")
                if os.path.exists(Oname):          
                    ReplaceName(Oname)
                else:
                    print "{0} is NOT Exist!" .format(Oname)
                    CountineOrExit()


            if int(a) == 8:
                print "====Replace File Name With SpecificName===="
                FolderDir = raw_input ("Please input the folder path: ")
                if os.path.exists(FolderDir):
                    ReplaceFileNameWithSpecificName(FolderDir)
                else:
                    print "{0} is NOT Exist!" .format(FolderDir)
                    CountineOrExit()
    
        else:
            print "Bye~"
            exit(1)

    else:
        print "Bye~"
        exit(1)
      

def ReplaceContentOnDir(TestCasesDir):
    s = raw_input("Please input what word you want to find: ")
    p = raw_input("Please input what word you want to replace: ")
    t = 0
    c = 0
    print "================================ Start ================================"
    for root,dirnames,filenames in os.walk(TestCasesDir):
        for myFile in filenames:
            TxtFile = os.path.join(root,myFile)
            if "txt" in myFile:
                t = t + 1  
                files = open (TxtFile,'r') 
                content = files.read()
                files.close()
                
                if s in content:
                    c+=1         
                    files = open (TxtFile,'w') 
                    files.writelines(content.replace (s, p))
                    files.close()
                    print s + " has been replaced as " + p + " on file "+ TxtFile +" succeeded!"              
                files.close()

    if c == 0 and t != 0:
        print s + " didn't found on " + TestCasesDir
    if c == 0 and t == 0:
        print "There is no txt files under folder " + TestCasesDir
    print "================================ Finish ==============================="     
    CountineOrExit()

def DeleteMethod(TestCasesDir):
    print "Deleteing " + TestCasesDir + " now..."
    print "============================================"
    if os.path.isfile(TestCasesDir):
        os.remove(TestCasesDir)
    elif os.path.isdir(TestCasesDir):
        shutil.rmtree(TestCasesDir)
    
    if not os.path.exists(TestCasesDir):
        print  TestCasesDir + " has been deleted succeeded!"
    else:
        print  TestCasesDir + " has been deleted failed!"
    print "============================================"    
    CountineOrExit()
        

def CopyFoldertoFolder(sourceCustomed):
    TargetCustomed = raw_input ("Please input the target folder path: ")
    if not os.path.exists(TargetCustomed):
        os.makedirs(TargetCustomed)
            
    Type = sourceCustomed.split("\\")[-1]
    TargetCustomed = os.path.join(TargetCustomed,Type)
    if os.path.exists(TargetCustomed):
        while(1):
            IsConver = raw_input ("There is a same folder on target folder , would you still want to copy? (Y/N) ")
            if IsConver.lower() == 'y':
                break
            elif IsConver.lower() == 'n':
                CountineOrExit()
    print "============================================"
    print ("SourceFolder is : {0} " .format(sourceCustomed))
    print time.strftime("Start Copy Time :%Y-%m-%d %X",time.localtime())
    if not os.listdir(sourceCustomed):
        shutil.copytree(sourceCustomed,TargetCustomed)
    else:
        copyFiles(sourceCustomed,TargetCustomed)
    print sourceCustomed + " have copied succeeded to folder " + TargetCustomed
    print time.strftime("End Copy Time :%Y-%m-%d %X",time.localtime())
    print "============================================"
    
    CountineOrExit()

def CopyFiletoFolder(TestCasesDir):
    sourceFile = TestCasesDir
    TargetFolder = raw_input ("Please input the target folder path: ")
    pathname,filename = os.path.split (sourceFile)
    if not os.path.exists(TargetFolder):
        os.makedirs(TargetFolder)

    if os.path.exists(os.path.join(TargetFolder,sourceFile.split("\\")[-1])):
        while(1):
            IsConver = raw_input ("There is a same file on target file , would you still want to copy? (Y/N) ")
            if IsConver.lower() == 'y':
                break
            elif IsConver.lower() == 'n':
                CountineOrExit()
    print "============================================"
    print time.strftime("Start Copy Time :%Y-%m-%d %X",time.localtime())
    shutil.copy (sourceFile,TargetFolder) 
    print sourceFile + " has been copied to " + TargetFolder + " succeeded!"
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


def MoveFoldertoFolder(sourceFolder):
    targetFolder = raw_input ("Please input the target folder path: ")
    print "============================================"
    if not os.path.exists(targetFolder):
        os.makedirs(targetFolder)
    
    Type = sourceFolder.split("\\")[-1]
    targetFolder = os.path.join(targetFolder,Type)
    if os.path.exists(targetFolder):
        while(1):
            if os.path.isfile(targetFolder):
                IsConver = raw_input ("There is a same file on target file , would you still want to move? (Y/N) ")
            elif os.path.isdir(targetFolder):
                IsConver = raw_input ("There is a same folder on target folder , would you still want to move? (Y/N) ")
                    
            if IsConver.lower() == 'y':
                break
            elif IsConver.lower() == 'n':
                CountineOrExit()

    if os.path.isfile(sourceFolder):
        if os.path.exists(targetFolder):
            os.remove(targetFolder)
        shutil.move (sourceFolder,targetFolder)

    elif os.path.isdir(sourceFolder):
        if not os.listdir(sourceFolder):
            shutil.copytree(sourceFolder,targetFolder)
        else:
            copyFiles(sourceFolder,targetFolder)                    
        shutil.rmtree(sourceFolder)

    if os.path.exists(targetFolder):
        print sourceFolder + " has been moved to " + targetFolder + " succeeded!"
    else:
        print sourceFolder + " has been moved failed!"

    print "============================================"
    CountineOrExit()


def FindContentOnTxt(Path):
    Content = raw_input ("What content you want to find on txt file? ")
    j = 0
    w = 0
    print "================================ Start ==============================="
    for root,dirnames,filenames in os.walk(Path):
        for myFile in filenames:
            TxtFile = os.path.join(root,myFile)
            i=0          
            if 'txt' in myFile:
                j = j + 1
                
                f = open (TxtFile, 'r')
                Filecontent = f.readlines()
                for eachline in Filecontent:
                    if Content.lower() in eachline.lower():
                        i+= 1
                        w+= 1
                
                if i > 0:
                    print Content + " found on " + TxtFile + " for " + str(i) + " times"
                
                f.close()

    if w == 0:
        print Content + " didn't found on " + Path
                    
    if j == 0:
        print "There is no txt files under folder " + Path
    print "================================ Finish ==============================="
    CountineOrExit()
                
def FindFilesonDirs(Path):
    File = raw_input ("What file you want to find on this folder? ")
    k = 0
    for root,dirnames,filenames in os.walk(Path):
        for myFile in filenames:
            if File.lower() in myFile.lower():
                k = k + 1
                print "File: " + File + " has found on " + root               
    if k == 0:
        print "File: " + File + " didn't found on " + Path

    CountineOrExit()
            
def ReplaceName(Oname):
    Rname = raw_input ("Please input new name want to replace: ")
    Oname = os.path.abspath(Oname)
    Rname = os.path.join(os.path.split(Oname)[0],Rname)   
    print "============================================"
    if os.path.exists(Rname):
        print Oname + " has already exists, cannot be renamed!"
    else:
        os.rename (Oname,Rname)
        print Oname + " has been renamed as " + Rname +" succeeded!"
    print "============================================"
    CountineOrExit()

def ReplaceFileNameWithSpecificName(FolderDir):
    FindContent = raw_input("What word do you want find? ")
    FindContent = FindContent.lower()
    ReplaceContent = raw_input("What word do you want replace? ")
    w = 0
    print "============================================"
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
                    print OldNameFile +" has been replaced as " + NewNameFile + " succeeded!"
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

    

