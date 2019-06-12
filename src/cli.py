from Emulator import Emulator
import shlex
import os
from argparse import ArgumentParser
from utils import nist_str_to_bytes

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
	try:
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
		except FileExistsError as e:
			print("erro: %s já existe"%e)
		except FileNotFoundError as e:
			print("erro: %s não encontrado"%e)
		except OSError as e:
			print("erro: %s"%e)
	except KeyboardInterrupt:
		print("\b\bexit")
		break
del emu #só por preucação



