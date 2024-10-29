from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
from urllib import parse

hostName = "localhost"
serverPort = 1111
ports = [8081,8080]

class MyServer(BaseHTTPRequestHandler):    
        
    def do_GET(self):
        global skeletonOpened
        print("GET REQUEST balancer.py")
        
        if self.getURI() == '/lab5':
           self.set_headers(200)
           self.wfile.write(self.getURI().encode())
           html = open("loadTester.html")
           htmlString = html.read()
           html.close()
           self.wfile.write(bytes(htmlString, "utf-8"))      
           
        params = self.getParams()
        if 'number' in params:
            print("number is: " + params['number'])
            self.set_headers(200)
            html = open('skeleton.html')
            htmlString = html.read()
            htmlString = htmlString.replace("_NUM_", params['number'])
            htmlString = htmlString.replace("_PORT_", str(ports[0]))
            html.close()
            self.wfile.write(bytes(htmlString, "UTF-8"))

            
        # Here, we'll get the input 'number' parameter first from the GET request
        # Then we'll open our skeleton HTML file and read it into a string
        # We'll replace the _NUM_ value in the HTML with our input number parameter
        # And we'll replace the _PORT_ with the first port in our ports list
        # We'll rotate the list around (for round robin), and then we'll send our html
        
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

    def getURI(self):
         return parse.urlsplit(self.path).path
     
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