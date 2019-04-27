import win32api, win32process, win32con
from ctypes import *
from ctypes.wintypes import *


class PROCESSENTRY32(Structure):
    _fields_ = [ ( 'dwSize' , DWORD ) ,
    ( 'cntUsage' , DWORD) ,
    ( 'th32ProcessID' , DWORD) ,
    ( 'th32DefaultHeapID' , POINTER(ULONG)) ,
    ( 'th32ModuleID' , DWORD) ,
    ( 'cntThreads' , DWORD) ,
    ( 'th32ParentProcessID' , DWORD) ,
    ( 'pcPriClassBase' , LONG) ,
    ( 'dwFlags' , DWORD) ,
    ( 'szExeFile' , c_char * 260 ) ]


class Memory(object):

	def __init__(self):
		self.CreateToolhelp32Snapshot = CDLL("kernel32.dll").CreateToolhelp32Snapshot
		self.Process32First = CDLL("kernel32.dll").Process32First
		self.Process32Next = CDLL("kernel32.dll").Process32Next
		self.GetLastError = CDLL("kernel32.dll").GetLastError
		self.CloseHandle = CDLL("kernel32.dll").CloseHandle
		self.OpenProcess = CDLL("kernel32.dll").OpenProcess
		self.ReadProcessMemory = CDLL("kernel32.dll").ReadProcessMemory
		self.WriteProcessMemory = CDLL("kernel32.dll").WriteProcessMemory
		self.VirtualProtectEx = CDLL("kernel32.dll").VirtualProtectEx
		self.EnumProcessModulesEx = CDLL("Psapi.dll").EnumProcessModulesEx
		self.TH32CS_SNAPPROCESS = 0x00000002
		self.ALL_ACCESS = 0x1f0fff
		

	def EnumModules(self, Handle):
		return win32process.EnumProcessModulesEx(Handle, 3)


	def GetProcessIDByName(self, pname):
		pname = bytes(pname, encoding="utf8")
		hSnapshot = HANDLE
		hSnapshot = self.CreateToolhelp32Snapshot(self.TH32CS_SNAPPROCESS, 0)

		if (hSnapshot):
			pe32 = PROCESSENTRY32()
			pe32.dwSize = sizeof(PROCESSENTRY32);
			process = self.Process32First(hSnapshot, byref(pe32))
		while True:
			process = self.Process32Next(hSnapshot, byref(pe32))
			if process:
				if pe32.szExeFile.lower() == pname.lower():
					return pe32.th32ProcessID
			else:
				print("Process not found!")
				return False
		else:
			print("Snapshot failed!")
			return False


	def GetProcessHandle(self, pname, hType):
		pid = self.GetProcessIDByName(pname)
		if pid and type(1) == type(pid):
			if hType == 0:
				phandle = HANDLE(self.OpenProcess(DWORD(self.ALL_ACCESS),False,DWORD(pid)))
			elif hType == 1:
				phandle = self.OpenProcess(DWORD(self.ALL_ACCESS),False,DWORD(pid))

			if phandle:
				return phandle
			else:
				return self.GetLastError()
		else:
			print("Couldn't get the process ID!")
			return False
			

	def Read_UINT32(self, handle, addr):
		buffer = c_ulong(0)
		ret = self.ReadProcessMemory(handle,LPCVOID(addr),byref(buffer),sizeof(buffer),None)
		if (ret == 0):
			print("[+] ERROR: ReadProcessMemory Failed: ", self.GetLastError())
			print("[+] ERROR: Access of Address", addr, " failed")
			exit(1)
		return buffer.value
		

	def Read_UINT64(self, handle, addr):
		buffer = c_ulonglong()
		ret = self.ReadProcessMemory(handle, LPCVOID(addr), byref(buffer), sizeof(buffer), None)
		if (ret == 0):
			print("[+] ERROR: ReadProcessMemory Failed: ", self.GetLastError())
			print("[+] ERROR: Access of Address", addr, " failed")
			exit(1)
		return buffer.value


	def Read_String(self, handle, addr):
		buffer = c_ulonglong(0)
		ret = self.ReadProcessMemory(handle, LPCVOID(addr), byref(buffer), sizeof(buffer), None)
		if (ret == 0):
			print("[+] ERROR: ReadProcessMemory Failed: ", self.GetLastError())
			print("[+] ERROR: Access of Address", addr, " failed")
			exit(1)
		str = ""        
		while (1):
			c = c_char()
			ret = self.ReadProcessMemory(handle,buffer,byref(c),sizeof(c),None)
			if (ret == 0):
				print("[+] ERROR: ReadProcessMemory Failed: ", self.GetLastError())
				print("[+] ERROR: Access of Address", addr, " failed")
				exit(1)
			if (c.value == '\x00'):
				break
			str += c.value
			buffer.value += 1
		return str


	def Write_UINT64(self, handle, addr, value):
		buffer = c_ulonglong(value)
		ret = self.WriteProcessMemory(handle,LPCVOID(addr),byref(buffer),sizeof(buffer),None)
		if (ret == 0):
			print("[+] ERROR: WriteProcessMemory Failed: ", self.GetLastError())
			print("[+] ERROR: Access of Address", addr, " failed")
			exit(1)