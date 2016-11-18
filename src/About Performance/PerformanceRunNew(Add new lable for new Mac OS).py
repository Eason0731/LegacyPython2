import os
import math
import xml.dom.minidom
import glob
import subprocess
import threading
import MySQLdb
import time
import pymongo,uuid, datetime, platform #Added by Wally
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except:
    pass

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

	def KillProcessCmd(self, processes):
		for process in processes:
			if os.name == 'nt':
				os.system('taskkill /f /im \"' + process + '*\"')
				os.system('tskill \"' + process + '*\"')
			elif os.name == 'posix':
				cmd = 'killall -9 \"' + process + '\"'
				print cmd
				p = subprocess.Popen(["killall", "-9", process], stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)

# Added By Wally
class mongo:
    def __init__(self, url, port, dbName, collection):
        client = pymongo.MongoClient(url, port)
        self.db = client[dbName]
        self.collection = collection

    def save(self, dic, collection = 'default-pymongo-collection##'):
        if collection == 'default-pymongo-collection##':
            insert_collection = self.collection
        else:
            insert_collection = collection
        insertID = self.db[insert_collection].save(dic)
        return insertID

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


def varAgainstMean(valuelist):
	sum1=0.0
	sum2=0.0
	N = len(valuelist)
	for i in range(N):
		sum1+=valuelist[i]
		sum2+=valuelist[i]**2
	mean=sum1/N
	var=sum2/N-mean**2
	return var/mean

def CheckData(exePath, testcase):
	path, fileName = os.path.split(testcase)
	name, ext = os.path.splitext(fileName)

	path, fileName = os.path.split(exePath)
	resultDir = ''
	if os.name == 'nt':
		resultDir = path.replace('\\', '/') + '/Neutron/Test/Performance/' + name
	elif os.name == 'posix':
		resultDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Neutron', 'Test', 'Performance', name)

	data = extractData(resultDir, 'checkdata')
	for tmp in data:
		if (varAgainstMean(tmp) > 0.08):
			return False
	return True

def RunTestCase(exePath, testcasePath, processes):
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
	command.run(timeout=900)
	# Kill the Fusion process because test.run cannot kill itself now
	KillProcess(processes)

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

def execute_sql(sql):
	result = ();
	try:
		#print "execute sql = ", sql
		conn = MySQLdb.connect(host="10.148.227.108",user="root",passwd="123456",db="db_fusion",charset="utf8")
		cursor = conn.cursor()
		n = cursor.execute(sql)
		result = cursor.fetchall()
		#print 'insert',n
		#print result
		cursor.close()
		conn.commit()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])

	return result



def	insert_perf_table_intoDB(buildid):
	buildtype = ''
	if buildid[2] == '0':
		buildtype = 'fusionsite_perf_rc'
	elif buildid[2] == '1':
		buildtype = 'fusionsite_perf_main'

	OSname = ''
	if os.name == 'nt':
		OSname = 'Win'
	elif os.name == 'posix':
		#OSname = 'Mac'
		if (os.path.exists("/Users/Perf_Yosemite")):
                    OSname = 'Mac 10.10'
                else:
                    OSname = 'Mac 10.12'

	StartTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

	sql = "insert into " + buildtype + "(BuildId, OS, label, AverageTime, AverGraphicsFPS, StartTime, EndTime) values('" + buildid + "','" + OSname + "',0,0,0,'" + StartTime +"',0);"
	execute_sql(sql)



def	insert_perf_workflow_intoDB(workflow, buildid, OSname):
	table_workflow = ''
	if buildid[2] == '0':
		table_workflow = 'fusionsite_perf_rc_workflow'
	elif buildid[2] == '1':
		table_workflow = 'fusionsite_perf_main_workflow'

	sql = "select 1 from " + table_workflow + " where BuildId = '" + buildid + "' and workflow = '" + workflow + "' and OS = '" + OSname + "';"
	result = execute_sql(sql)
	#print result
	insert_sql = ''
	if result == ():
		insert_sql = "insert into " + table_workflow + "(BuildId, workflow, OS, AverageTime) values('" + buildid + "','" + workflow + "','" + OSname + "',0);"
		execute_sql(insert_sql)

def	update_all_table(buildid, OSname):
	tbl_perf = ''
	flag_perf = 0
	mongo_doc = {"data":{}} # By Wally - init mongo_doc
	if buildid[2] == '0':
		tbl_perf = 'fusionsite_perf_rc'
		tbl_workflow = 'fusionsite_perf_rc_workflow'
		tbl_testcase = 'fusionsite_perf_rc_testcase'
		mongo_doc['branch'] = 'rc' # By Wally
	elif buildid[2] == '1':
		tbl_perf = 'fusionsite_perf_main'
		tbl_workflow = 'fusionsite_perf_main_workflow'
		tbl_testcase = 'fusionsite_perf_main_testcase'
		mongo_doc['branch'] = 'main' # By Wally

	#update workflow
	sql = "select workflow from " + tbl_workflow + " where BuildId = '" + buildid + "' and OS = '" + OSname + "';"
	results = execute_sql(sql)
	#print results
	timeresult = 0
	time_workflow = 0
	FPS_Graphics = 0
	count_workflow = 0
	if len(results)== 0:
		time_workflow = 0
		FPS_Graphics = 0
	else :
		for workflow in results:
			count_workflow = 0
			timeresult = 0
			sql = "select AverageTime from " + tbl_testcase + " where BuildId = '" + buildid + "' and OS = '" + OSname + "' and workflow = '" + workflow[0] + "';"
			average_casetime = execute_sql(sql)
			for i in average_casetime:
				if i[0] == 0:
					count_workflow = count_workflow + 1
				timeresult = timeresult + i[0]
			number = len(average_casetime)-count_workflow
			if number == 0 :
				timeresult = 0
			else:
				timeresult = timeresult/ number
			sql_update = "UPDATE " + tbl_workflow + " SET AverageTime = " + bytes(timeresult)[0:9] + " where BuildId = '" + buildid + "' and OS = '" + OSname + "' and workflow = '" + workflow[0] + "';"

			# Add to mongo_doc - by Wally
			m_work_folw = workflow[0]
			mongo_doc['data'][m_work_folw] = timeresult

			#print sql_update
			execute_sql(sql_update)
			if workflow[0] == "FUS_Graphics":
				FPS_Graphics = timeresult
			else:
				time_workflow = time_workflow + timeresult

		time_workflow = time_workflow/(len(results)-1)
	EndTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
	sql_flag = "select * from " + tbl_testcase + " where BuildId = '" + buildid + "' and OS = '" + OSname + "' and Value = '';"
	results = execute_sql(sql_flag)
	print results
	if len(results) != 0:
		flag_perf = 1
	up_workflow =  "UPDATE " + tbl_perf + " SET AverageTime = " + bytes(time_workflow)[0:9] + " , AverGraphicsFPS = " + bytes(FPS_Graphics)[0:9] + " , EndTime = '" + EndTime + "', flag = " + bytes(flag_perf) + " where BuildId = '" + buildid + "' and OS = '" + OSname + "';"
	results = execute_sql(up_workflow)

	# Insert to mongo - by Wally
	MONGO_PROD_URL = '10.35.131.198'
	MONGO_STG_URL = '10.148.173.92'
	mongo_stg_instance = mongo(MONGO_STG_URL, 27017, 'fusion_rating', 'model_performance_raw')
	mongo_prod_instance = mongo(MONGO_PROD_URL, 27017, 'fusion_rating', 'model_performance_raw')
	mongo_doc['_id'] = str(uuid.uuid4())
	mongo_doc['platform'] = OSname
	mongo_doc['platform_detail'] = str(platform.platform())
	mongo_doc['build'] = buildid
	mongo_doc['exec_time'] = datetime.datetime.utcnow()
	mongo_stg_instance.save(mongo_doc)
	mongo_prod_instance.save(mongo_doc)
	print "Export Workflow to QMetrix as: %s"%mongo_doc # Please comment out if you don't need it

def process_Model_TestResult(exePath, testCases, buildid):
	insert_perf_table_intoDB(buildid)
	OSname = ''
	for testcase in testCases:
		path, fileName = os.path.split(testcase)
		#print("path, fileName", path, fileName)
		name, ext = os.path.splitext(fileName)
		#print("name, ext", name, ext)
		path, fileName = os.path.split(exePath)
		resultDir = ''
		if os.name == 'nt':
			OSname = 'Win'
			resultDir = path.replace('\\', '/') + '/Neutron/Test/Performance/' + name
		elif os.name == 'posix':
			OSname = 'Mac'
			resultDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Neutron', 'Test', 'Performance', name)

		data = extractData(resultDir, 'Perf')
		workflow = name.split('_',2)[0] + '_' + name.split('_',2)[1]
		insert_perf_workflow_intoDB(workflow, buildid, OSname)
		Averagetime = 0.0
		Value = ''
		if data== []:
			Value = ''
		else:
			for i in range(0, len(data[0])):
				Averagetime = Averagetime + data[0][i]
				Value = Value + str(data[0][i]) + ":"
			Averagetime = str(Averagetime/(i+1))
		table_testcase = ''
		if buildid[2] == '0':
			table_testcase = 'fusionsite_perf_rc_testcase'
		elif buildid[2] == '1':
			table_testcase = 'fusionsite_perf_main_testcase'
		testcase_sql = "insert into " + table_testcase + "(BuildId, OS, workflow, TestCaseName, Value, AverageTime) values('" + buildid + "','" + OSname + "','" + workflow + "','" + name + "','" + Value +"','" + bytes(Averagetime)[0:9] + "');"
		execute_sql(testcase_sql)
	update_all_table(buildid, OSname)


def	update_LAworkflow(buildid, tbl_workflow, OSname):
	StartTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
	components = ['Data', 'UI', 'Compute', 'Viewing', 'Roll', 'EditMiddle']
	for workflow in components:
		sql = "insert into " + tbl_workflow + "(BuildId, workflow, OS, AverageTime, StartTime, Label) values('" + buildid + "','" + workflow + "','" + OSname + "',0,'" + StartTime + "',0);"
		execute_sql(sql)

def update_LA_table(buildid, tbl_workflow, tbl_testcase, OSname):
	sql = "select Workflow from " + tbl_workflow + " where BuildId = '" + buildid + "' and OS = '" + OSname + "';"
	results = execute_sql(sql)
	#print results
	timeresult = 0
	count_workflow = 0
	if len(results)== 0:
		print sql
		time_workflow = 0
	else :
		for workflow in results:
			timeresult = 0
			sql = "select AverageTime from " + tbl_testcase + " where BuildId = '" + buildid + "' and OS = '" + OSname + "' and workflow = '" + workflow[0] + "';"
			print sql
			average_casetime = execute_sql(sql)
			for i in average_casetime:
				if i[0] == 0:
					count_workflow = count_workflow + 1
				timeresult = timeresult + i[0]
			number = len(average_casetime)-count_workflow
			if number == 0:
				timeresult = 0
			else:
				timeresult = timeresult/(len(average_casetime)-count_workflow)
			EndTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
			sql_update = "UPDATE " + tbl_workflow + " SET AverageTime = " + bytes(timeresult)[0:9] + " , EndTime = '" + EndTime + "' where BuildId = '" + buildid + "' and OS = '" + OSname + "' and workflow = '" + workflow[0] + "';"
			print sql_update
			execute_sql(sql_update)

def update_tbl_viewing(buildid, tbl_viewing, name, OSname, data):
	categoryList = ('Pan','FreeOrbit','Orbit','Zoom')
	dict = analyse_data(data, categoryList)
	#print dict
	sql = "insert into " + tbl_viewing + "(BuildId, workflow, OS, TestCaseName, PanTime, PanAverageTime,PanFPS,PanAverageFPS,OrbitTime,OrbitAverageTime,OrbitFPS, OrbitAverageFPS,ZoomTime,ZoomAverageTime,ZoomFPS,ZoomAverageFPS,FreeOrbitTime,FreeOrbitAverageTime,FreeOrbitFPS,FreeOrbitAverageFPS) values ('"\
	+ buildid + "','viewing','" + OSname + "','" + name + "','" + \
	dict['Pan']['elapsedtime'][0] + "','" + dict['Pan']['elapsedtime'][1] + "','" + dict['Pan']['framerategraphics'][0] + "','" + dict['Pan']['framerategraphics'][1] + "','" + \
	dict['Orbit']['elapsedtime'][0] + "','" + dict['Orbit']['elapsedtime'][1] + "','" + dict['Orbit']['framerategraphics'][0] + "','" + dict['Orbit']['framerategraphics'][1] + "','" + \
	dict['Zoom']['elapsedtime'][0] + "','" + dict['Zoom']['elapsedtime'][1] + "','" + dict['Zoom']['framerategraphics'][0] + "','" + dict['Zoom']['framerategraphics'][1] + "','" + \
	dict['FreeOrbit']['elapsedtime'][0] + "','" + dict['FreeOrbit']['elapsedtime'][1] + "','" + dict['FreeOrbit']['framerategraphics'][0] + "','" + dict['FreeOrbit']['framerategraphics'][1]+ "');"
	#print sql
	execute_sql(sql)


def update_tbl_compute(buildid, tbl_computer, name, OSname, data):
	categoryList = ('ComputeAll',)
	dict = analyse_data(data, categoryList)
	#print dict
	sql = "insert into " + tbl_computer + "(BuildId, workflow, OS, TestCaseName, ComputeAll, ComputeAllAverage) values ('" + buildid + "','Computer','" + OSname + "','" + name + "','" + dict['ComputeAll']['elapsedtime'][0] + "','" + dict['ComputeAll']['elapsedtime'][1] + "');"
	#print sql
	execute_sql(sql)

def updata_tbl_editmid(buildid, tbl_deitMiddle, name, OSname, data):
	categoryList = ('EditMiddle', 'Undo' ,)
	dict = analyse_data(data, categoryList)
	#print dict
	sql = "insert into " + tbl_deitMiddle + "(BuildId, workflow, OS, TestCaseName, EditMiddle, EditMiddleAverage, UndoValue, UndoAverage) values ('" + buildid + "','editmid','" + \
	OSname + "','" + name + "','" + dict['EditMiddle']['elapsedtime'][0] + "','" + dict['EditMiddle']['elapsedtime'][1] + "','" +dict['Undo']['elapsedtime'][0] + "','" + dict['Undo']['elapsedtime'][1] + "');"
	#print sql
	execute_sql(sql)


def	update_tbl_roll(buildid, tbl_roll, name, OSname, data):
	categoryList = ('Roll',)
	dict = analyse_data(data, categoryList)
	#print dict
	sql = "insert into " + tbl_roll + "(BuildId, workflow, OS, TestCaseName, Roll, RollAverage) values ('" + buildid + "','Roll','" + OSname + "','" + name + "','" + dict['Roll']['elapsedtime'][0] + "','" + dict['Roll']['elapsedtime'][1] + "');"
	#print sql
	execute_sql(sql)


def update_tbl_UI(buildid, tbl_UI, name, OSname, data):
	print data
	categoryList = ('ToggleVisibility','InvokeCommand','CancelCommand','ChangeEnv')
	dict = analyse_data(data, categoryList)
	print dict
	sql = "insert into " + tbl_UI + "(BuildId, workflow, OS, TestCaseName, ToggleVisibility,ToggleVisibilityAverage,InvokeCommand,InvokeCommandAverage,CancelCommand,CancelCommandAverage, ChangeEnv,ChangeEnvAverage) values ('"\
	+ buildid + "','UI','" + OSname + "','" + name + "','" + \
	dict['ToggleVisibility']['elapsedtime'][0] + "','" + dict['ToggleVisibility']['elapsedtime'][1] + "','" + dict['InvokeCommand']['elapsedtime'][0] + "','" + dict['InvokeCommand']['elapsedtime'][1] + "','" +\
	dict['CancelCommand']['elapsedtime'][0] + "','" + dict['CancelCommand']['elapsedtime'][1] + "','" + dict['ChangeEnv']['elapsedtime'][0] + "','" + dict['ChangeEnv']['elapsedtime'][1] + "');"
	print sql
	execute_sql(sql)

def updata_tbl_data(buildid, tbl_data, name, OSname, data):
	categoryList = ('Import', 'Export' ,)
	dict = analyse_data(data, categoryList)
	#print dict
	sql = "insert into " + tbl_data + "(BuildId, workflow, OS, TestCaseName, Import, ImportAverage, Export, ExportAverage) values ('" + buildid + "','Data','" + OSname +\
	"','" + name + "','" + dict['Import']['elapsedtime'][0] + "','" + dict['Import']['elapsedtime'][1] + "','" +dict['Export']['elapsedtime'][0] + "','" + dict['Export']['elapsedtime'][1] + "');"
	print sql
	execute_sql(sql)


def analyse_data(data, categoryList):
	dict = {}

	for temp in categoryList:
		print ('temp', temp)
		if temp not in data.keys():
			dict[temp]={'elapsedtime':['0', '0'], 'framerategraphics':['0', '0']}
			continue

		dict[temp]={}
		for category in ('elapsedtime', 'framerategraphics'):
			value = ''
			if category not in data[temp].keys():
				dict[temp][category] = ['0', '0']
				continue

			for i in data[temp][category]:
				value = value + str(i) + ':'
			average = sum(data[temp][category])/len(data[temp][category])
			dict[temp][category] = [value, str(average)]
			#print dict
	return dict


def process_LA_TestResult(exePath, testCases, buildid):
	if buildid[2] == '0':
		tbl_workflow = 'fusionsite_la_rc_workflow'
		tbl_computer = 'fusionsite_la_rc_computer'
		tbl_data = 'fusionsite_la_rc_data'
		tbl_deitMiddle = 'fusionsite_la_rc_editmiddle'
		tbl_roll = 'fusionsite_la_rc_roll'
		tbl_UI = 'fusionsite_la_rc_ui'
		tbl_viewing = 'fusionsite_la_rc_viewing'
	elif buildid[2] == '1':
		tbl_workflow = 'fusionsite_la_main_workflow'
		tbl_computer = 'fusionsite_la_main_computer'
		tbl_data = 'fusionsite_la_main_data'
		tbl_deitMiddle = 'fusionsite_la_main_editmiddle'
		tbl_roll = 'fusionsite_la_main_roll'
		tbl_UI = 'fusionsite_la_main_ui'
		tbl_viewing = 'fusionsite_la_main_viewing'

	OSname = ''
	if os.name == 'nt':
		OSname = 'Win'
	elif os.name == 'posix':
		OSname = 'Mac'
	update_LAworkflow(buildid, tbl_workflow, OSname)

	for testcase in testCases:
		path, fileName = os.path.split(testcase)
		path, workFlowName = os.path.split(path)
		print workFlowName
		if -1 != workFlowName.find('_'):
			workFlowName = workFlowName[(workFlowName.find('_')+1):]
			print workFlowName
		#print("path, fileName", path, fileName)
		name, ext = os.path.splitext(fileName)
		name = name.replace("'", "")
		#print("name, ext", name, ext)
		path, fileName = os.path.split(exePath)
		#print("path, fileName", path, fileName)
		resultDir = ''
		if os.name == 'nt':
			OSname = 'Win'
			resultDir = path.replace('\\', '/') + '/Neutron/Test/Performance/' + name
		elif os.name == 'posix':
			OSname = 'Mac'
			resultDir = os.path.join(os.path.dirname(exePath), 'Libraries', 'Neutron', 'Neutron', 'Test', 'Performance', name)

		data = extractData(resultDir, 'LA')
		if workFlowName == 'Viewing':
			update_tbl_viewing(buildid, tbl_viewing, name, OSname, data)
		elif workFlowName == 'Data':
			updata_tbl_data(buildid, tbl_data, name, OSname, data)
		elif workFlowName == 'Compute':
			update_tbl_compute(buildid, tbl_computer, name, OSname, data)
		elif workFlowName == 'EditMid':
			updata_tbl_editmid(buildid, tbl_deitMiddle, name, OSname, data)
		elif workFlowName == 'Roll':
			update_tbl_roll(buildid, tbl_roll, name, OSname, data)
		elif workFlowName == 'UI':
			update_tbl_UI(buildid, tbl_UI, name, OSname, data)
			print "123456789"
	#update_LA_table(buildid, tbl_workflow, tbl_testcase, OSname)

def RunMgr(exePath, ntpFile, processes,label, ntpProject):
	testCases = parseNtpFile(exePath, ntpFile)
	for i in range(3):
		for testcase in testCases:
			RunTestCase(exePath, testcase, processes)


	for testcase in testCases:
		if (CheckData(exePath, testcase)):
			continue
		else:
			print "Test case {0} is not stable, rerun it".format(testcase)
			for i in range(3):
				RunTestCase(exePath, testcase, processes)
	if -1 != ntpProject.lower().find('perf'):
		process_Model_TestResult(exePath, testCases,label)
	elif -1 != ntpProject.lower().find('largeassembly'):
		process_LA_TestResult(exePath, testCases,label)


if __name__ == '__main__':
	RunMgr("c:\\fusion.exe", "PerformanceNew.ntp")
