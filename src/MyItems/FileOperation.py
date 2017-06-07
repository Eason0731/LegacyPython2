# -*- coding: utf-8 -*-
import os
import re
import shutil
import time

def MainFunction():
    a = raw_input ("""
==========Welcome to File Operation==========
1. Replace content on txt files
2. Delete file or folder
3. Copy file or folder
4. Move file or folder
5. Find contents on txt files
6. Find files or folder on folder
7. Rename file or folder
8. Rename file with specificname
=============================================
Press AnyKey to Exit
        
Please choose : """)

    if a.isdigit():
        if int(a) in range(1,9):
            if int(a) == 1:
                print "========Replace content on txt files========"
                TestCasesDir = raw_input ("Please input the folder path: ")
                if os.path.exists(TestCasesDir):
                    ReplaceContentOnDir(TestCasesDir)
                elif not TestCasesDir.strip():
                    EmptyReturn()
                else:
                    print "{0} is NOT Exist!" .format(TestCasesDir)
                    CountineOrExit()
                
            if int(a) == 2:
                print "===========Delete file or folder============"
                TestCasesDir = raw_input ("Please input the folder or file path: ")
                if os.path.exists(TestCasesDir):
                    DeleteMethod(TestCasesDir)
                elif not TestCasesDir.strip():
                    EmptyReturn()
                else:
                    print "{0} is NOT Exist!" .format(TestCasesDir)
                    CountineOrExit()

            if int(a) == 3:
                print "===========Copy file or folder============="
                sourceCustomed = raw_input ("Please input the folder or file path: ")
                if os.path.exists(sourceCustomed):
                    CopyMethod(sourceCustomed)
                elif not sourceCustomed.strip():
                    EmptyReturn()
                else :
                    print "source File or Folder: {0} is NOT Exist!" .format(sourceCustomed)
                    CountineOrExit()
            
            if int(a) == 4:
                print "===========Move file or folder============="
                sourceFolder = raw_input ("Please input the source folder or file path: ")
                if os.path.exists(sourceFolder):
                    MoveMethod(sourceFolder)
                elif not sourceFolder.strip():
                    EmptyReturn()
                else:
                    print "{0} is NOT Exist!" .format(sourceFolder)
                    CountineOrExit()
                    

            if int(a) == 5:
                print "=========Find contents on txt files========"
                Path  = raw_input ("Please input the folder path: ")
                if os.path.exists(Path):   
                    FindContentOnTxt(Path)
                elif not Path.strip():
                    EmptyReturn()
                else:
                    print "{0} is NOT Exist!" .format(Path)
                    CountineOrExit()
                
            if int(a) == 6:
                print "============Find files on folder==========="
                Path  = raw_input ("Please input the folder path: ")
                if os.path.exists(Path):
                    FindFilesonDirs(Path)
                elif not Path.strip():
                    EmptyReturn()
                else:
                    print "{0} is NOT Exist!" .format(Path)
                    CountineOrExit()


            if int(a) == 7:
                print "===========Rename file or folder==========="
                Oname = raw_input ("Please input the folder or file path: ")
                if os.path.exists(Oname):          
                    ReplaceName(Oname)
                elif not Oname.strip():
                    EmptyReturn()
                else:
                    print "{0} is NOT Exist!" .format(Oname)
                    CountineOrExit()


            if int(a) == 8:
                print "=======Rename file with specificname======"
                FolderDir = raw_input ("Please input the folder path: ")
                if os.path.exists(FolderDir):
                    ReplaceFileNameWithSpecificName(FolderDir)
                elif not FolderDir.strip():
                    EmptyReturn()
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
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
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
                    print "   "
                files.close()
                

    if c == 0 and t != 0:
        print s + " didn't found on " + TestCasesDir
    if c == 0 and t == 0:
        print "There is no txt files under folder " + TestCasesDir
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="     
    CountineOrExit()

def DeleteMethod(TestCasesDir):
    print "================================ Start ================================"
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    print "Deleteing " + TestCasesDir + " now..."
    if os.path.isfile(TestCasesDir):
        os.remove(TestCasesDir)
    elif os.path.isdir(TestCasesDir):
        shutil.rmtree(TestCasesDir)
    
    if not os.path.exists(TestCasesDir):
        print  TestCasesDir + " has been deleted succeeded!"
    else:
        print  TestCasesDir + " has been deleted failed!"
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="    
    CountineOrExit()
        

def CopyMethod(sourceCustomed):
    TargetCustomed = raw_input ("Please input the target folder path: ")
    if not os.path.exists(TargetCustomed):
        os.makedirs(TargetCustomed)          
    Type = sourceCustomed.split("\\")[-1]
    TargetCustomed = os.path.join(TargetCustomed,Type)
    if os.path.exists(TargetCustomed):
        while(1):
            if os.path.isdir(TargetCustomed):
                IsConver = raw_input ("There is a same folder on target folder , would you still want to copy? (Y/N) ")            
            elif os.path.isfile(TargetCustomed):
                IsConver = raw_input ("There is a same file on target file , would you still want to copy? (Y/N) ")
            if IsConver.lower() == 'y':
                if os.path.isdir(TargetCustomed):
                    if not os.listdir(sourceCustomed) and not os.listdir(TargetCustomed):
                        shutil.rmtree(TargetCustomed) 
                break
            elif IsConver.lower() == 'n':
                CountineOrExit()
    print "================================ Start ================================"
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    if os.path.isdir(sourceCustomed):
        if not os.listdir(sourceCustomed):
            shutil.copytree(sourceCustomed,TargetCustomed)
        else:
            copyFiles(sourceCustomed,TargetCustomed)
    elif os.path.isfile(sourceCustomed):
        shutil.copy (sourceCustomed,TargetCustomed) 
    print sourceCustomed + " has copied succeeded to folder " + TargetCustomed
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ===============================" 
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


def MoveMethod(sourceFolder):
    targetFolder = raw_input ("Please input the target folder path: ")
    print "================================ Start ================================"
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
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
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="
    CountineOrExit()


def FindContentOnTxt(Path):
    Content = raw_input ("What content you want to find on txt file? ")
    t = 0
    c = 0
    print "================================ Start ==============================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    for root,dirnames,filenames in os.walk(Path):
        for myFile in filenames:
            TxtFile = os.path.join(root,myFile)
            i=0          
            if 'txt' in myFile:
                t = t + 1
                
                f = open (TxtFile, 'r')
                Filecontent = f.readlines()
                for eachline in Filecontent:
                    if Content.lower() in eachline.lower():
                        i+= 1
                        c+= 1
                
                if i > 0:
                    print Content + " found on " + TxtFile + " for " + str(i) + " times"
                    print "   "
                f.close()
    if c == 0 and t != 0:
        print Content + " didn't found on " + Path
                    
    if c == 0 and t == 0:
        print "There is no txt files under folder " + Path
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="
    CountineOrExit()
                
def FindFilesonDirs(Path):
    File = raw_input ("What file or folder you want to find on this folder? ")
    k = 0
    print "================================ Start ==============================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    for root,dirnames,filenames in os.walk(Path):
        if os.path.isfile(os.path.join(Path,File)):
            for myFile in filenames:
                if File.lower() in myFile.lower():
                    k = k + 1
                    print "File: " + File + " has found on " + root
                    print "  "
        elif os.path.isdir(os.path.join(Path,File)):
            for myFolder in dirnames:
                if File.lower() in myFolder.lower():
                    k = k + 1
                    print "Folder: " + File + " has found on " + root
                    print "  "   
    if k == 0:
        print "File: " + File + " didn't found on " + Path
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="
    CountineOrExit()
            
def ReplaceName(Oname):
    Rname = raw_input ("Please input new name want to replace: ")
    Oname = os.path.abspath(Oname)
    Rname = os.path.join(os.path.split(Oname)[0],Rname)   
    print "================================ Start ==============================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    if os.path.exists(Rname):
        print Oname + " has already exists, cannot be renamed!"
    else:
        os.rename (Oname,Rname)
        print Oname + " has been renamed as " + Rname +" succeeded!"
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="
    CountineOrExit()

def ReplaceFileNameWithSpecificName(FolderDir):
    FindContent = raw_input("What word do you want find? ")
    FindContent = FindContent.lower()
    ReplaceContent = raw_input("What word do you want replace? ")
    w = 0
    print "================================ Start ==============================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
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
                    print "   "
    if w == 0:
        print "Didn't found file named with " + FindContent + " under folder " + FolderDir
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="
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
            
def EmptyReturn():
    print "Please do not input the empty infos"
    CountineOrExit()
    
            
if __name__=='__main__':
    MainFunction()

    

