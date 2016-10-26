import os

def SearchFile(TestCasesDir):
    Dir = os.listdir(TestCasesDir)       
    for myFile in Dir:
        TxtFile = os.path.join(TestCasesDir,myFile)
        #print TxtFile
        #print myFile

        if "txt" in myFile:
            #print myFile
            
            print "File Path is: " + TxtFile #Show the txt file path(Should open this)
            print "File Name is: " + myFile #Show the txt file name
            print myFile+ " is reading....."   
            f = open (TxtFile,'r') #read mode
            content = f.read()
            f.close()
            #print content
            s = "enable"
            if s in content:
                print "Found word: " + s +" in File " + myFile
                
                f = open (TxtFile,'w') # write mode
                
                f.writelines(content.replace (s, "disable"))
                f.close()
                
                f = open (TxtFile,'r')
                content = f.read()
                f.close()
                print content
                
            else:
                print "Not found!"
            f.close()
            print "============ Finish ================"
            #return
        

if __name__=='__main__':
    TestCasesDir = "C:\\Users\\t_zhanj\\Desktop\\Cases"
    SearchFile(TestCasesDir)
    

