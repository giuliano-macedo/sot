from . import path
from . import File
class FileTree:
	def __init__(self,t=None,name=None,parent=None):
		self.t={} if t==None else t
		self.name=name if name!=None else ""
		if parent!=None:
			if type(parent)!=FileTree:raise TypeError("parent must be FileTree")
			self.t[".."]=parent
		else:
			self.t[".."]=None
		# self.t["."]=self
	def __traverse(self,p):
		ans=self
		for t in p[:-1]:
			ans=ans.t.get(t,None)
			if type(ans)!=FileTree:raise NotADirectoryError(ans.name)
		return ans
	def set(self,k,v):
		p=path.parse(k)
		act=self.__traverse(p)
		if(type(v)==FileTree):
			v.t[".."]=act
			v.name=p[-1]
		act.t[p[-1]]=v
	def get(self,f):
		p=path.parse(f)
		act=self.__traverse(p)
		return act.t.get(p[-1],None)
	def pathName(self):
		ans=[]
		aux=self
		while(aux!=None):
			ans.append(aux.name)
			aux=aux.t[".."]
		return path.join(ans[::-1])
	def __str__(self):
		return "FileTree:(%s)"%str(self.t)
	def __repr__(self):
		return str(self)