# -*- coding: utf-8 -*-
'''
Created on Jun 3, 2016

@author: wangcat
'''

import os
from xml.dom.minidom import Document

BlackList = ['Archive',
             'Neutron\Test\APITest',
             'Neutron\Test\Sample',
             'NeuCAM\Test\IronLib-test']

officialProducts = ['Fusion',
                 'FusionDoc',
                 'NeuCAM',
                 'Animation',
                 'Simulation']

def inBlackList(testCasesDir):
    for blackName in BlackList:
        if(-1!= testCasesDir.find(blackName)):
            return True
    return False
    

def mergeTestDirOnList(rawTestDirList):   
    listTestDir = []
    tempDeleteList = []
    for rawTestDir in rawTestDirList:
        ignoreTestFolder = False
        for testDir in listTestDir:       
            # Ignore the new folder which already included in TestList
            if -1 != rawTestDir.find(testDir):
                ignoreTestFolder = True;                 
            # Remove the existed folder in TestList if the new folder already include it
            if -1 != testDir.find(rawTestDir) and testDir != rawTestDir:
                tempDeleteList.append(testDir) 
        if not ignoreTestFolder:
            listTestDir.append(rawTestDir)  
    for deleteItem in tempDeleteList:
        listTestDir.remove(deleteItem)
    
    return listTestDir


def GenerateNtp(rawTestDirList, FusionBuild):
       
    doc = Document()

    #Set project root 
    ntpProjectRoot = doc.createElement('NTest_Project_Root') 
    doc.appendChild(ntpProjectRoot)

    #Set Project Setting
    projectSetting = doc.createElement('Project_Settings') 
    ntpProjectRoot.appendChild(projectSetting)

    restartAfterFailedN = doc.createElement('Restart_After_Failed_N')
    projectSetting.appendChild(restartAfterFailedN)
    
    restartAfterFailedN_text = doc.createTextNode('1')
    restartAfterFailedN.appendChild(restartAfterFailedN_text)

    #Set cases root
    caseRoot = doc.createElement('Item')
    ntpProjectRoot.appendChild(caseRoot)

    caseRoot.setAttribute('CheckStatus', '1')
    caseRoot.setAttribute('IsDefaultPath','0')
    caseRoot.setAttribute('RunStatus','1')
    caseRoot.setAttribute('ScriptFile','') 
  
    #Set Automation case item        
    listTestDir = mergeTestDirOnList(rawTestDirList)
    
    for relativeTestDir in listTestDir:
        testDir = os.path.join(FusionBuild, relativeTestDir)
        if os.path.exists(testDir):
            rootnode = AddOfficialProductNode(doc, testDir, caseRoot, FusionBuild)
            AddFolderNode(testDir, doc, rootnode, FusionBuild)

    return doc

def AddOfficialProductNode(doc, testDir, caseRoot, FusionBuild):
    for officialProduct in officialProducts:
        productTestDirMarker = os.path.join(officialProduct, 'Test')
        if endWith(testDir,productTestDirMarker):
            productDir = os.path.join(testDir.split(productTestDirMarker)[0],officialProduct)
            newRootNode = AddCurrentNode(productDir, doc, caseRoot, '0', FusionBuild)          
            return newRootNode
    return caseRoot

def AddFolderNode(testCasesDir, doc, parentNode, FusionBuild):
    if inBlackList(testCasesDir):
        return
    currentNode = AddCurrentNode(testCasesDir, doc, parentNode, '0', FusionBuild) 
    items = os.listdir(testCasesDir)       
    for item in items:
        TestFolderDir = os.path.join(testCasesDir,item)
        AddItems(TestFolderDir, doc, currentNode, FusionBuild)
    if not currentNode.hasChildNodes():
        parentNode.removeChild(currentNode)

def AddItems(testCasesDir, doc, currentNode, FusionBuild): 
    if os.path.isdir(testCasesDir):
        AddFolderNode(testCasesDir, doc, currentNode, FusionBuild)    
        
    elif CheckIsCase(testCasesDir):
        AddCaseNode(testCasesDir, doc, currentNode, FusionBuild)       
 
def  AddCaseNode(testCasesDir, doc, currentNode, FusionBuild):
    AddCurrentNode(testCasesDir, doc, currentNode, '1', FusionBuild) 
      
def AddCurrentNode(testCasesDir, doc, caseRoot, isCase, FusionBuild):
    item = doc.createElement('Item')
    caseRoot.appendChild(item)

    item.setAttribute('CaseType', '0')
    item.setAttribute('IsCase', isCase)
    item.setAttribute('CheckStatus', '1')
    item.setAttribute('IsDefaultPath','1')
    item.setAttribute('RunStatus','1')    
    
    itemPath = polishPath(testCasesDir, FusionBuild)
    
    item.setAttribute('ScriptFile', itemPath) 
    return item


def CheckIsCase(item):
    testCaseMarker = '.txt'
    return endWith(item, testCaseMarker)

def endWith(s,*endstring):
        array = map(s.endswith,endstring)
        if True in array:
                return True
        else:
                return False

def polishPath(testCasesDir, FusionBuild):
    # Trim to relative path
    FusionBuildTrim = FusionBuild + '\\'
    relativePath = testCasesDir.split(FusionBuildTrim)[-1]
    
    # replace "\" on path
    relativePath = relativePath.replace('\\', '/') 
    
    return relativePath


# main is for testing

if  __name__  ==  "__main__":   

    # Test remove same folder on ListTestDir
    rawTestDirList = [
                      'Simulation\Test\Smoke',
                      'Fusion\Test',
                      'FusionDoc\Test\Smoke',
                      'Simulation\Test\Smoke',   
                      'NeuCAM\Test\Smoke',
                      'FusionDoc\Test\Smoke'
                   ]
    
    TestDirList = mergeTestDirOnList(rawTestDirList)
    print(TestDirList)
    FusionBuild = r'C:\Users\t_zhanj\AppData\Local\Autodesk\webdeploy\dev\a54b4b720935980385e2d8a3ba6e9cdba3a02af4'
    rawTestDirList = ['Fusion\Test',
                   'Animation\Test',
                   'FusionDoc\Test',
                   'Simulation\Test',
                   'Neutron\Test\Defects',
                   'Neutron\Test\Migration',
                   'Neutron\Test\Workflow',
                   'NeuCAM\Test']
   
    
    doc = GenerateNtp(rawTestDirList, FusionBuild)
    
    resultOutPut = r'D:\GeneratedNTP'
    ntpFileName = 'All.ntp'
    ntpfile = os.path.join(resultOutPut, ntpFileName)
    
    with open(ntpfile,'wb') as f:
        res = doc.toprettyxml(indent="  ", encoding="UTF-16")
        f.write(res)

        


