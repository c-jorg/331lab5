from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
from urllib import parse
import uuid

hostName = "0.0.0.0"
serverPort = 80
address = uuid.getnode()
print("File running")

class MyServer(BaseHTTPRequestHandler):    
        
    def do_GET(self):
        # self.set_headers(200)
        # self.wfile.write("the page has loaded".encode("utf-8"))
        # Here, we'll fetch a 'number' parameter from the incoming GET request
        # We'll print the incoming request number to the console
        # Then, we'll perform an iterative calculation on it - summing all values less than or equal to the input
        # We'll then return the number
        params = self.getParams()
        if 'number' in params:
            try:
                output = 0
                for x in range(int(params['number']) + 1):
                    output += x
                print(output)
                self.set_headers(200)
                self.wfile.write(f"<h2>Trangular number: {output}, My Address: {address}</h2>".encode("utf-8"))
            except:
                self.set_headers(400)
                self.wfile.write("something bad happened".encode("utf-8"))
        else:
            self.set_headers(400)
            self.wfile.write("no number".encode("utf-8"))
        
    # Gets the query parameters of a request and returns them as a dictionary
    def getParams(self):
        output = {}
        queryList = parse.parse_qs(parse.urlsplit(self.path).query)
        for key in queryList:
            if len(queryList[key]) == 1:
                output[key] = queryList[key][0]
        return output
    
    # Set the HTTP status code and response headers
    def set_headers(self, responseCode):
        self.send_response(responseCode)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', "*")
        self.send_header('Access-Control-Allow-Headers', "*")
        self.end_headers()

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except:
        webServer.server_close()
        print("Server stopped.")
        sys.exit()
    webServer.server_close()
    print("Server stopped.")
    sys.exit()