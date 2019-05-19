from base64 import b64decode
import struct
class MasterBootRecord:
	def __init__(self,n,msg):
		#base64 of basecode.bin
		basecode=b64decode("vo586DYA6EEAMcC7AQC5AQCLFox8OdF1Br5ufOgdAJHoLgC+hXzoEwCR6CQA6BoAAdiTg8EBg/kOddr0UKw8AHQGtA7NEOv1WMO+iXzo7P/DUFNSMdK7CgD384XAdAPo7/+J0AQwtA7NEFpbWMNudW1lcm8gZXNjb2xoaWRvICAtLT4gACAsIAAKDQA=")
		basecode+=struct.pack("H",n)
		basecode+=bytes(msg,"ascii")
		basecode+=bytes('\0'*(510-len(basecode)),"ascii")
		basecode+=struct.pack("H",0xaa55)
		self.code=basecode
		
		with open("boot.bin","wb") as f:
			f.write(self.code)

MasterBootRecord(2,"Ola turma")