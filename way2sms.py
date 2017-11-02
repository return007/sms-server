import requests

class sms:

	def __init__(self, username, password, proxies=None):

		# Using username and password, login to the way2sms server
		self.url = 'http://site24.way2sms.com/Login1.action?'
		self.cred = {
			'username': username, 
			'password': password
		}

		self.s = requests.Session()
		self.s.headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:55.0) Gecko/20100101 Firefox/55.0"
		
		self.proxyDict = proxies
		self.q = self.s.post(self.url, data = self.cred, proxies = self.proxyDict)
		self.loggedIn = False

		if self.q.status_code == 200:
			self.loggedIn = True

		self.jsid = self.s.cookies.get_dict()['JSESSIONID'][4:]

	def send(self, number, message):
		if len(message) > 139 :
			return {
				"status": "ERROR",
				"response": "Message length exceeded!"
			}

		if len(number) != 10 or (number[0] != '7' and number[0] != '8' and number[0] != '9'):
			return {
				"status": "ERROR",
				"response": "Number Invalid!"
			}

		self.form_data = { 
					'ssaction' : 'ss',
					'Token' : self.jsid,
			        'mobile' : number,       				 
			        'message' : message,
			        'msgLen' : '129'
       	}

		self.msg_url = 'http://site24.way2sms.com/smstoss.action'		
		self.q = self.s.post(self.msg_url, data=self.form_data, proxies=self.proxyDict)

		if self.q.status_code == 200:
			return {
				"status": "OK",
				"response": message
			}
		else:
			return {
				"status": "ERROR",
				"response": "Some Error Occurred!"
			}