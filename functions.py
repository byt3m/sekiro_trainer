import os


def ByteArrayToLittleEndian(ByteArray):
	n = bytearray.fromhex('{:016x}'.format(ByteArray))
	return hex(int.from_bytes(n, "little"))


def ByteArrayToInt(ByteArray):
	return hex(int.from_bytes(ByteArray, "big"))


def CheatStatus(handle, GameValue, CheatValue):
	#print(ByteArrayToInt(CheatValue))
	#print(ByteArrayToLittleEndian(GameValue))
	if ByteArrayToLittleEndian(GameValue) == ByteArrayToInt(CheatValue):
		return False
	elif ByteArrayToLittleEndian(GameValue) == ByteArrayToInt(CheatValue):
		return True
	else:
		print("Couldn't check the state of the cheats.")
		os.system("pause")
		exit(1)	