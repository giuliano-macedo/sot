from core import FileSystem
from core import path
from utils import nist_str_to_bytes
import lorem
def lorem_gen(nbytes):
	state=0
	while True:
		if state==0:
			buffer=lorem.text().encode("utf-8")
			i=0
			state+=1
		if state==1:
			if i==len(buffer)-1:
				state=0
			yield buffer[i]
			i+=1
			nbytes-=1
		if nbytes==0:
			break

class Emulator:
	def __init__(self,filename,n):
		self.fs=FileSystem(filename,n)
		self.cmdhooks={
			"pwd":self.pwd,
			"mkdir":self.mkdir,
			"rm":self.rm,
			"cd":self.cd,
			"ls":self.ls,
			"lorem":self.lorem,
			"cat":self.cat,
			"fsize":self.get_file_size,
			"fblock":self.cat_block
		}
	def cli(self,*args):
		f=self.cmdhooks.get(args[0],None)
		if f==None:
			return "Commando não encontrado (%s)"%args[0]
		try:
			ans=f(*(args[1:]))
		except TypeError as e:
			if "required positional argument" in str(e):
				return "número incorreto de argumentos para o comando %s"%args[0]
			raise e
		return ans
	
	def cd(self,filename):
		self.fs.chdir(filename)
		
	def ls(self):
		return "\n".join([".",".."]+self.fs.get_topdir().get_children_name())

	def pwd(self):
		return self.fs.pwd()

	def mkdir(self,filename):
		self.fs.mkdir(filename)		
		
	def rm(self,filename):
		self.fs.rm(filename)
	def lorem(self,filename,nbytes):
		try:
			nbytes=nist_str_to_bytes(nbytes)
		except TypeError as e:
			raise OSError("formato incorreto para %s"%nbytes)
		self.fs.newfile(filename,lorem_gen(nbytes),nbytes)
	def cat(self,filename):
		self.fs.cat(filename)
		print()
	def get_file_size(self,filename):
		print("Tamanho do arquivo \"%s\" : %ib"%(filename,self.fs.get_file_size(filename)))
	def cat_block(self,filename,n):
		self.fs.cat_block(filename,int(n))
	