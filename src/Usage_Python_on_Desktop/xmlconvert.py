import xml.etree.ElementTree as ET
import sys
import re
import datetime

def getDuration(startTime, endTime):
    startTime = datetime.datetime.strptime(startTime,"%H:%M:%S")
    endTime = datetime.datetime.strptime(endTime,"%H:%M:%S")
    duration = endTime - startTime
    return duration
    
def load_xml_result_info(fileName):
    dic = {}
    root = ET.parse(fileName).getroot()
    
    dic['totalCase'] = root.get('TotalCases')
    dic['passedCase'] = root.get('PassedCases')
    dic['failedCase'] = root.get('FailedCases')
    startDate = root.get('Date')
    startTime = "{0} {1}".format(startDate, root.get('StartTime'))
    endTime = "{0} {1}".format(startDate, root.get('EndTime'))
    dic['startTime'] = startTime
    dic['endTime'] = endTime
    dic['duration'] = getDuration(root.get('StartTime'), root.get('EndTime'))
    return dic

def load_xml_result(fileName):
    dic = {}
    failedCases = []
    
    root = ET.parse(fileName).getroot()

    topFolders = root.findall('Folder')
    
    for topFolder in topFolders:
        topName = topFolder.get('Name')
        
        for testcase in topFolder.iter('Case'):
            caseName = testcase.get('Name')
            result = testcase.get('Passed')

            errormsg = '';
            if result.upper() != 'TRUE':
                errormsg = testcase.find('ErrorInformation').text
                failedCases.append(topName+'\\'+caseName)
            dic[caseName.replace(".txt", "")] = (result, errormsg, topName)
        
        all_folders = topFolder.findall('Folder')
        for folder in all_folders:
            folderName = folder.get('Name')
            
            for testcase in folder.iter('Case'):
                caseName = testcase.get('Name')
                result = testcase.get('Passed')

                errormsg = '';
                if result.upper() != 'TRUE':
                    errormsg = testcase.find('ErrorInformation').text
                    failedCases.append(topName+'\\'+folderName+'\\'+caseName)
                dic[caseName.replace(".txt", "")] = (result, errormsg, topName)

    return (dic, failedCases)

def load_all_xml_result(firstResult, *args):
    baseResult, failCases = load_xml_result(firstResult)
    
    for value in args:
        rerunResult, rerunFailCases = load_xml_result(value)
        for key in rerunResult.keys():
            if len(baseResult[key]) == 4 and baseResult[key][3].upper() == 'TRUE':
                continue
            baseResult[key] = (baseResult[key][0], baseResult[key][1], baseResult[key][2], rerunResult[key][0])
            
    return baseResult

def load_txt_result(filePath):
    dic = {}
    
    txtFile = open(filePath, 'r')
    lines = txtFile.readlines()
    
    pattern = re.compile(r'Case:\s+(?P<model>.*\.\S+)\s+Result:\s+(?P<result>.*)')
    
    model = ''
    errormsg = ''
    result = ''
    endflag = False
    for line in lines:
        #print line
        match = pattern.match(line)
        if match:
            if model != '':
                dic[model.split('\\')[-1]] = (result, errormsg, 'none')
                model = errormsg = result = ''
            
            model = match.group('model')
            result = match.group('result')
            
            if result.lower() == 'ok':
                result = 'True'
            else:
                errormsg = result
                result = 'False'
            
            endflag = True
        else:
            errormsg = errormsg + line
    
    # Add the last case log
    dic[model.split('\\')[-1]] = (result, errormsg)
    
    return dic
    

def convert_unit_result(caseDic):
    testsuite = ET.Element('testsuite')
    tree = ET.ElementTree(testsuite)
    for (k,v) in caseDic.items():
        caseElement = ET.SubElement(testsuite, 'testcase', {'name':k, 'classname':v[2], 'status':v[0]})
        #caseElement.text = ' '
        if v[0].upper() == 'FALSE':
            error = ET.SubElement(caseElement, 'failure')
            error.text = v[1]
    
    return tree
    
def merge_result(originalResult, newResult):
    oRoot = originalResult.getroot()
    nRoot = newResult.getroot()
    
    
def load_xml_project(fileName, failedList):
    tree = ET.parse(fileName)
    
    root = tree.getroot()
    for item in root.iter('Item'):
        scriptFile = item.get('ScriptFile')
        splits = scriptFile.split('/')
        caseName = splits[-1]
        if caseName.upper() in failedList:
            item.set('CheckStatus', '1')
    
    return tree

def save_xml_file(fileName, resultData):
    print('I am here')
    
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        buildnumber = sys.argv[1]
        
    (mydata, caseList) = load_xml_result(buildnumber+'.xml')
    
    unitresult = convert_unit_result(mydata)
    unitresult.write('unitresult.xml')
    
    #ntp = load_xml_project('test.ntp', caseList)
    #ntp.write('my.ntp')
    
    # Sample for parse txt file
    cases = load_txt_result(r'C:\Users\zhujin\Documents\360\SeleniumAutomationLog.txt')
    result = convert_unit_result(cases)
    result.write(r'C:\Users\zhujin\Documents\360\unitresult.xml')