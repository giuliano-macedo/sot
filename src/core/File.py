class File():
	def new_block(blocks,name,data_generator,indexes):
		raise RuntimeError("nao implementeado :(")
	def __init__(self,name,index):
		self.name=name
		self.index=index
	def __str__(self):
		return "File(name=%s,indexinitial=%i)"%(self.name,self.index)
	def __repr__(self):
		return str(self)
	