from core import FileSystem,File

#removeme
from core import FileTree,path
#
class Emulator:
	def __init__(self,filename):
		#self.fs=FileSystem(filename)
		self.cmdhooks={
			"pwd":self.pwd,
			"mkdir":self.mkdir,
			"touch":self.touch,
			"mv":self.mv,
			"rm":self.rm,
			"cd":self.cd,
			"ls":self.ls
		}
		# self.root=self.fs.getFileTree()
		self.root=FileTree()
		self.act=self.root
		self.pwd="/"
	def cli(self,*args):
		f=self.cmdhooks.get(args[0],None)
		if f==None:
			return "Command not found (%s)"%args[0]
		return f(*(args[1::]))
	# changeMe
	def __isdir(self,f):
		return type(f)==str
	#
	def cd(self,filename):
		p=self.root if path.parse(filename)[0]=="/" else self.act
	def ls(self,p=None):
		if p!=None:
			pass
			#todo
		return "\n".join(self.act.t.keys())


	def pwd(self):
		return self.pwd

	def mkdir(self,filename):
		# self.fs.mkdir(filename)
		#changeMe
		p=self.root if path.parse(filename)[0]=="/" else self.act
		assert p.get(filename)==None,FileExistsError(filename)
		p.set(filename,FileTree())
		#
	def touch(self,filename):
		#self.fs.touch(filename)
		#changeme
		p=self.root if path.parse(filename)[0]=="/" else self.act
		assert p.get(filename)==None,FileExistsError(filename)
		p.set(filename,File(path.parse(filename)[-1]))
		#
	def mv(self,f1,f2):
		# self.fs.mv(f1,f2)
		p=self.root if path.parse(f1)[0]=="/" else self.act
		f1v=p.get(f1)
		if(self.__isdir(f1v)):raise IsADirectoryError(f1)
		assert p.get(f2)==None,FileExistsError(f2)

		p.rm(f1)
		p.set(f2,f1v)

	def rm(self,filename):
		#self.fs.rm(f1)
		p=self.root if path.parse(filename)[0]=="/" else self.act
		p.rm(f1)


	def __del__(self):
		# del self.fs
		pass