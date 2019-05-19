from Emulator import Emulator
from argparse import ArgumentParser

#todo
def arg_splitter(s):
	return s.split(" ")
#

parser=ArgumentParser()
parser.add_argument("f",help="img of the disk",type=str)
args=parser.parse_arguments()

emu=Emulator(args.f)
while True:
	user=arg_splitter(input(":%s>"%emu.pwd))
	if len(user)==0:
		continue
	if user[0]=="exit":
		break
	try:
		print(emu.cli(user))
	#todo
	except Exception as e:
		print(e)
	#
del emu



