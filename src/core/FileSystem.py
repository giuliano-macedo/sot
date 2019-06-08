from . import BitMap
from math import ceil
import struct
def parseBlock(buffer):
	flag=buffer[0]
	if flag==0:#FileTree
	
	else:#File

class FileSystem:
	magic=b"\x00\x05\x0a" #05A
	blocksize=512

	def __init__(self,filename,disksize=None):
		self.f=open(filename,"r+b")
		temp=self.f.read(len(self.magic))
		if temp==b"":
			return __newDisk(disksize)
		if temp!=self.magic:
			raise TypeError("Arquivo de formato incorreto")
		self.disksize=struct.unpack("I",self.f.read(4))
		self.blockstotal=self.disksize//self.blocksize
		self.blocklocation=0
		self.bitmap=BitMap(self.f.read(self.blockstotal//8))
		self.updateBlockLocation()
		#seja lá onde eu esteja, vamo pro proximo bloco
		self.gotoBlock(self.blocklocation+1)
		self.scanDirectories()
	def updateBlockLocation(self):
		self.blocklocation=self.f.tell()//self.blocksize
	def readBlock(self):
		self.gotoBlock(self.blocklocation)
		self.blocklocation+=1
		return self.f.read(self.blocksize)
	def gotoBlock(self,n):
		self.blocklocation=n
		self.f.seek(self.blocklocation*self.blocksize)
	def __newDisk(self,disksize):
		disksize=int(disksize)
	def scanDirectories(self):
		obj=parseBlock(self.readBlock())
