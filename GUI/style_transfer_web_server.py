#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import cherrypy
from cherrypy.lib import static

config = {
    'global' : {
        'server.socket_host' : '127.0.0.1',
        'server.socket_port' : 8080
    }
}


class App:

    @cherrypy.expose
    def check_output_ready(self):
        #needs to be changed to return ready or not or build in wait until ready
        return "Ready"

    @cherrypy.expose
    def confirm_selection(self, style="starry"):
        #if nothing selected assume starry
        #add in the code to save style on python side
        #return selected style as confirmation

        return style


    @cherrypy.expose
    def upload(self, ufile):
        # Either save the file to the directory where server.py is
        # or save the file to a given path:
        # upload_path = '/path/to/project/data/'
        upload_path = os.path.dirname(__file__)

        # Save the file to a predefined filename
        # or use the filename sent by the client:
        upload_filename = ufile.filename
        #upload_filename = 'saved.txt'

        upload_file = os.path.normpath(
            os.path.join(upload_path, upload_filename))
        size = 0
        with open(upload_file, 'wb') as out:
            while True:
                data = ufile.file.read(8192)
                if not data:
                    break
                out.write(data)
                size += len(data)
        out = '''
        File received.
        Filename: {}
        Length: {}
        Mime-type: {}
        ''' .format(ufile.filename, size, ufile.content_type, data)
        return out

    @cherrypy.expose
    def download(self):
        #change this to be directory on the server
        absDir='/Users/edina/Documents/BerkeleyHW/w251/finalproject/'        
        path = os.path.join(absDir, 'file.txt')
        return static.serve_file(path, 'application/x-download',
                                 'attachment', os.path.basename(path)) 
if __name__ == '__main__':
    cherrypy.quickstart(App(), '/', config)
