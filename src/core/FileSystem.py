from . import BitMap
from . import Blocks
from . import BLOCKSIZE
from . import FileTree
from . import File
from . import path
from collections import deque
from math import ceil
import struct

class FileSystem:
	magic=b"\x00\x05\x0a" #05A
	def __newDisk(self,disksize):
		assert disksize!=None
		zeroes=bytes(512)
		for i in range(0,disksize,512):
			self.f.write(zeroes)
		if (disksize%512)!=0:
			self.f.write(zeroes[:disksize%512])
		self.f.seek(0)
		self.f.write(self.magic)
		self.f.write(struct.pack("I",disksize))
		self.f.write(b'\x80')#bitarray([1,0,0,0,0,0,0,0]).tobytes()
		self.f.seek(0)
		
	def __init__(self,filename,disksize=None):
		self.f=open(filename,"r+b")
		temp=self.f.read(len(self.magic))
		if temp==b"":
			self.__newDisk(disksize)
			temp=self.f.read(len(self.magic))
		if temp!=self.magic:
			raise TypeError("Arquivo de formato incorreto")
		self.disksize=struct.unpack("I",self.f.read(4))[0]
		self.blockstotal=self.disksize//BLOCKSIZE
		self.bitmap=BitMap(self.f,(self.f.tell(),self.blockstotal//8))
		offset=(sum(self.bitmap.bitrange)//BLOCKSIZE)+1
		self.blocks=Blocks(self.f,offset,self.blockstotal)

		self.stack=deque([FileTree(self.blocks,0)])
	def get_topdir(self):
		return self.stack[-1]
	def get_root(self):
		return self.stack[0]
	def chdir(self,name):
		if name==".":
			return
		if name=="..":
			self.stack.pop()
			return
		todir=self.get_topdir().get(name)
		if todir==None:
			raise FileNotFoundError()
		if not todir["isdir"]:
			raise NotADirectoryError()
		self.stack.append(FileTree(self.blocks,todir["index"]))
	def pwd(self):
		return path.join([ft.name for ft in self.stack])
	def mkdir(self,name):
		actdir=self.get_topdir()
		if actdir.get(name)!=None:
			raise FileExistsError()
		actdir.add_dir(name,*self.bitmap.alloc(1))
	def newfile(self,name,data_generator):
		actdir=self.get_topdir()
		if actdir.get(name)!=None:
			raise FileExistsError()
		freeblocks=self.bitmap.alloc(ceil(len(data_generator)/BLOCKSIZE))
		actdir.add_file(name,data_generator,freeblocks)
	def __del__(self):
		self.f.close()



