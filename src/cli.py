from Emulator import Emulator
from argparse import ArgumentParser
import shlex

parser=ArgumentParser()
parser.add_argument("image",help="image file of the disk",type=str)
args=parser.parse_args()

emu=Emulator(args.image)
while True:
	user=shlex.split(input(":%s>"%emu.pwd))
	if len(user)==0:
		continue
	if user[0]=="exit":
		break
	try:
		ans=emu.cli(*user)
		print(ans) if ans!=None else print()
	#todo
	except NotADirectoryError as e:
		print("err: %s is not a directory"%e)
	except Exception as e:
		raise e
	#
del emu



