import os
os.system("cls")


import memory, keyboard, time
from ctypes import *
from ctypes.wintypes import *
import functions as f


m = memory.Memory()

process = "sekiro.exe"

# Getting Base Address
pyHandle = m.GetProcessHandle(process, 1)
modulos = m.EnumModules(pyHandle)
BaseAddress = modulos[0]


# CHEATS

# ITEMS, SPIRITS AND SKILLPOINTS ALWAYS 10
ISS10Addr = 0xC257B0 + BaseAddress
ISS10Enabled = False # Current state (enabled/disabled)
ISS10_0 = b"\x89\x51\x08\xC3\xCC\xCC\xCC\xCC" # Disabled
ISS10_1 = b"\xC7\x41\x08\x0A\x00\x00\x00\xC3" # Enabled

# ITEMS DONT GET USED
INUAddr = 0x79E8DE + BaseAddress
INUEnabled = False # Current state (enabled/disabled)
INU_0 = b"\x8b\xd7\x48\x8b\xcb\xe8\xc8\x6e" # Disabled
INU_1 = b"\x8b\xd6\x48\x8b\xcb\xe8\xc8\x6e" # Enabled
#print(hex(INUAddr))



# Getting handle for reading and writting
cHandle = m.GetProcessHandle(process, 0)


# Checking if the cheats are enabled/disabled
ISS10Enabled = f.CheatStatus(cHandle, m.Read_UINT64(cHandle, ISS10Addr), ISS10_0)
INUEnabled = f.CheatStatus(cHandle, m.Read_UINT64(cHandle, INUAddr), INU_0)




Menu =  "\n                     Sekiro trainer v0.1\n"
Menu += "             Version of the game compatible = 1.02\n"
Menu += " **************************************************************\n"
Menu += " * Press F8 for INFINITE ITEMS AND SPIRITS.                   *\n"
Menu += " * Press F7 for ITEMS, SPIRITS AND SKILLPOINTS ALWAYS 10.     *\n"
Menu += " * Press F6 to clear the screen.                              *\n"
Menu += " * Press F5 to exit.                                          *\n"
Menu += " **************************************************************\n"
print(Menu)


while(True):	

	if keyboard.is_pressed("F5"):
		m.CloseHandle(cHandle)
		exit(1)

	if keyboard.is_pressed("F6"):
		os.system("cls")
		time.sleep(0.5)
		print(Menu)

	if keyboard.is_pressed("F7"): # ISS10
		if ISS10Enabled == True:
			buff0 = (c_ubyte * len(ISS10_0)).from_buffer_copy(ISS10_0)
			m.WriteProcessMemory(cHandle,LPCVOID(ISS10Addr),buff0,c_int(len(ISS10_0)),None)
			ISS10Enabled = False
			print(" Items, spirits and skillpoints always 10 DISABLED.")
			time.sleep(0.5)
		elif ISS10Enabled == False:
			buff1 = (c_ubyte * len(ISS10_1)).from_buffer_copy(ISS10_1)
			m.WriteProcessMemory(cHandle,LPCVOID(ISS10Addr),buff1,c_int(len(ISS10_1)),None)
			ISS10Enabled = True
			print(" Items, spirits and skillpoints always 10 ENABLED.")
			time.sleep(0.5)

	if keyboard.is_pressed("F8"): # INU
		if INUEnabled == True:
			buff0 = (c_ubyte * len(INU_0)).from_buffer_copy(INU_0)
			m.WriteProcessMemory(cHandle,LPCVOID(INUAddr),buff0,c_int(len(INU_0)),None)
			INUEnabled = False
			print(" Infinite Items and spirits DISABLED.")
			time.sleep(0.5)
		elif INUEnabled == False:
			buff1 = (c_ubyte * len(INU_1)).from_buffer_copy(INU_1)
			m.WriteProcessMemory(cHandle,LPCVOID(INUAddr),buff1,c_int(len(INU_1)),None)
			INUEnabled = True
			print(" Infinite Items and spirits ENABLED.")
			time.sleep(0.5)


	time.sleep(0.01)