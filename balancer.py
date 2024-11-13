from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
from urllib import parse

hostName = "localhost"
serverPort = 1111
ports = ["8080","8081"]

class MyServer(BaseHTTPRequestHandler):    
        
    def do_GET(self):
        # Here, we'll get the input 'number' parameter first from the GET request
        # Then we'll open our skeleton HTML file and read it into a string
        # We'll replace the _NUM_ value in the HTML with our input number parameter
        # And we'll replace the _PORT_ with the first port in our ports list
        # We'll rotate the list around (for round robin), and then we'll send our html
        self.set_headers(200)
        # if self.getURI() == '/lab5':
        #     html = open("loadTester.html")
        #     htmlString = html.read()
        #     html.close()
        #     self.wfile.write(bytes(htmlString,"UTF-8"))
        
        params = self.getParams()
        print(params)
        if 'number' in params:
            print("number in params")
            # html = open("skeleton.html")
            # htmlString = html.read()
            # html.close()
            html = open("skeleton.html", 'r')
            htmlString = html.read()
            htmlString = htmlString.replace("_NUM_", params['number'])
            htmlString = htmlString.replace("_PORT_", ports[0])
            ports.append(ports.pop(0))
            self.wfile.write(bytes(htmlString, "UTF-8"))
            
        
    # Gets the query parameters of a request and returns them as a dictionary
    def getParams(self):
        output = {}
        queryList = parse.parse_qs(parse.urlsplit(self.path).query)
        for key in queryList:
            if len(queryList[key]) == 1:
                output[key] = queryList[key][0]
        return output
    
    def getURI(self):           
        return parse.urlsplit(self.path).path
    
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