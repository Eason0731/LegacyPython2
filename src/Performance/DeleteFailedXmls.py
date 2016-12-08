'''
Created on Dec 8, 2016

@author: t_zhanj
'''
import os
import time
import shutil

def DeleteFailedXmlFiles():
    XmlDir = r'C:\Users\t_zhanj\Desktop\123'
    for root,dirs,filenames in os.walk(XmlDir):
        for myFile in filenames:
            if 'xml' in myFile:
                print "Found xml file: " + os.path.join(root,myFile)
                xmlfiles = os.path.join(root,myFile)
                f = open (xmlfiles, 'r')
                content = f.read()
                #print content
                
                for eachline in content:
                    if '< F a i l / >' in eachline:
                        print "Found Failed xml file: " + os.path.join(root,myFile) 
                             
                print "==================================="
                f.close()

if __name__ == '__main__':
    DeleteFailedXmlFiles()