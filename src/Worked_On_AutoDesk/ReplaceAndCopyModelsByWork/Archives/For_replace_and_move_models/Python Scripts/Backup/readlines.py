import os

def Methods():

    f = open ("C:\\Users\\t_zhanj\\Desktop\\Cases\\FUS-27016_Joint_XYOffsetBasic.txt")  
    lines = f.read()

    if "NuCommands.CloseDocumentCmd" in lines:
        lines.replace("NuCommands.CloseDocumentCmd","Close!")
        print "Replace Success!"
        f.write(lines)
    else:
        print "Not Found"

    f.close()
   


if __name__=='__main__':
    Methods()   

