# -*- coding: utf-8 -*-
import os
import re
import shutil
import time
import sys
import ViewPCInfos

def MainFunction():
    Choose = raw_input ("""
=============Welcome to File Operation=============
1. Replace content on txt files
2. Delete file or folder
3. Copy file or folder
4. Move file or folder
5. Find contents on txt files
6. Find files or folder on folder
7. Rename file or folder
8. Rename file with specificname
9. Calculate the file or folder size
10. View PC infos

=========  """+ GetDate() +"""  =========

Press AnyKey to Exit
        
Please choose : """)
    Fun = sys._getframe().f_code.co_name
    if Choose == '1':
        print "===========Replace content on txt files============"
        Dir = raw_input ("Please input the folder path: ")
        if os.path.exists(Dir):
            if not '\\' in Dir:
                FormatJudge(Dir,Fun)
            ReplaceOnTxt(Dir)
        elif not Dir.strip():
            EmptyOrNot()
        else:
            ExistOrNot(Dir)
                                  
    elif Choose == '2':
        print "===============Delete file or folder==============="
        Dir = raw_input ("Please input the folder or file path: ")
        if os.path.exists(Dir):
            if not '\\' in Dir:
                FormatJudge(Dir,Fun)
            Delete(Dir)
        elif not Dir.strip():
            EmptyOrNot()
        else:
            ExistOrNot(Dir)

    elif Choose == '3':
        print "===============Copy file or folder================="
        Source = raw_input ("Please input the folder or file path: ")
        if os.path.exists(Source):
            if not '\\' in Source:
                FormatJudge(Source,Fun)
            Copy(Source)
        elif not Source.strip():
            EmptyOrNot()
        else:
            ExistOrNot(Source)
            
    elif Choose == '4':
        print "===============Move file or folder================="
        Source = raw_input ("Please input the source folder or file path: ")
        if os.path.exists(Source):
            if not '\\' in Source:
                FormatJudge(Source,Fun)
            Move(Source)
        elif not Source.strip():
            EmptyOrNot()
        else:
            ExistOrNot(Source)
                    
    elif Choose == '5':
        print "=============Find contents on txt files============"
        Dir  = raw_input ("Please input the folder path: ")
        if os.path.exists(Dir):
            if not '\\' in Dir:
                FormatJudge(Dir,Fun)
            FindOnTxt(Dir)
        elif not Dir.strip():
            EmptyOrNot()
        else:
            ExistOrNot(Dir)
                
    elif Choose == '6':
        print "===========Find files or folder on folder=========="
        Dir  = raw_input ("Please input the folder path: ")
        if os.path.exists(Dir):
            if not '\\' in Dir:
                FormatJudge(Dir,Fun)
            FindOnDirs(Dir)
        elif not Dir.strip():
            EmptyOrNot()
        else:
            ExistOrNot(Dir)

    elif Choose == '7':
        print "===============Rename file or folder==============="  
        Source = raw_input ("Please input the folder or file path: ")
        if os.path.exists(Source):
            if not '\\' in Source:
                FormatJudge(Source,Fun)
            Rename(Source)
        elif not Source.strip():
            EmptyOrNot()
        else:
            ExistOrNot(Source)

    elif Choose == '8':
        print "============Rename file with specificname=========="
        Dir = raw_input ("Please input the folder or file path: ")
        if os.path.exists(Dir):
            if not '\\' in Dir:
                FormatJudge(Dir,Fun)
            BatchRename(Dir)
        elif not Dir.strip():
            EmptyOrNot()
        else:
            ExistOrNot(Dir)
            
    elif Choose == '9':
        print "========Calculate the file or folder size=========="  
        Source = raw_input ("Please input the folder or file path: ")
        if os.path.exists(Source):
            if not '\\' in Source:
                FormatJudge(Source,Fun)
            GetSize(Source)
        elif not Source.strip():
            EmptyOrNot()
        else:
            ExistOrNot(Source)
        
    elif Choose == '10':
        ViewPCInfos.ViewPCInfos()

    else:
        exit(1)
      
def ReplaceOnTxt(Dir):
    if os.path.isdir(Dir):
        if 'txt' in str(os.listdir(Dir)):
            c = 0
            while(True):
                Original = raw_input("Please input what content you want to find: ")
                if not Original.strip():
                    print "Cannot input empty search content, please input again!"
                else:
                    break
            while(True):
                Replace = raw_input("Please input what content you want to replace: ")
                if not Replace.strip():
                    print "Cannot input empty replace content, please input again!"
                else:
                    break
            print "=================== Start ========================="
            print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
            for root,dirs,filenames in os.walk(Dir):
                for myFile in filenames:
                    TxtFile = os.path.join(root,myFile)
                    files = open (TxtFile,'r') 
                    content = files.read()
                    files.close()
                    Original = Original.lower()
                    content = content.lower()
                    if Original in content:
                        c+=1         
                        files = open (TxtFile,'w') 
                        files.writelines(content.replace (Original, Replace))
                        files.close()
                        print Original + " has been replaced as " + Replace + " on file "+ TxtFile +" successfully!"
                        print "   "
                    files.close()
            if c == 0:
                print Original + " didn't found on " + Dir       
            print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
            print "=================== Finish ========================"
        else:
            print "There is no txt files under folder " + Dir
    else:
        print Dir + " is a file path , please input a folder path"
    CountineOrExit()

def Delete(Dir):
    print "=================== Start ========================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    if os.path.isfile(Dir):
        os.remove(Dir)
    elif os.path.isdir(Dir):
        shutil.rmtree(Dir)  
    if not os.path.exists(Dir):
        print  Dir + " has been deleted successfully!"
    else:
        print  Dir + " has been deleted failed!"
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "=================== Finish ========================"
    CountineOrExit()
        
def Copy(Source):
    while(True):
        Target = raw_input ("Please input the target folder path: ")
        if not '\\' in Target:
            FormatJudge(Target,sys._getframe().f_code.co_name)
        else:
            break
    TargetFolderEmptyOrNot(Source,Target,sys._getframe().f_code.co_name)
    Disk = '\\'.join(Target.split("\\")[:1])
    if os.path.exists(Disk):
        if not os.path.exists(Target):
            os.makedirs(Target)
    else:
        print Disk + " is not exists on this PC, cannot copy"
        CountineOrExit()
    Type = Source.split("\\")[-1]
    Target = os.path.join(Target,Type)
    if os.path.exists(Target):
        if Source == Target:    
            print "Cannot copy same file or folder to origin path"
            CountineOrExit()
        else:
            OverwriteOrNot(Source,Target)
    print "=================== Start ========================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    if os.path.isdir(Source):
        if not os.listdir(Source):
            shutil.copytree(Source,Target)
        else:
            copyFiles(Source,Target)
    elif os.path.isfile(Source):
        shutil.copy (Source,Target)
    print Source + " has copied to " + '\\'.join(Target.split("\\")[:-1]) + " successfully!"
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "=================== Finish ========================"
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

def Move(Source):
    while(True):
        Target = raw_input ("Please input the target folder path: ")
        if not '\\' in Target:
            FormatJudge(Target,sys._getframe().f_code.co_name)
        else:
            break
    TargetFolderEmptyOrNot(Source,Target,sys._getframe().f_code.co_name)
    Disk = '\\'.join(Target.split("\\")[:1])
    Type = Source.split("\\")[-1]
    if os.path.exists(Disk):
        if not os.path.exists(Target):
            os.makedirs(Target)
    else:
        print Disk + " is not exists on this PC, cannot move"
        CountineOrExit()
    Target = os.path.join(Target,Type)
    if os.path.exists(Target):
        if Source == Target:
            print "Cannot move file or folder to origin path"
            CountineOrExit()
        else:
            OverwriteOrNot(Source,Target)
    print "=================== Start ========================="
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
        print Source + " has been moved from " + "\\".join(Source.split("\\")[0:-1]) + " to " + "\\".join(Target.split("\\")[0:-1]) + " successfully!"
    else:
        print Source + " has been moved failed!"
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "=================== Finish ========================"
    CountineOrExit()

def FindOnTxt(Dir):
    if os.path.isdir(Dir):
        if 'txt' in str(os.listdir(Dir)):
            c = 0
            while(True):
                Content = raw_input ("What content you want to find on txt file? ")
                if not Content.strip():
                    print "Cannot input empty search content, please input again!"
                else:
                    break
            print "=================== Start ========================="
            print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
            for root,dirs,filenames in os.walk(Dir):
                for myFile in filenames:
                    i = 0
                    TxtFile = os.path.join(root,myFile)
                    f = open (TxtFile, 'r')
                    Filecontent = f.readlines()              
                    for eachline in Filecontent:
                        if Content.lower() in eachline.lower():
                            i += 1
                            c += 1
                    f.close()
                    if i > 0:
                        print Content + " found on " + TxtFile + " for " + str(i) + " times"
            if c ==0 and i == 0:
                print Content + " didn't found on " + Dir
            print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
            print "=================== Finish ========================"
        else:
            print "There is no txt files under folder " + Dir
    else:
        print Dir + " is a file path , please input a folder path"   
    CountineOrExit()
                
def FindOnDirs(Dir):
    if os.path.isdir(Dir):
        while(True):
            File = raw_input ("What file or folder you want to find on this folder? ")
            if not File.strip():
                print "Cannot input empty file or folder name, please input again!"
            else:
                break 
        k = 0
        print "=================== Start ========================="
        print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
        for root,dirs,filenames in os.walk(Dir):
            for myFile in filenames:
                if File.lower() in myFile.lower():
                    k = k + 1
                    print "File: " + File + " has found on " + os.path.join(root,myFile)
                    print "  "

            for myFolder in dirs:
                if File.lower() in myFolder.lower():
                    k = k + 1
                    print "Folder: " + File + " has found on " + os.path.join(root,myFolder)
                    print "  "   
        if k == 0:
            print File + " didn't found on " + Dir
        print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
        print "=================== Finish ========================"
    else:
        print Dir + " is a file path , please input a folder path"
    CountineOrExit()
            
def Rename(Source):
    while(True):
        Target = raw_input ("Please input new name want to replace: ")
        if not Target.strip():
            print "Cannot input empty replace content, please input again!"
        else:
            break
    Source = os.path.abspath(Source)
    Target = os.path.join(os.path.split(Source)[0],Target)
    print "=================== Start ========================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    if os.path.exists(Target):
        print Source + " has already exists, cannot be renamed!"
    else:
        os.rename (Source,Target)
        print Source + " has been renamed as " + Target +" successfully!"
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "=================== Finish ========================"
    CountineOrExit()

def BatchRename(Dir):
    while(True):
        FindContent = raw_input("What content do you want find? ")
        if not FindContent.strip():
            print "Cannot input empty search content, please input again!"
        else:
            FindContent = FindContent.lower()
            break
    while(True):
        ReplaceContent = raw_input("What content do you want replace? ")
        if not ReplaceContent.strip():
            print "Cannot input empty replace content, please input again!"
        else:
            break
    w = 0
    print "=================== Start ========================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    if os.path.isdir(Dir):
        for root,dirs,filenames in os.walk(Dir):
            for myFile in filenames:
                myFile = myFile.lower()  
                if FindContent in myFile:
                    w = w + 1
                    OldNameFile = os.path.join(root,myFile)
                    myFile = myFile.replace(FindContent,ReplaceContent)
                    NewNameFile = os.path.join(root,myFile)
                    os.rename (OldNameFile,NewNameFile)
                    if os.path.exists(NewNameFile):
                        print OldNameFile +" has been replaced as " + NewNameFile + " successfully!"
                        print "   "
        if w == 0:
            print "Didn't found file named with " + FindContent + " under folder " + Dir
    else:
        myFile = Dir.split('\\')[-1]
        myFile = myFile.lower()
        if FindContent in myFile:
            myFile = myFile.replace(FindContent,ReplaceContent)
            Path = '\\'.join(Dir.split('\\')[0:-1])
            NewNameFile = os.path.join(Path,myFile)
            os.rename (Dir,NewNameFile)
            if os.path.exists(NewNameFile):
                print Dir +" has been replaced as " + NewNameFile + " successfully!"
        else:
            print "Didn't found file named with " + FindContent + " on file " + Dir
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "=================== Finish ========================"
    CountineOrExit()              

def GetSize(Source):
    print "=================== Start ========================="
    print time.strftime("Start Time :%Y-%m-%d %X",time.localtime())
    size = 0L
    if os.path.isfile(Source):
        size = os.path.getsize(Source)
    elif os.path.isdir(Source):
        for root, dirs, files in os.walk(Source):
            for names in files:
                myfiles = os.path.join(root,names)
                size += sum([os.path.getsize(myfiles)])
    print "The size of " + Source + " are %.2f" % (size/1024.00/1024.00), "MB"
    print time.strftime("End Time :%Y-%m-%d %X",time.localtime())
    print "=================== Finish ========================"
    CountineOrExit()

def CountineOrExit():
    IsExit = raw_input ("Countine(Y) or Exit(N)? ")
    while(1):
        if IsExit.upper() == 'Y':
            MainFunction()
        elif IsExit.upper() == 'N':
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
    
def OverwriteOrNot(Source,Target):
    while(1):
        if os.path.isfile(Target):
            IsConver = raw_input ("There is a same file on target file , would you still want to operate it? (Y/N) ")
        elif os.path.isdir(Target):
            IsConver = raw_input ("There is a same folder on target folder , would you still want to operate it? (Y/N) ")              
        if IsConver.lower() == 'y':
            if os.path.isdir(Target):
                if not os.listdir(Source) and not os.listdir(Target):
                    shutil.rmtree(Target) 
            break
        elif IsConver.lower() == 'n':
            CountineOrExit()
        
def FormatJudge(Source,Fun):
    print "The format of " + Source + " is incorrect! Should with '\\'"
    if 'Main' in Fun:
        CountineOrExit()

def TargetFolderEmptyOrNot(Source,Target,Fun):
     if not Target.strip():
         print "Do not input the empty infos. Please input again!"
         if 'Copy' in Fun:
             Copy(Source)
         elif 'Move' in Fun:
             Move(Source)
             
def GetDate():
    Date = time.strftime("%Y-%m-%d , %A", time.localtime())
    return "Today is " + Date

if __name__== '__main__':
    MainFunction()
