'''
Created on Dec 8, 2016

@author: t_zhanj
'''
import os
import time
import shutil
from xml.dom.minidom import parse

def DeleteFailedXmlFiles():
    XmlDir = r'E:\Performance Result\2.1.4259_Yosemite_performance'
    for root,dirs,filenames in os.walk(XmlDir):
        for myFile in filenames:
            if 'xml' in myFile:
                #print "Found xml file: " + os.path.join(root,myFile)            
                #f = open (xmlfiles)              
                #content = f.readlines() #The content will print line by line
                #print content
                
                xmlfiles = os.path.join(root,myFile)
                xmldoc = parse(xmlfiles)
                xmlContent = xmldoc.toxml()
                
                if '<Fail/>' in xmlContent:                   
                    os.remove(xmlfiles)
                    if not os.path.exists(xmlfiles):
                        print "Useless file " +xmlfiles + " has been deleted successfully!"
                        
                #f.close()

if __name__ == '__main__':
    DeleteFailedXmlFiles()