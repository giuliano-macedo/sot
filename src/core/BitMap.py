from bitarray import bitarray
class BitMap:
	def __init__(self,f,bitrange):
		self.f=f
		self.bits=bitarray()
		self.bitrange=bitrange
		
		t=self.f.tell()
		
		self.f.seek(self.bitrange[0])
		self.bits.fromfile(self.f,self.bitrange[1])
		
		self.f.seek(t)

		self.size=len(self.bits)

		self.freeblocks =set()
		self.allocblocks=set()

		for i,b in enumerate(self.bits):
			if b==0:
				self.freeblocks.add(i)
			else:
				self.allocblocks.add(i)
	def __update(self):
		t=self.f.tell()
		
		self.f.seek(self.bitrange[0])
		self.bits.tofile(self.f)
		
		self.f.seek(t)

	def alloc(self,n):
		assert 1<=n<self.size
		ans=[]
		for i in self.freeblocks:
			if len(ans)==n:
				break
			ans.append(i)
		if len(ans)!=n:
			raise OSError("Não tem espaço suficiente")
		for index in ans:
			self.bits[index]=1
			self.freeblocks.remove(index)
			self.allocblocks.add(index)
		self.__update()
		return ans
	def free(self,blockslist):
		for b in blockslist:
			assert b in self.allocblocks
		for b in blockslist:
			self.allocblocks.remove(b)
			self.freeblocks.add(b)
			self.bits[b]=0
		self.__update()
	def bitstr(self):
		return self.bits.to01()
	def getPercentageFull(self):
		return 100*(len(self.allocblocks)/self.size)
	def __bytes__(self):
		return self.bits.b.tobytes()