from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
from urllib import parse

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):    
        
    def do_GET(self):
        print("GET REQUEST mathservice.py")
        params = self.getParams();
        if 'number' in params:
            #self.set_headers(200)
            print("number is " + params['number'])
            total = 0
            for x in range(0, int(params['number'])):
                total += x
            print('total ' + str(total))
            return total
        # Here, we'll fetch a 'number' parameter from the incoming GET request
        # We'll print the incoming request number to the console
        # Then, we'll perform an iterative calculation on it - summing all values less than or equal to the input
        # We'll then return the number
        
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