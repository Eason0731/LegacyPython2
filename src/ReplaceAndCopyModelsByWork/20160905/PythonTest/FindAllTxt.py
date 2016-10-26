import string, os, sys
"""
TestDir = r'D:\\PythonTest'
#TestDir = os.listdir(TestDir)

items = os.listdir(TestDir)

for item in items:
    #TestFolderDir = os.path.join(TestDir,item)
    print item
"""
#TestCasesDir = r'C:\Users\t_zhanj\Desktop\Cases'
#Dir = os.listdir(TestCasesDir)

def abc(TestCasesDir):    
    for root, dirs, files in os.walk(TestCasesDir):
        for myFile in files:
            TxtFile = os.path.join(root, myFile)
            print myFile


if __name__ == '__main__':
    TestCasesDir = raw_input("Input folder: ")
    abc(TestCasesDir)
    
        
        
        
    
