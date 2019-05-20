import os,sys
sys.path.insert(0,os.path.abspath("../src"))
from core import FileTree,File
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
print(ft.get("d1").get("d11").get("f4"))

print(ft.get("f4"))
try:
	ft.get("f1/d1")
except Exception as e:
	print(e)
ft.set("file.txt",File("file.txt"))
ft.set("d1/file2.txt",File("file2.txt"))

print(ft)