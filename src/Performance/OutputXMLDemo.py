#-*- coding:utf-8 -*-  

from xml.dom.minidom import parse
 
xmldoc = parse("E:\Test\FUS_POLE_FinishForm-19429\FUS_POLE_FinishForm-19429_build2.1.4259_20161209T172352.xml")
#Use method parse to read xml file (利用parse方法打开xml文件)

print xmldoc.toxml() #Use method toxml to output all the content of xml file(利用toxml()方法输出xml文件内所有内容)

XMLcontent = xmldoc.toxml()

if '<Fail/>' in XMLcontent: #Judge the specific content on file (判断指定内容是不是在xml内容中存在)
    print "Found!"
else:
    print "Not Found!"

