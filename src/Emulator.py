from core import FileSystem
from core import path

class Emulator:
	def __init__(self,filename,n):
		self.fs=FileSystem(filename,n)
		self.cmdhooks={
			"pwd":self.pwd,
			"mkdir":self.mkdir,
			"touch":self.touch,
			"mv":self.mv,
			"rm":self.rm,
			"cd":self.cd,
			"ls":self.ls
		}
	def cli(self,*args):
		f=self.cmdhooks.get(args[0],None)
		if f==None:
			return "Command not found (%s)"%args[0]
		return f(*(args[1::]))
	
	def cd(self,filename):
		course=path.parse(filename)
		backup=self.fs.stack
		try:
			if course[0]=="":
				while len(self.fs.stack)!=1:
					self.fs.chdir("..")
				course.pop(0)
			for c in course:
				self.fs.chdir(c)
		except Exception as e:
			self.fs.stack=backup
			raise e
	def __cdIfNeeded(self,course,removelast):
		course=path.split(course)
		if removelast:
			course.pop()
		self.cd(path.join(course))

	def ls(self,course=None):
		if course!=None:
			backup=self.fs.stack
			__cdIfNeeded(course)
			items=self.fs.get_topdir().get_children_name()
			self.fs.stack=backup
		else:
			items=self.fs.get_topdir().get_children_name()
		return "\n".join([".",".."]+items)

	def pwd(self):
		return self.fs.pwd()

	def mkdir(self,filename):
		backup=self.fs.stack
		self.__cdIfNeeded(filename,True)
		self.fs.mkdir(path.split(filename)[-1])		
		self.fs.stack=backup
		
	def touch(self,filename):
		raise RuntimeError("todo")
	def mv(self,f1,f2):
		raise RuntimeError("todo")
	def rm(self,filename):
		raise RuntimeError("todo")
	