from core import FileSystem
from flask import Flask,jsonify
from argparse import ArgumentParser
app=Flask(__name__)
@app.route("/webservice")
def webservice():
	fs=FileSystem(args.image)
	ans={
		"status":"ok",
		"bitarray":fs.bitmap.bitstr(),
		"allocset":list(fs.bitmap.allocblocks),
		"freeset": list(fs.bitmap.freeblocks),
		"diskpercentage":fs.bitmap.getPercentageFull()
	}
	return jsonify(ans)

@app.route("/")
def index():
	with open("web/index.html") as f:
		return f.read()
def fileExists(filename):
	with open(filename) as f:pass
	return filename
parser=ArgumentParser()
parser.add_argument("image",help="image file of the disk",type=fileExists)
args=parser.parse_args()

app.run()