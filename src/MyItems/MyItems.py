# -*- coding: utf-8 -*-
import os
import re
import shutil
import time

def MainFunction():
    a = raw_input ("""
1. Replace Content on txt files
2. Delete Folders
3. Delete Files
4. Copy Folder to Folder
5. Copy Files or Folder
6. Move Folder or files to Folder
7. Find Contents on txt files
8. Find Files on Folder
9. Rename Folder
10. Rename File
11. Replace File Name With SpecificName

Press AnyKey to Exit
        
Please choose : """)
    if (a == "1" or a == "2" or a == "3" or a == "4" or a == "5" or a == "6" or a == "7" or a == "8" or a == "9" or a == "10" or a =="11"):
        
        #TestCasesDir = raw_input ("Please Input your folder or file Path: ")

        if a == "1":
            TestCasesDir = raw_input ("Please Input your folder Path: ")
            s = raw_input("Please Input what words you want to find: ")
            p = raw_input("Please Input what words you want to replace: ")

            #TestCasesDir = "C:\\Users\\t_zhanj\\Desktop\\Cases"
            if os.path.exists(TestCasesDir):
                ReplaceContentOnDir(TestCasesDir,s,p)
            else:
                print "This folder path not exist!"
                CountineOrExit()
                
        if a == "2":
            TestCasesDir = raw_input ("Please Input your folder Path: ")
            if os.path.exists(TestCasesDir):
                DeleteFolders(TestCasesDir)
            else:
                print "This folder path not exist!"
                CountineOrExit()

        if a == "3":
            TestCasesDir = raw_input ("Please Input your file Path: ")
            if os.path.exists(TestCasesDir):
                DeleteFiles(TestCasesDir)
            else:
                print "This file path not exist!"
                CountineOrExit()

        if a == "4":
            CopyFoldertoFolder()

        if a == "5":
            TestCasesDir = raw_input ("Please Input your file Path: ")
            CopyFiletoFolder(TestCasesDir)

        if a == "6":
            MoveFoldertoFolder()

        if a == "7":
            Path  = raw_input ("Please input the folder path with txt files:")
            Content = raw_input ("What content you want to find on txt file?")
            if os.path.exists(Path):
                FindContentOnTxt(Path,Content)
            else:
                print Path + " not exists!"
                CountineOrExit()
                
        if a == "8":
            Path  = raw_input ("Please input your folder path:")
            File = raw_input ("What file you want to find on this folder?")
            if os.path.exists(Path):
                FindFilesonDirs(Path,File)
            else:
                print Path + " not exists!"
                CountineOrExit()


        if a == "9":
            Dir = raw_input ("Input your folder path(if on disk should type like this -> E:\ ):")
            Foldername = raw_input ("Input your folder name: ")
            ReplaceFoldername = raw_input ("Input new folder name want to replace: ")

            if os.path.exists(os.path.join(Dir,Foldername)):
                ReplaceFolder(Dir,Foldername,ReplaceFoldername)
            else:
                print os.path.join(Dir,Foldername) + " is not exists!"
                CountineOrExit()

        if a == "10":
            Dir = raw_input ("Input your folder path(if on disk should type like this -> E:\ ):")
            Filename = raw_input ("Input your file name: ")
            ReplaceFilename = raw_input ("Input new file name want to replace: ")

            if os.path.exists(os.path.join(Dir,Filename)):
                ReplaceFile(Dir,Filename,ReplaceFilename)
            else:
                print os.path.join(Dir,Filename) + " is not exists!"
                CountineOrExit()
        
        if a == "11":
            FolderDir = raw_input ("Please input folder: ")
            if os.path.exists(FolderDir):
                FindContent = raw_input("What word do you want find?")
                FindContent = FindContent.lower() #Convert the FindContent path to lower
                ReplaceContent = raw_input("What word do you want replace?")
                ReplaceFileNameWithSpecificName(FolderDir,FindContent,ReplaceContent)
            else:
                print "Target Folder path: " + FolderDir + " is not exists!"
                CountineOrExit()
    
    else:
        print "Bye~"
        exit(1)
      

def ReplaceContentOnDir(TestCasesDir,s,p):
    i = 0
    #Dir = os.listdir(TestCasesDir)
    """
    for myFile in Dir:
        TxtFile = os.path.join(TestCasesDir,myFile)
    """
    for root,dirnames,filenames in os.walk(TestCasesDir):
        for myFile in filenames:
            TxtFile = os.path.join(root,myFile)
            #print "root is:" + root  root is the path which your file in now
            if "txt" in myFile:
                i = i + 1
                #print "File Path is: " + TxtFile #Show the txt file path(Should open this)
                #print "File Name is: " + myFile #Show the txt file name
                #print "the full name of the file is:" + os.path.join(parent,myFile)
                
                print "================================ Start ================================"
                print "File on " + TxtFile   
                files = open (TxtFile,'r') #read mode
                content = files.read()
                #print content
                files.close()
                # OK
                
                if s in content:
                    print "Found word: " + s + " in File " + myFile
                
                    files = open (TxtFile,'w') # write mode
                    files.writelines(content.replace (s, p))
                    files.close()
                    print s + " has been replaced as " + p + " Success!"
                
                    #f = open (TxtFile,'r')
                    #content = f.read()
                    #f.close()
            
                
                else:
                    print s + " Not found on File!"
            
            
                    
                files.close()
                print "================================ Finish ==============================="
                print "                                                                       "

    if i == 0:
        print "There is no txt files under folder " + TestCasesDir
                
    CountineOrExit()



def DeleteFolders(TestCasesDir):
    print "Deleteing folder " + TestCasesDir + " now..."
    shutil.rmtree(TestCasesDir)
    if not os.path.exists(TestCasesDir):
        print "The contents of folder: " + TestCasesDir + " have been deleted succeeded!"
    else:
        print "The contents of folder: " + TestCasesDir + " have been deleted failed!"        
    CountineOrExit()

def DeleteFiles(TestCasesDir):
    os.remove(TestCasesDir)
    if not os.path.exists(TestCasesDir):
        print "The file: " + TestCasesDir + " have been deleted succeeded!"
    else:
        print "The file: " + TestCasesDir + " have been deleted failed!"
    CountineOrExit()
        

def CopyFoldertoFolder():
    sourceCustomed = raw_input ("please input sourceFolder: ")
    TargetCustomed = raw_input ("please input TargetFolder: ")

    if (os.path.exists(sourceCustomed)):
        if os.path.isfile(sourceCustomed):
            print "This is a file NOT a folder, if wanna copy a file please back to menu to choose again!"
            CountineOrExit()
        else:
            if not os.path.exists(TargetCustomed):
                os.makedirs(TargetCustomed)
            else:
                Type = sourceCustomed.split("\\")[-1]
                TargetCustomed = os.path.join(TargetCustomed,Type)
                if os.path.exists(TargetCustomed):
                    while(1):
                        IsConver = raw_input ("There is a same folder on target folder , would you like to cover? (Y/N) ")
                        if IsConver.lower() == 'y':
                            break
                        elif IsConver.lower() == 'n':
                            CountineOrExit()
                         
    else :
        print ("sourceFolder: {0} is NOT Exist!" .format(sourceCustomed))
        CountineOrExit()

    #if (os.path.isdir(TargetCustomed)):
    print ("SourceFolder is : {0} " .format(sourceCustomed))
    print time.strftime("Start Copy Time :%Y-%m-%d %X",time.localtime())
    copyFiles(sourceCustomed,TargetCustomed)
    print "Copy Success to folder " + TargetCustomed
    print time.strftime("End Copy Time :%Y-%m-%d %X",time.localtime())
    print ("============================================")
        
    #else :
        #print ("{0} is NOT Exist!" .format(TargetCustomed))

    CountineOrExit()

def CopyFiletoFolder(TestCasesDir):
    sourceFile = TestCasesDir
    TargetFolder = raw_input ("Please input Target Folder:")
    pathname,filename = os.path.split (sourceFile)

    
    if (os.path.exists(sourceFile)):
        if os.path.isdir(sourceFile):
            print "This is a folder NOT a file, if wanna copy a file please back to menu to choose again!"
            CountineOrExit()
        else:
            if (not os.path.exists(TargetFolder)):
                os.makedirs(TargetFolder)

            print time.strftime("Start Copy Time :%Y-%m-%d %X",time.localtime())
            shutil.copy (sourceFile,TargetFolder) #Copy File to Folder method
            print ("Copy File Success!")
            print time.strftime("End Copy Time :%Y-%m-%d %X",time.localtime())
            print ("============================================")
    else:
        print ("You File {0} is NOT Exist!" .format(sourceFile))
        
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
        shutil.move (sourceFolder,targetFolder)
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
            #print "root is:" + root  root is the path which your file in now
            if 'txt' in myFile:
                j = j + 1
                #print TxtFile
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
            #else: #means not found
                #print ""                
    if k == 0:
        print "File: " + File + " didn't found on " + Path

    CountineOrExit()
            
def ReplaceFolder(Dir,Foldername,ReplaceFoldername):
    os.rename (os.path.join(Dir,Foldername),os.path.join(Dir,ReplaceFoldername))       
    if os.path.join(os.path.join(Dir,ReplaceFoldername)):
        print "Rename succeed!"
    else:
        print os.path.join(Dir,ReplaceFoldername) + " rename failed!"
    CountineOrExit()

def ReplaceFile(Dir,Filename,ReplaceFilename):
    os.rename (os.path.join(Dir,Filename),os.path.join(Dir,ReplaceFilename))       
    if os.path.join(os.path.join(Dir,ReplaceFilename)):
        print "Rename succeed!"
    else:
        print os.path.join(Dir,ReplaceFilename) + " rename failed!"
    CountineOrExit()

def ReplaceFileNameWithSpecificName(FolderDir,FindContent,ReplaceContent):
    w = 0
    for root,dirs,filenames in os.walk(FolderDir):
        for myFile in filenames:
            myFile = myFile.lower() #Convert the root path to lower
            #if 'xml' in myFile:
                #print myFile            
            if FindContent in myFile:
                w = w + 1
                OldNameFile = os.path.join(root,myFile)
                myFile = myFile.replace (FindContent,ReplaceContent)
                NewNameFile = os.path.join(root,myFile)
                os.rename (OldNameFile,NewNameFile) #rename function
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

    

