from . import path
from . import File
from . import BLOCKSIZE
from . import Blocks
import struct

class FileTree:
	def new_block(blocks,name,index):
		buffer=bytearray(BLOCKSIZE)
		Blocks.set_metadata(buffer,True,name)
		blocks.set(index,buffer)
	def __init__(self,blocks,index):
		self.blocks=blocks
		self.index=index
		self.children=dict()#name->(isdir,index)
		
		buffer=self.blocks.get(index)
		isdir,self.name=Blocks.get_metadata(buffer)
		if not isdir:
			raise TypeError("bloco de formato incorreto")
		for i in range(64,len(buffer),4):
			index=struct.unpack("I",buffer[i:i+4])[0]
			if index==0:
				break
			isdir,name=Blocks.get_metadata(self.blocks.get(index,64))
			self.children[name]=(isdir,index)
	def get_children_name(self):
		return list(self.children.keys())
	def get(self,name):
		ans=self.children.get(name,None)
		if ans==None:
			return ans
		return {"isdir":ans[0],"index":ans[1]}
	def __add(self,name,isdir,index):
		buffer=self.blocks.get(self.index)
		for i in range(64,len(buffer),4):
			aux=struct.unpack("I",buffer[i:i+4])[0]
			if aux==0:
				#update on block list of indexes
				buffer[i:i+4]=struct.pack("I",index)
				self.blocks.set(self.index,buffer)
				#
				self.children[name]=(isdir,index)
				return
		raise RuntimeException("Limite de 112 itens alcançado")
	def add_dir(self,name,index):
		self.__add(name,True,index)
		FileTree.new_block(self.blocks,name,index)
	def add_file(self,name,data_generator,indexes):
		self.__add(name,False,indexes[0])
		File.new_block(self.blocks,name,data_generator,indexes)

	def __str__(self):
		return "FileTree:(name=%s,index=%s)"%(self.name,self.index)
	def __repr__(self):
		return str(self)