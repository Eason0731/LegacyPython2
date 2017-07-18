import os

def MainFunction():
    TestCasesDir = raw_input ("Please Input your folder Path: ")
    s = raw_input ("Please Input what words you want to find: ")
    #s = "RP="
    #p = raw_input ("Please Input what words you want to replace: ")
    #TestCasesDir = "C:\\Users\\t_zhanj\\Desktop\\Cases"
    if os.path.exists(TestCasesDir):
        FindModels(TestCasesDir,s,p)
    else:
        print "This folder not exist!"
        CountineOrExit()

def FindModels(TestCasesDir,s,p):
    Dir = os.listdir(TestCasesDir)       
    for myFile in Dir:
        TxtFile = os.path.join(TestCasesDir,myFile)
       
        if "txt" in myFile:
            #print "File Path is: " + TxtFile #Show the txt file path(Should open this)
            #print "File Name is: " + myFile #Show the txt file name
            print "================================ Start ================================"
            print myFile+ " is reading....."   
            files = open (TxtFile,'r') #read mode
            content = files.read()
            files.close()
            
            if s in content:
                print "Found word: " + s +" in File " + myFile
                
                
                
                #f = open (TxtFile,'r')
                #content = f.read()
                #f.close()
                #print content
                
            else:
                print s + " Not found on File!"
            #f.close()
            print "================================ Finish ==============================="
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

    

