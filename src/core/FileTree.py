import path
from File import File
class FileTree:
	def __init__(self,t=None,parent=None):
		self.t={} if t==None else t
		if parent!=None:
			assert type(parent)==FileTree,"parent must be FileTree"
			self.t[".."]=parent
		# self.t["."]=self
	def __traverse(self,p):
		ans=self
		for t in p[:-1]:
			ans=ans.t[t]
			assert type(ans)==FileTree,"Impossible to traverse"
		return ans
	def set(self,k,v):
		p=path.parse(k)
		act=self.__traverse(p)
		act.t[p[-1]]=v
	def get(self,f):
		p=path.parse(f)
		act=self.__traverse(p)
		return act.t.get(p[-1],None)

	def __str__(self):
		return "FileTree:(%s)"%str(self.t)
	def __repr__(self):
		return str(self)
if __name__=="__main__":
	ft=FileTree({
		"f1":File("F1"),
		"f2":File("F2"),
		"d1":FileTree({
			"f3":File("F3"),
			"d11":FileTree({
					"f4":File("F4")
				})
			})
		})
	print(ft.get("d1"))
	print(ft.get("d1/d11"))

	print(ft.get("f1"))
	print(ft.get("d1/f3"))
	print(ft.get("d1/d11/f4"))

	print(ft.get("f4"))
	try:
		ft.get("f1/d1")
	except Exception as e:
		print(e)
	ft.set("file.txt",File("file.txt"))
	ft.set("d1/file2.txt",File("file2.txt"))

	print(ft)

