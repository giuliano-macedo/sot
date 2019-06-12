from . import BLOCKSIZE
class Blocks:
	def __init__(self,f,offset,blockstotal):
		self.f=f
		self.offset=offset
		self.blockstotal=blockstotal
	def __moveToBlock(self,i):
		i+=self.offset
		if i<=0<self.blockstotal+1:
			raise IndexError()
		self.f.seek(i*BLOCKSIZE)
	def get(self,i,l=None,buffer=None):
		l=BLOCKSIZE if l==None else l
		buffer=bytearray(l) if buffer==None else buffer
		self.__moveToBlock(i)
		buffer[0:l]=self.f.read(l)
		return buffer
	def set(self,i,buffer):
		# print("writing block ",i)
		# print(buffer)
		self.__moveToBlock(i)
		ans=self.f.write(buffer)
		self.f.flush()
		return ans
	def get_metadata(buffer):
		flag=buffer[0]
		name=buffer[1:64].decode("utf-8").rstrip("\0")
		return flag==0,name
	def set_metadata(buffer,flag,name):
		flag=0 if flag==True else 255
		buffer[0]=flag
		name=name.encode("utf-8")
		l=len(name)
		if l>64:
			raise RuntimeError("nome do diretorio/arquivo é maior que 64")
		buffer[1:l+1]=name