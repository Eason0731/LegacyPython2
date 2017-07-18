import os

File = r'D:\\PythonTest\\myFile.txt'

ff = open (File,'r')
abc = ff.readlines()
ff.close()

"""
ff = open (File,'r')
abc1 = ff.read()
ff.close()



print "============readlines========"
print abc
print type(abc)
print "============readlines========"


print "============read========"
print abc1
print type(abc1)
print "============read========"
"""

s = "RP"
s = s.lower()


i=0
for l in abc: # l saved as string ,Type of abc is list
    if s in l.lower(): # Change All the type to lower!
        i+=1
        
if i == 0:
    print s + " didn't found!"
elif i == 1:
    print s + " have found for " + str(i) + " time"
else:
    print s + " have found for " + str(i) + " times"
    
ff.close()

"""
str='akwdlkandwm,nam,wndajbddaklwnldhawlhdlahndwla'
dupstr=set()
for i in str:
	if i in str:
		dupstr.add(i)
print dupstr
"""
