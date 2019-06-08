from bitarray import bitarray
class BitMap:
	def __init__(self,bytesbuffer):
		self.bits=bitarray()
		self.bits.frombytes(bytesbuffer)
		self.size=len(self.bits)
	def __get(self,n,aloc):
		assert 1<=n<=self.size
		ans=[]
		i=-1
		while i<self.size and len(ans)!=n:
			try:
				i=self.bits.index(0,i+1)
				if aloc==True:
					self.bits[i]=1
				ans.append(i)
			except ValueError:
				break
		return ans
	def getFreeBlocks(self,n):
		return self.__get(n,False)
	def alocBlocks(self,n):
		return self.__get(n,True)
	def freeBlocks(self,blockslist):
		for b in blockslist:
			self.bits[b]=0
	def bitstr(self):
		return self.bits.to01()
	def getPercentageFull(self):
		return 100*(self.bits.count(1)/self.size)
	def __bytes__(self):
		return self.bits.b.tobytes()