#  coding: utf-8
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2021 Graeme Keates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):

        # Receive data from client
        self.data = self.request.recv(1024).strip()
        
        print(self.data)
        # Check for empty response
        # if len(self.data) == 0:
        #     self.request.sendall(bytearray('HTTP/1.1 400 Bad Request\r\nConnection: close', 'utf-8'))
        #     return
        request = self.data.split() 
        if (request[0].decode('utf-8')=='GET'):
            requestPath = request[1].decode('utf-8')
            path = './www' + requestPath
            if (os.path.exists('./www/'+os.path.abspath(requestPath))):
                fileName = 'index.html'
                if(os.path.isdir(path)):
                    if path[-1]=='/':
                        path+=fileName
                        file = open(path,"r")
                        content = file.read()
                        file.close()
                        fileType = requestPath.split('.')[-1].strip()
                        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/{}\r\n\r\n{}'.format(fileType, content)
                    else:
                        path+='/'+fileName
                        file = open(path,"r")
                        content = file.read()
                        file.close()
                        response = 'HTTP/1.1 301 Moved Permanently\r\nLocation: {}/\r\n\r\n<html>\r\n<head><title>301 Moved Permanently</title></head>\r\n<body>\r\n<h1>Moved Permanently</h1>\r\n</body>\r\n</html>'.format(requestPath)
        else:
            response = 'HTTP/1.1 404 Not Found\r\n'
        self.request.sendall(bytearray(response, 'utf-8'))



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()