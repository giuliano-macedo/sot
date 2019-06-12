from itertools import islice
from math import ceil
import struct
from . import BLOCKSIZE
from . import Blocks
class File:
	def new_block(blocks,name,data_generator,nbytes,indexes):
		header=lambda a,b,c,d,e,f:File.__write_header_block(a,b,c,d,e,f)
		link  =lambda a,b,c,d:    File.__write_link_block(a,b,c,d)
		if len(indexes)==1:
			header(blocks,indexes[0],name,nbytes,data_generator,0)
		else:
			header(blocks,indexes[0],name,nbytes,data_generator,indexes[1])
			for i in range(len(indexes)-2):
				link(blocks,indexes[i+1],data_generator,indexes[i+2])
			link(blocks,indexes[-1],data_generator,0)
		
	def __get_padded_data(generator,l):
		data=bytes(islice(generator,l))
		return data+(b"\0"*(l-len(data)))
	def __write_header_block(blocks,index,name,nbytes,data_generator,index_next):
		buffer=bytearray(BLOCKSIZE)
		Blocks.set_metadata(buffer,False,name)
		buffer[64:68]=struct.pack("I",nbytes)
		buffer[68:508]=File.__get_padded_data(data_generator,508-68)
		buffer[508:512]=struct.pack("I",index_next)

		blocks.set(index,buffer)
	def __write_link_block(blocks,index_now,data_generator,index_next):
		buffer=bytearray(BLOCKSIZE)
		buffer[0:508]=File.__get_padded_data(data_generator,508)
		buffer[508:512]=struct.pack("I",index_next)
		blocks.set(index_now,buffer)
	def __init__(self,name,index):
		self.name=name
		self.index=index
	def cat(blocks,index):
		buffer=blocks.get(index)
		print(buffer[68:508].decode("utf-8").rstrip("\0"),end="",flush=True)
		index=struct.unpack("I",buffer[508:512])[0]
		while index!=0:
			blocks.get(index,BLOCKSIZE,buffer)
			print(buffer[0:508].decode("utf-8").rstrip("\0"),end="",flush=True)
			index=struct.unpack("I",buffer[508:512])[0]
	def get_file_size(blocks,index):
		buffer=blocks.get(index)
		return struct.unpack("I",buffer[64:68])[0]
	def get_all_indexes(blocks,index):
		ans=[index]
		buffer=blocks.get(index)
		index=struct.unpack("I",buffer[508:512])[0]
		while index!=0:
			ans.append(index)
			blocks.get(index,BLOCKSIZE,buffer)
			index=struct.unpack("I",buffer[508:512])[0]
		return ans
	def cat_block(blocks,index,n):
		fs=File.get_file_size(blocks,index)
		nblocks=ceil(fs/BLOCKSIZE)
		if not (1<=n<nblocks+1):
			raise OSError("argumento invalido, n deve ser 1<=n<%i"%(nblocks+1))
		n-=1
		buffer=blocks.get(index)
		if n==0:
			return print(buffer[68:508].decode("utf-8").rstrip("\0"))
		index=struct.unpack("I",buffer[508:512])[0]
		i=1
		while index!=0:
			blocks.get(index,BLOCKSIZE,buffer)
			if n==i:
				return print(buffer[0:508].decode("utf-8").rstrip("\0"))
			index=struct.unpack("I",buffer[508:512])[0]
			i+=1
	def __str__(self):
		return "File(name=%s,indexinitial=%i)"%(self.name,self.index)
	def __repr__(self):
		return str(self)
	