import os

rootdir = r'C:\Users\Administrator\Desktop\Demo'

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:        
        if "txt" in filename:
            #print "parent is:" + parent
            #print "filename is:" + filename
            print "the full name of the file is:" + os.path.join(parent,filename)
            

