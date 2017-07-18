''''' 
Created on Sep 18, 2014 
 
@author: liu.chunming 
'''  
#There is a text.txt file which contains "AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDD"  
  
text_file=r"C:\\Users\\t_zhanj\\Desktop\\Demo\\test.txt"  
#open()  
f=open(text_file,"r")
f1=f.readline()
search = 'D'    
start = 0

while(1):     
    index = f1.find(search, start)     
    # if search string not found, find() returns -1     
    # search is complete, break out of the while loop     
    if index == -1:     
        break
    print f1.split('/')[-2]
    print( "%s found at index %d"  % (search, index) )     
    # move to next possible start position
    break
  

#print text_to_number  
#print text_to_all  
