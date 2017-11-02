from flask import Flask, jsonify
from flask import request as rq
import json

import way2sms

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

proxies = None
try:
	proxies = config_params['proxy']
except:
	pass

q = way2sms.sms(username, password,proxies=proxies)

@app.route("/sendsms", methods=['GET'])
def send_sms():
	mobile_number = rq.args.get('number')
	message = rq.args.get('message')

	if mobile_number == None or message == None:
		return "Invalid request"

	numbers = mobile_number.split(",")

	response = []

	for num in numbers:
		response.append(q.send(num, message))

	return jsonify(response=response)

@app.route('/register', methods=['PUT'])
def register_user():
	print dir(rq)
	print rq.form
	print json.loads(rq.data)
	return "Hello World"

app.run(debug = True, host="0.0.0.0")