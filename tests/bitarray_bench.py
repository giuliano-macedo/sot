from bitarray import bitarray
from time import time
from os import urandom
from argparse import ArgumentParser
def find1(l,bits):
	c=0
	for i in range(0,len(bits),l):
		if bits[i:i+l].all():
			c+=1
	return c
def findConstant(l,bits):
	c=0
	f64=bitarray()
	f64.frombytes(b"\xff"*(l//8))
	for i in range(0,len(bits),l):
		if bits[i:i+l]==f64:
			c+=1
	return c
def test(f,bits):
	start=time()
	ans=f(bits)
	return time()-start,ans
parser=ArgumentParser()
parser.add_argument("n",nargs="?",default=1000,type=int)
args=parser.parse_args()
n=args.n
print("test with %s bytes"%("{:,}".format(n)))
bytesbuffer=urandom(n)+(b"\xff"*8)
bits=bitarray()
bits.frombytes(bytesbuffer)


print("(64 bit) find with .all    : %lfs ans:%i"%test(find1,bits))
print("(64 bit) find with constant: %lfs ans:%i"%test(find2,bits))
print("( 8 bit) find with .all    : %lfs ans:%i"%test(find3,bits))
print("( 8 bit) find with constant: %lfs ans:%i"%test(find4,bits))
print("( 1 bit) find with .all    : %lfs ans:%i"%test(find5,bits))
print("( 1 bit) find with constant: %lfs ans:%i"%test(find6,bits))