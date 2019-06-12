from core import FileSystem
from flask import Flask,jsonify,send_from_directory
from argparse import ArgumentParser

# text: { name: "Parent node" },
# 		children: [
# 			{
# 				text: { name: "First child" }
# 			},
# 			{
# 				text: { name: "Second child" }
# 			}
# 		]
def gentree(fs):
	ans={}
	return ans
app=Flask(__name__)
@app.route("/webservice")
def webservice():
	try:
		fs=FileSystem(args.image)
		tree=gentree(fs)
		ans={
			"status":"ok",
			"bitarray":fs.bitmap.bitstr(),
			"allocset":list(fs.bitmap.allocblocks),
			"freeset": list(fs.bitmap.freeblocks),
			"diskpercentage":fs.bitmap.getPercentageFull(),
			"tree":tree
		}
		del fs
	except Exception as e:
		ans={"status":"err","msg":str(e)}

	return jsonify(ans)
@app.route('/<path:path>')
def send(path):
    return send_from_directory('web', path)


def fileExists(filename):
	with open(filename) as f:pass
	return filename
parser=ArgumentParser()
parser.add_argument("image",help="image file of the disk",type=fileExists)
args=parser.parse_args()

app.run()