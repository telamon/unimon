from ctypes import *

#Define the data structure for core_temp_shared_data
class core_temp_shared_data(Structure):
	_fields_ = [
		("uiLoad", c_uint * 256), #The * operand makes an array of n
		("uiTjMax", c_uint * 128),
		("uiCoreCnt", c_uint),
		("uiCPUCnt", c_uint),
		("fTemp", c_float * 256),
		("fVID", c_float),
		("fCPUSpeed", c_float),
		("fFSBSpeed", c_float),
		("fMultipier", c_float),
		("fMultipier", c_float),
		("sCPUName", c_char * 100),
		("ucFahrenheit", c_ubyte),
		("ucDeltaToTjMax", c_ubyte)
	]

GetCoreTempInfo = WinDLL('GetCoreTempInfo.dll')
GetCoreTempInfo.restype =  c_bool
GetCoreTempInfo.argtypes = [core_temp_shared_data]

#Create a variable of type core_temp_shared_data and a pointer to it
coretemp = core_temp_shared_data();
a1 = pointer(coretemp)

coretempRunning = False
def UpdateCoreTemp():
	""" This function calls the dll to update coretemp variable with system data
	"""
	global coretempRunning
	result = GetCoreTempInfo.fnGetCoreTempInfoAlt(a1) #Returns 0 if fail, 1 if success

	if result==0:
		print  "Error: ", GetLastError()
		print  FormatError()

		if GetLastError()==2:
			print "Coretemp.exe is not running, it must be running for this progam to work"
			coretempRunning = False
	else:
		coretempRunning = True

def GetCoreTemperatures():
	"""Returns the data value in the coretemp structure that corresponds to the array of core temperatures
	"""
	global coretempRunning
	if coretempRunning == False:
		return {"error": "Coretemp is not running on the monitored pc"}

	ret = []
	for i in range(coretemp.uiCoreCnt):
		ret.append(coretemp.fTemp[i])

	return ret

def GetCoreLoad():
	"""Returns the data value in the coretemp structure that corresponds to the array of core loads
	"""
	global coretempRunning
	if coretempRunning == False:
		return {"error": "Coretemp is not running on the monitored pc"}

	ret = []
	for i in range( coretemp.uiCoreCnt):
		ret.append(int(coretemp.uiLoad[i]))
	return ret
