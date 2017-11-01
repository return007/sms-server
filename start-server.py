from flask import Flask, request
import json

app = Flask(__name__)

config_params = None
try:
	with open("sms-server.conf", "r") as _file:
		config_params = json.load(_file)
except:
	print "Error: sms-server.conf missing!"
	exit()

username, password = None, None

try:
	username = config_params['username']
	password = config_params['password']
except:
	print "Error: username or password fields missing in sms-server.conf!"
	exit()

@app.route("/sendsms")
def send_sms():
	mobile_number = request.args.get('number')
	message = request.args.get('message')

	if mobile_number == None or message == None:
		return "Invalid request"

if __name__ == '__main__' :
	app.run(debug = True)