import os
import re
import shutil
import time

def MainFunction():
    
    TestCasesDir = raw_input ("Please Input your folder Path: ") 
    s = raw_input("Please Input what words you want to find: ")
    p = raw_input("Please Input what words you want to replace: ")

    if os.path.exists(TestCasesDir):
        ReplaceContentOnDir(TestCasesDir,s,p)
    else:
        print "This folder not exist!"
        CountineOrExit()
    

def ReplaceContentOnDir(TestCasesDir,s,p):
    #Dir = os.listdir(TestCasesDir)
    """
    for myFile in Dir:
        TxtFile = os.path.join(TestCasesDir,myFile)
    """
    for root,dirnames,filenames in os.walk(TestCasesDir):
        for myFile in filenames:
            TxtFile = os.path.join(root,myFile)
                if "txt" in myFile:       
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
                else:
                    print s + " Not found on File!"
                    
                files.close()
                print "================================ Finish ==============================="
                print "                                                                       "
                
                
    CountineOrExit()
        

def CountineOrExit():
    IsExit = raw_input ("Countine(Y) or Exit(N)? ")
    while(1):
        if IsExit.upper() == "Y":
            MainFunction()
        elif IsExit.upper() == "N":
            exit(0)
        else:
            print "You have inputed the illegal character,try again!"
            CountineOrExit()
            break
            
            
            
if __name__=='__main__':
    MainFunction()

    

