# -*- coding: utf-8 -*-
import os
import re
import shutil
import time
import sys

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
                Dir = raw_input ("Please input the folder path: ")
                if os.path.exists(Dir):
                    ReplaceContentOnDir(Dir)
                elif not Dir.strip():
                    EmptyOrNot()
                else:
                    ExistOrNot(Dir)
                                  
            if int(a) == 2:
                print "===========Delete file or folder============"
                Dir = raw_input ("Please input the folder or file path: ")
                if os.path.exists(Dir):
                    DeleteMethod(Dir)
                elif not Dir.strip():
                    EmptyOrNot()
                else:
                    ExistOrNot(Dir)

            if int(a) == 3:
                print "===========Copy file or folder============="
                Source = raw_input ("Please input the folder or file path: ")
                if os.path.exists(Source):
                    CopyMethod(Source)
                elif not Source.strip():
                    EmptyOrNot()
                else :
                    ExistOrNot(Source)
            
            if int(a) == 4:
                print "===========Move file or folder============="
                Source = raw_input ("Please input the source folder or file path: ")
                if os.path.exists(Source):
                    MoveMethod(Source)
                elif not Source.strip():
                    EmptyOrNot()
                else:
                    ExistOrNot(Source)
                    
            if int(a) == 5:
                print "=========Find contents on txt files========"
                Dir  = raw_input ("Please input the folder path: ")
                if os.path.exists(Dir):   
                    FindOnTxtMethod(Dir)
                elif not Dir.strip():
                    EmptyOrNot()
                else:
                    ExistOrNot(Dir)
                
            if int(a) == 6:
                print "=======Find files or folder on folder======="
                Dir  = raw_input ("Please input the folder path: ")
                if os.path.exists(Dir):
                    FindOnDirsMethod(Dir)
                elif not Dir.strip():
                    EmptyOrNot()
                else:
                    ExistOrNot(Dir)

            if int(a) == 7:
                print "===========Rename file or folder==========="
                Source = raw_input ("Please input the folder or file path: ")
                if os.path.exists(Source):          
                    ReplaceNameMethod(Source)
                elif not Source.strip():
                    EmptyOrNot()
                else:
                    ExistOrNot(Source)

            if int(a) == 8:
                print "=======Rename file with specificname======"
                Dir = raw_input ("Please input the folder path: ")
                if os.path.exists(Dir):
                    RenameWithSpecificNameMethod(Dir)
                elif not Dir.strip():
                    EmptyOrNot()
                else:
                   ExistOrNot(Dir)
    
        else:
            print "Bye~"
            exit(1)

    else:
        print "Bye~"
        exit(1)
      
def ReplaceContentOnDir(Dir):
    Original = raw_input("Please input what word you want to find: ")
    Replace = raw_input("Please input what word you want to replace: ")
    t = 0
    c = 0
    print "================================ Start ================================"
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    for root,diTargets,filenames in os.walk(Dir):
        for myFile in filenames:
            TxtFile = os.path.join(root,myFile)
            if "txt" in myFile:
                t = t + 1  
                files = open (TxtFile,'r') 
                content = files.read()
                files.close()         
                if Original in content:
                    c+=1         
                    files = open (TxtFile,'w') 
                    files.writelines(content.replace (Original, Replace))
                    files.close()
                    print Original + " has been replaced as " + Replace + " on file "+ TxtFile +" succeeded!"
                    print "   "
                files.close()
    if c == 0 and t != 0:
        print Original + " didn't found on " + Dir
    if c == 0 and t == 0:
        print "There is no txt files under folder " + Dir
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="     
    CountineOrExit()

def DeleteMethod(Dir):
    print "================================ Start ================================"
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    print "Deleteing " + Dir + " now..."
    if os.path.isfile(Dir):
        os.remove(Dir)
    elif os.path.isdir(Dir):
        shutil.rmtree(Dir)  
    if not os.path.exists(Dir):
        print  Dir + " has been deleted succeeded!"
    else:
        print  Dir + " has been deleted failed!"
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="    
    CountineOrExit()
        
def CopyMethod(Source):
    Target = raw_input ("Please input the target folder path: ")
    if not os.path.exists(Target):
        os.makedirs(Target)          
    Type = Source.split("\\")[-1]
    Target = os.path.join(Target,Type)
    if os.path.exists(Target):
        OverwriteOrNot(Source,Target,sys._getframe().f_code.co_name)
    print "================================ Start ================================"
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    if os.path.isdir(Source):
        if not os.listdir(Source):
            shutil.copytree(Source,Target)
        else:
            copyFiles(Source,Target)
    elif os.path.isfile(Source):
        shutil.copy (Source,Target) 
    print Source + " has copied succeeded to folder " + Target
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

def MoveMethod(Source):
    Target = raw_input ("Please input the target folder path: ")
    if not os.path.exists(Target):
        os.makedirs(Target)
    Type = Source.split("\\")[-1]
    Target = os.path.join(Target,Type)
    if os.path.exists(Target):
        OverwriteOrNot(Source,Target,sys._getframe().f_code.co_name)
    print "================================ Start ================================"
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    if os.path.isfile(Source):
        if os.path.exists(Target):
            os.remove(Target)
        shutil.move (Source,Target)

    elif os.path.isdir(Source):
        if not os.listdir(Source):
            shutil.copytree(Source,Target)
        else:
            copyFiles(Source,Target)                    
        shutil.rmtree(Source)
    if os.path.exists(Target):
        print Source + " has been moved to " + Target + " succeeded!"
    else:
        print Source + " has been moved failed!"
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="
    CountineOrExit()

def FindOnTxtMethod(Dir):
    Content = raw_input ("What content you want to find on txt file? ")
    t = 0
    c = 0
    print "================================ Start ==============================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    for root,diTargets,filenames in os.walk(Dir):
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
        print Content + " didn't found on " + Dir              
    if c == 0 and t == 0:
        print "There is no txt files under folder " + Dir
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="
    CountineOrExit()
                
def FindOnDirsMethod(Dir):
    File = raw_input ("What file or folder you want to find on this folder? ")
    k = 0
    print "================================ Start ==============================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    for root,diTargets,filenames in os.walk(Dir):
        if os.path.isfile(os.path.join(Dir,File)):
            for myFile in filenames:
                if File.lower() in myFile.lower():
                    k = k + 1
                    print "File: " + File + " has found on " + root
                    print "  "
        elif os.path.isdir(os.path.join(Dir,File)):
            for myFolder in diTargets:
                if File.lower() in myFolder.lower():
                    k = k + 1
                    print "Folder: " + File + " has found on " + root
                    print "  "   
    if k == 0:
        print "File: " + File + " didn't found on " + Dir
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="
    CountineOrExit()
            
def ReplaceNameMethod(Source):
    Target = raw_input ("Please input new name want to replace: ")
    Source = os.path.abspath(Source)
    Target = os.path.join(os.path.split(Source)[0],Target)   
    print "================================ Start ==============================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    if os.path.exists(Target):
        print Source + " has already exists, cannot be renamed!"
    else:
        os.rename (Source,Target)
        print Source + " has been renamed as " + Target +" succeeded!"
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "================================ Finish ==============================="
    CountineOrExit()

def RenameWithSpecificNameMethod(Dir):
    FindContent = raw_input("What word do you want find? ")
    FindContent = FindContent.lower()
    ReplaceContent = raw_input("What word do you want replace? ")
    w = 0
    print "================================ Start ==============================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    for root,dirs,filenames in os.walk(Dir):
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
        print "Didn't found file named with " + FindContent + " under folder " + Dir
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
            
def EmptyOrNot():
    print "Please do not input the empty infos"
    CountineOrExit()

def ExistOrNot(Dir):
    print "{0} is NOT Exist!" .format(Dir)
    CountineOrExit()

def OverwriteOrNot(Source,Target,Fun):
    while(1):
        if os.path.isfile(Target):
            IsConver = raw_input ("There is a same file on target file , would you still want to move? (Y/N) ")
        elif os.path.isdir(Target):
            IsConver = raw_input ("There is a same folder on target folder , would you still want to move? (Y/N) ")              
        if IsConver.lower() == 'y':
            if 'Copy' in Fun:
                if os.path.isdir(Target):
                    if not os.listdir(Source) and not os.listdir(Target):
                        shutil.rmtree(Target) 
            break
        elif IsConver.lower() == 'n':
            CountineOrExit()
    
if __name__=='__main__':
    MainFunction()

    

