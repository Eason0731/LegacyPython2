import os

def ReplaceContentOnDir(TestCasesDir,s,p):
    Dir = os.listdir(TestCasesDir)       
    for myFile in Dir:
        TxtFile = os.path.join(TestCasesDir,myFile)
        
        if "txt" in myFile: 
            #print "File Path is: " + TxtFile #Show the txt file path(Should open this)
            #print "File Name is: " + myFile #Show the txt file name
            print "============ Start ================"
            print myFile+ " is reading....."   
            f = open (TxtFile,'r+') #read/write mode
            content = f.read()
            
            #s = "Fusion/Test/Dataset"
            if s in content:
                length = len(s)
                contentlength = len(content)
                f.seek(contentlength - length)
                f.writelines(' '*length)
                f.seek(0)
                print "Found word: " + s +" in File " + myFile        
                f.writelines(content.replace(s, p))  #replace new content .replace("old","new")
                f.close()
                print "Replace success!"
                
            else:
                print s + " Not found on file!"
            f.close()
            print "============ Finish ================"
            #return
        

if __name__=='__main__':
    TestCasesDir = raw_input ("Please Input your folder Path: ")
    s = raw_input ("Please Input what words you want to find: ")
    p = raw_input ("Please Input what words you want to replace: ")  #TestCasesDir = "C:\\Users\\t_zhanj\\Desktop\\Cases"
    ReplaceContentOnDir(TestCasesDir,s,p)
    

