from Emulator import Emulator
import shlex
import os
from argparse import ArgumentParser
def nist_str_to_bytes(s):
	kmg={
		"k":1024**1,
		"m":1024**2,
		"g":1024**3,
		"t":1024**4,
		"p":1024**5
	}
	s=s.lower()
	if s[-1]!="b":
		raise TypeError()
	state=0
	n=""
	for l in s[:-1]:
		if l==" ":
			continue
		if state==0:
			if (not l.isdecimal()) and (not l=="."):
				n=float(n)
				state+=1
			else:
				n+=l
		if state==1:
			m=kmg.get(l,None)
			if m==None:
				raise TypeError()
			state+=1
			n*=m
		elif state==2:
			raise TypeError()
	return int(n)

parser=ArgumentParser()
parser.add_argument("image",help="image file of the disk",type=str)
parser.add_argument("--n",help="size in bytes of the new disk image",type=nist_str_to_bytes)
args=parser.parse_args()

if not os.path.isfile(args.image):
	if args.n==None:
		print("Erro: arquivo %s não existe, e parametro n não passado"%args.image)
		exit(-1)

	if args.n<=512:
		print("Erro: n tem que ser maior que 512 bytes")
		exit(-1)
	#touch
	with open(args.image,"w") as f:
		f.write("")

emu=Emulator(args.image,args.n)
while True:
	user=shlex.split(input("(emulador):%s>"%emu.pwd()))
	if len(user)==0:
		continue
	if user[0]=="exit":
		break
	try:
		ans=emu.cli(*user)
		if ans!=None:print(ans)
	#todo
	except NotADirectoryError as e:
		print("erro: %s não é um diretório"%e)
	except OSError as e:
		print("erro: %s"%e)
	except Exception as e:
		raise e
	#
del emu #só por preucação



