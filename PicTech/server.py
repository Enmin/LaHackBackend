from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import demjson
import simplejson
import FileUtil as fu
from PIL import Image
import Estimate as es
import base64

cases = ['/images/']


class Server(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	def do_HEAD(self):
		self._set_headers()

	# GET sends back a Hello world message
	def do_GET(self):
		self._set_headers()
		self.wfile.write(bytes(json.dumps({'hello': 'world', 'received': 'ok'}), encoding='utf-8'))

	# POST echoes the message adding a JSON field
	def do_POST(self):
		ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
		# refuse to receive non-json content
		if ctype != 'application/json':
			self.send_response(400)
			self.end_headers()
			return

		# read the message and convert it into a python dictionary
		data = dict()
		if self.path in cases:
			length = int(self.headers.get('content-length'))
			content = self.rfile.read(length).decode(encoding='utf-8')
			print(content)
			message = json.loads(content)
			data = self.handler(self.path, message)
			print(data)
			received = 'OK'
		else:
			received = 'Error'
		# add a property to the object, just to mess with data
		data['received'] = received

		# send the message back
		self._set_headers()
		self.wfile.write(bytes(json.dumps(data), encoding='utf-8'))

	def handler(self, command, data):
		if command == '/images/':
			# print(bytes(data['front']))
			# fu.writeToFile('resources/{0}-front.jpg'.format(data['username']), data['front'])
			# # imgFront = Image.open('resources/{0}-front.jpg'.format(data['username']))
			# # imgFront.save('resources/{0}-front.jpg'.format(data['username']), 'JPEG', quality=0.1)
			# fu.writeToFile('resources/{0}-side.jpg'.format(data['username']), data['side'])
			# # imgSide = Image.open('resources/{0}-side.jpg'.format(data['username']))
			# # imgSide.save('resources/{0}-side.jpg'.format(data['username']), 'JPEG', quality=0.1)
			# frontImage = 'resources/{0}-front.jpg'.format(data['username'])
			# sideImage = 'resources/{0}-side.jpg'.format(data['username'])
			frontImage = 'resources/demo2-front.jpg'
			sideImage = 'resources/demo2-side.jpg'
			estimate = es.Estimate(frontImage, sideImage, 180)
			return estimate.getGeneral()
		else:
			return {'Waist': '?', 'Chest': '?', 'Hip': '?'}

def run(server_class=HTTPServer, handler_class=Server, port=8030):
	server_address = ('127.0.0.1', port)
	httpd = server_class(server_address, handler_class)

	print('Starting httpd on port %d...' % port)
	httpd.serve_forever()


if __name__ == "__main__":
	run()