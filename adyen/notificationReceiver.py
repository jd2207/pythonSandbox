"""
Very simple HTTP server for testing and record Adyen notifications. It customizes parent classes 
to customize receiving POST requests. Specifically:

	- always responds with "[accepted]"
	- records the received POST data in a file called NotificationsReceived.txt

Usage::
    notificationsReceiver.py [<port>]

    Then on the client side:

    Example 1:
    	curl -d "foo=bar&bin=baz" http://localhost[:<port>]
    
    This is appended to NotificationsReceived.txt:

    <timestamp>
    foo=bar&bin=baz
	--------------------------------

    Example 2:
    	curl -X POST --data '{ "somethingelse":"blah blah" { "other": "other"} }' http://localhost:8080

    This is appended to NotificationsReceived.txt:

    <timestamp>
	{ "somethingelse":"blah blah" { "other": "other"} }
	--------------------------------

"""


import SimpleHTTPServer, SocketServer, datetime


RECEIVED_TRACE = 'NotificationsReceived.txt'			# name of the file which records incoming notifications


class NotificationReceiver(SocketServer.TCPServer):

	def __init__(self, port=8080):
		self.port = port
		return SocketServer.TCPServer.__init__(self, ("", self.port), HTTPPostHandler)

	def start(self):
		print "Notification Receiving Server listening at port", self.port
		self.serve_forever()


class HTTPPostHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
			
	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself

		# output post_data to a file
		f = open(RECEIVED_TRACE, 'a')
		f.write( '%s\n%s\n--------------------------------\n\n' % (datetime.datetime.now(), post_data))
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

		self.wfile.write("[accepted]\n")



if __name__ == "__main__":
	server = NotificationReceiver()
	server.start()


