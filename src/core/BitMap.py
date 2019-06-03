from bitarray import bitarray
class BitMap:
	def __init__(self,bytesbuffer):
		self.bits=bitarray()
		self.bits.frombytes(bytesbuffer)
	def getFreeBlock(self):
		l=len(self.bits)//64
		i64=0
		for i in range(l):
			if not self.bits[i:i+64].all():
				i64=i
				break
