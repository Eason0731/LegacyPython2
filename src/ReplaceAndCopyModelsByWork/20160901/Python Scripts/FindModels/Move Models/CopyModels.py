import re
import os
import time
import shutil

def MainFunction():
    #TestCasesDir = raw_input ("Please Input your folder Path: ")
    s = raw_input ("Please Input what words you want to find: ")
    #s = s.upper()
    #p = raw_input ("Please Input what words you want to replace: ")
    TestCasesDir = "C:\\Users\\t_zhanj\\Desktop\\Demo"
    print s
    if os.path.exists(TestCasesDir):
        FindMyModels(TestCasesDir,s)
    else:
        print "This folder not exist!"
        CountineOrExit()

def FindMyModels(TestCasesDir,s):
    Dir = os.listdir(TestCasesDir)       
    for myFile in Dir:
        TxtFile = os.path.join(TestCasesDir,myFile)
        
        if "txt" in myFile:
            i=0
            print myFile+ " is reading....."   
            files = open (TxtFile,'r') #read mode

            AllLines = files.readlines()
            #print AllLines,type(AllLines)

            # Use Readlines to read all content on txt file and for cycle to convert to str type 
            for eachline in AllLines:
                eachline = eachline.replace('"','')
                #print eachline
                match = re.search(r'^([a-zA-Z]:|//[a-zA-Z0-9_.$ -]+/[a-z0-9_.$ -]+)?((?:/|^)(?:[^//:*?"<>|\r\n]+/)+)', eachline)
                extname = re.findall(r'\[^.\\/:*?"<>|\r\n]+$', eachline)
                filename = re.findall(r'[^\\/:*?"<>|\r\n]+$' , eachline)
        
                if s in eachline:
                    if match:
                        filepath = match.group(2)
                        print "Match"
                    else:  
                        filepath = ""
                        print "Not Match"

                    search = 'RP'
                    start = 0
        
                    index = eachline.find(search, start)

                    index +=3 
                    print index
                    
                    print "file path is " +filepath[index:]

                    #print "file name is " + filename

                    #i+=1

                    
        """
            if i == 0:
                print s + " didn't found on " + myFile
            elif i == 1:
                print s + " has been found for " + str(i) + " time on " + myFile
            else:
                print s + " have been found for " + str(i) + " times on " + myFile
           """         
                
                
                
            
                
        files.close()
            


if __name__=='__main__':
    MainFunction()
