from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
from urllib import parse

hostName = "localhost"
serverPort = 8081
ports = [8081,8080]

class MyServer(BaseHTTPRequestHandler):    
        
    def do_GET(self):
        global skeletonOpened
        print("GET REQUEST balancer.py")
        params = self.getParams()
        if 'number' in params:
            skeletonOpened = 1
            print("number is: " + params['number'])
            self.set_headers(200)
            html = open('skeleton.html')
            #html = html.read()
            #html = html.replace("_NUM_", params['number'])
            #html = html.replace("_PORT_", str(ports[0]))
            htmlString = html.read()
            htmlString = htmlString.replace("_NUM_", params['number'])
            htmlString = htmlString.replace("_PORT_", str(ports[0]))
            html.close()
            #self.wfile.write(bytes(html, "UTF-8"))
            #self.wfile.write(bytes(htmlString.replace("_NUM_", str(params['number'])), "utf-8"))
            #self.wfile.write(bytes(htmlString.replace("_PORT_", str(ports[0])), "UTF-8"))
            self.wfile.write(bytes(htmlString, "UTF-8"))
            total = 0
            for x in range(0, int(params['number'])):
                total += x
            print('total ' + str(total))
            ports.append(ports.pop(0))
            return total
            
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