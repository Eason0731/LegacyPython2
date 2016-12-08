'''
Created on Dec 8, 2016

@author: t_zhanj
'''
import os
import time
import shutil

def DeleteFailedXmlFiles():
    XmlDir = r'E:\Test'
    for root,dirs,filenames in os.walk(XmlDir):
        for myFile in filenames:
            if 'xml' in myFile:
                print "Found txt file: " + os.path.join(root,myFile)
                xmlfiles = os.path.join(root,myFile)
                f = open (xmlfiles)
                content = f.readlines() #The content will print line by line
                #print content
                
                for eachline in content:
                    #print eachline
                    if '<skills>' in eachline:
                        myXMLfiles = os.path.join(root,myFile) 
                        f.close() #Should close file then delete
                        print "Failed xml found on " + myXMLfiles
                        '''
                        os.remove(myXMLfiles)
                        if not os.path.exists(myXMLfiles):
                            print "Delete file " + myXMLfiles + " Successfully"
                        '''  
                print "==================================="
                f.close()

if __name__ == '__main__':
    DeleteFailedXmlFiles()