import os
import math
import xml.dom.minidom
import glob
import subprocess
import threading
import time
import codecs
import numpy as np
import datetime

class Command(object):
	def __init__(self, cmd, processes):
		self.cmd = cmd
		self.processes = processes
		self.process = None

	def run(self, timeout):
		def target():
			self.process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			self.process.communicate()

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(timeout)
		if thread.is_alive():
			print 'Terminating process'
			self.KillProcessCmd(self.processes)
			self.process.terminate()
			thread.join()
		print self.process.returncode
		return self.process.returncode

	def KillProcessCmd(self, processes):
		for process in processes:
			if os.name == 'nt':
				os.system('taskkill /f /im \"' + process + '*\"')
				os.system('tskill \"' + process + '*\"')
			elif os.name == 'posix':
				cmd = 'killall -9 \"' + process + '\"'
				print cmd
				p = subprocess.Popen(["killall", "-9", process], stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)

def extractData(fullPath, type):
	# Just extract performance data, ignore capacity currently

	# parse all files in the inputed directory
	dataDict = {}
	dataDictLA = {}
	for fn in glob.glob(fullPath + os.sep + "*"):
		if not os.path.isfile(fn):
			continue

		path, fileName = os.path.split(fn)
		name, ext = os.path.splitext(fileName)
		if ext != ".xml":
			continue

		# right file
		inputDom = xml.dom.minidom.parse(fn)

		#print("Start recording the data in: " + fn)
		inputRootNode = inputDom.documentElement
		errorDeltaValue = "NO_error"
		for subNode in inputRootNode.childNodes:
			# just look at performance data
			nodeTypeName = subNode.nodeName.lower()
			if nodeTypeName not in ('elapsedtime', 'fps', 'framerategraphics'):
				continue
			if subNode.nodeType != subNode.ELEMENT_NODE:
				continue

			desValue = subNode.getAttribute("description")
			if desValue == "Error Delta":
				errorDeltaValue = subNode.getAttribute("value")
				continue

			fullTestName = desValue
			if fullTestName not in dataDict.keys():
				dataDict[fullTestName] = []

			# valuable node
			realValue = subNode.getAttribute("value")
			dataDict[fullTestName].append(float(realValue))

			if type == 'LA':
				if fullTestName not in dataDictLA.keys():
					dataDictLA[fullTestName] = {}
				if nodeTypeName not in dataDictLA[fullTestName].keys():
					dataDictLA[fullTestName][nodeTypeName] = []
				realValue = subNode.getAttribute("value")
				dataDictLA[fullTestName][nodeTypeName].append(float(realValue))
				# delete input dom
		del inputDom

	if type == 'LA':
		return dataDictLA
	else :
		resultList = []
		for tmp in dataDict:
			resultList.append(dataDict[tmp])
		return resultList


def StdMeanRatio(valuelist):
	array = np.array(valuelist)
	ratio = array.std()/array.mean()
	return ratio

def CheckData(exePath, testcase, ntpProject):
	path, fileName = os.path.split(testcase)
	name, ext = os.path.splitext(fileName)

	path, fileName = os.path.split(exePath)
	print "ntpProject name on Checkdata is: " +ntpProject
	
	if ntpProject == 'largeAssembly': #LA
		if os.name == 'nt': #As integrate from main to RC that the old path (Neutron/Test/Capacity) is useless
			#if 'dev' in path: #For main build
			performanceDir = path.replace('\\', '/') + '/Result/Neutron/Test/Capacity/'
			#else: #For RC,CU build
				#performanceDir = path.replace('\\', '/') + '/Neutron/Test/Capacity/'
		elif os.name == 'posix': #As integrate from main to RC that the old path (Neutron/Test/Capacity) is useless
			#if 'dev' in exePath:
			performanceDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Result', 'Neutron', 'Test', 'Capacity')
			#else:
				#performanceDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Neutron', 'Test', 'Capacity')
	
	else: #Modeling perofrmance
		if os.name == 'nt': #As integrate from main to RC that the old path (Neutron/Test/Capacity) is useless
			#if 'dev' in path: #For main build
			performanceDir = path.replace('\\', '/') + '/Result/Neutron/Test/Performance/'
			#else: #For RC,CU build
				#performanceDir = path.replace('\\', '/') + '/Neutron/Test/Performance/'
		elif os.name == 'posix': #As integrate from main to RC that the old path (Neutron/Test/Capacity) is useless
			#if 'dev' in exePath:
			performanceDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Result', 'Neutron', 'Test', 'Performance')
			#else:
				#performanceDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Neutron', 'Test', 'Performance')
	
		
		
	resultDir = None
	list_dirs = os.walk(performanceDir)
	for root, dirs, files in list_dirs:
		for d in dirs:
			if name.lower() == d.lower():
				resultDir = os.path.join(root, d)
				break
	
	if (resultDir == None):
		print "Failed to get result directory for case: " + name
		return True
	data = extractData(resultDir, 'checkdata')
	for tmp in data:
		if (len(tmp) < 3):
			return False
		if (StdMeanRatio(tmp) > 0.04):
			return False
	return True

def RunTestCase(exePath, testcasePath, processes, ntpProject):
	cmd = ''
	if os.name == "nt":
		cmd = '"{0}" -execute "test.run {1} /CloseAfterDone"'.format(exePath, testcasePath)
	elif os.name == 'posix':
		cmd = "open -W \"{0}\" --args nothing -execute \"test.run \\\"{1}\\\" /CloseAfterDone\"".format(exePath, testcasePath)
	print cmd
	#os.system(cmd)
	#p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	#(stdoutput,erroutput) = p.communicate()
	#print stdoutput, erroutput
	#processes = ['Fusion360', 'Autodesk Fusion 360 [dev]', 'Autodesk Fusion 360 [staging]']

	command = Command(cmd, processes)
	returncode = command.run(timeout=900)

	if returncode != 0:
		GenerateFailureXML(exePath, testcasePath, ntpProject)
	# Kill the Fusion process because test.run cannot kill itself now
	KillProcess(processes)

def GenerateFailureXML(exePath, testcasePath, ntpProject):
	impl = xml.dom.minidom.getDOMImplementation()
	dom = impl.createDocument(None, "Metrics", None)
	dom.version = '1.0'  
	dom.encoding = 'UTF-16'  
	dom.standalone = 'no'
	
	root = dom.documentElement  
	elem = dom.createElement('Fail')
	root.appendChild(elem)
	
	print "Current performance type is: " + ntpProject
	if ntpProject.lower() == 'largeassembly':
		if 'dev' in exePath: #For main build
			testcase = testcasePath.split('Neutron/Test/Capacity/')[-1].split('.txt')[0]
			if os.name == 'nt':
				resultDir = os.path.join(os.path.dirname(exePath), 'Result', 'Neutron', 'Test', 'Capacity')
			elif os.name == 'posix':
				resultDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Result', 'Neutron', 'Test', 'Capacity')
			caseDir = os.path.join(resultDir, testcase)
		
			if not os.path.exists(caseDir):
				print "create result directory for failure case if it is not exists"
				print caseDir
				os.makedirs(caseDir)

				f = codecs.open(os.path.join(caseDir, os.path.basename(testcase)+'_'+str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))+'.xml'), 'w', 'utf-16')
				dom.writexml(f,'\n',' ','')
				f.close()
		else: #For RC,CU build
			testcase = os.path.basename(testcasePath).split('.txt')[0]
			if os.name == 'nt':
				resultDir = os.path.join(os.path.dirname(exePath), 'Neutron', 'Test', 'Performance')
			elif os.name == 'posix':
				resultDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Neutron', 'Test', 'Performance')
			caseDir = os.path.join(resultDir, testcase)

			if not os.path.exists(caseDir):
				os.makedirs(caseDir)

			f = codecs.open(os.path.join(caseDir, testcase+'_'+str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))+'.xml'), 'w', 'utf-16')
			dom.writexml(f,'\n',' ','')
			f.close()
	
	else: #ntpProject.lower() == 'performance'
		if 'dev' in exePath: #For main build
			testcase = testcasePath.split('Neutron/Test/Performance/')[-1].split('.txt')[0]
			if os.name == 'nt':
				resultDir = os.path.join(os.path.dirname(exePath), 'Result', 'Neutron', 'Test', 'Performance')
			elif os.name == 'posix':
				resultDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Result', 'Neutron', 'Test', 'Performance')
			caseDir = os.path.join(resultDir, testcase)
		
			if not os.path.exists(caseDir):
				print "create result directory for failure case if it is not exists"
				print caseDir
				os.makedirs(caseDir)

				f = codecs.open(os.path.join(caseDir, os.path.basename(testcase)+'_'+str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))+'.xml'), 'w', 'utf-16')
				dom.writexml(f,'\n',' ','')
				f.close()
		else:#For RC,CU build
			testcase = os.path.basename(testcasePath).split('.txt')[0]
			if os.name == 'nt':
				resultDir = os.path.join(os.path.dirname(exePath), 'Neutron', 'Test', 'Performance')
			elif os.name == 'posix':
				resultDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Neutron', 'Test', 'Performance')
			caseDir = os.path.join(resultDir, testcase)

			if not os.path.exists(caseDir):
				os.makedirs(caseDir)

			f = codecs.open(os.path.join(caseDir, testcase+'_'+str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))+'.xml'), 'w', 'utf-16')
			dom.writexml(f,'\n',' ','')
			f.close()
		

def KillProcess(processes):
	for process in processes:
		if os.name == 'nt':
			os.system('taskkill /f /im \"' + process + '*\"')
			os.system('tskill \"' + process + '*\"')
		elif os.name == 'posix':
			os.system('killall -9 \"' + process + '\"')

def parseNtpFile(exePath, ntpFile):
	scriptList = []
	path, fileName = os.path.split(exePath)

	ntpDom = xml.dom.minidom.parse(ntpFile)
	rootNode = ntpDom.documentElement
	for subNode in rootNode.getElementsByTagName("Item"):
		scriptFile = subNode.getAttribute("ScriptFile")
		name, ext = os.path.splitext(scriptFile)
		if ext != ".txt":
			continue
		if os.name == 'nt':
			scriptList.append(path.replace('\\', '/') + '/' + scriptFile)
		elif os.name == 'posix':
			scriptList.append(os.path.dirname(exePath) + '/Libraries/Neutron/' + scriptFile)

	return scriptList

def RunMgr(exePath, ntpFile, processes,label, ntpProject):
	testCases = parseNtpFile(exePath, ntpFile)
	for i in range(3):
		for testcase in testCases:
			RunTestCase(exePath, testcase, processes,ntpProject)


	for testcase in testCases:
		if (CheckData(exePath, testcase, ntpProject)):
			continue
		else:
			print "Test case {0} is not stable, rerun it".format(testcase)
			for i in range(3):
				RunTestCase(exePath, testcase, processes,ntpProject)
	#if -1 != ntpProject.lower().find('perf'):
		#process_Model_TestResult(exePath, testCases,label)
	#elif -1 != ntpProject.lower().find('largeassembly'):
		#process_LA_TestResult(exePath, testCases,label)
	WriteResultToDB(ntpFile, exePath)

def WriteResultToDB(ntpFile, exePath):
	if 'dev' in exePath:
		if os.name == 'nt':
			resultDir = os.path.join(os.path.dirname(exePath), 'Result', 'Neutron', 'Test', 'Performance')
			cmd = r'python35\win\python CITools\save_performance_test_result_from_dir.py "{0}" "{1}"'.format(ntpFile, resultDir)
		elif os.name == 'posix':
			resultDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Result', 'Neutron', 'Test', 'Performance')
			cmd = r'python3 CITools/save_performance_test_result_from_dir.py "{0}" "{1}"'.format(ntpFile, resultDir)
	else:
		if os.name == 'nt':
			resultDir = os.path.join(os.path.dirname(exePath), 'Neutron', 'Test', 'Performance')
			cmd = r'python35\win\python CITools\save_performance_test_result_from_dir.py "{0}" "{1}"'.format(ntpFile, resultDir)
		elif os.name == 'posix':
			resultDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Neutron', 'Test', 'Performance')
			cmd = r'python3 CITools/save_performance_test_result_from_dir.py "{0}" "{1}"'.format(ntpFile, resultDir)
	print cmd
	os.system(cmd)


if __name__ == '__main__':
	a = CheckData(r"E:\TESTDATA\NewDesign\production\fusion.exe", r"E:\TESTDATA\NewDesign\Result\Neutron\Test\Performance\Modeling\Image\Fusion_Image_Decal.txt")
	print a
	#RunMgr("c:\\fusion.exe", "PerformanceNew.ntp")
