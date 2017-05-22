
import os
from os.path import abspath
import cherrypy
import shutil
import tempfile
import uuid
from Modules import gpsroute
current_dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
config = {
  'global' : {
    'server.socket_host' : '127.0.0.1',
    'server.socket_port' : 8080,
    'server.thread_pool' : 8,
    'server.environment' : "production",
    'engine.autoreload_on' : True,
    'engine.autoreload_frequency' : 60
    },
    '/':{
  'tools.staticdir.root' : current_dir
    },
    '/static':{
    'tools.staticdir.on' : True,
    'tools.staticdir.dir': 'static',
    },
}

def writer(csvdestination):
    with open(csvdestination, 'wb') as f:
        shutil.copyfileobj(cherrypy.request.body, f)

class App:
    directory_name = tempfile.mkdtemp()
    csvfilename    = str(uuid.uuid4())
    jsonfilename = str(uuid.uuid4())
    jsondestination = os.path.join(directory_name, jsonfilename)
    csvdestination = os.path.join(directory_name, csvfilename)
    @cherrypy.expose
    def index(self):
        """loads the index file"""
        return file('C:/Users/ASchwenker/Documents/GitHub/GPS_Project/index.html')
        
    @cherrypy.expose
    def upload(self):
        """uploads csv from request,wrtites a temporary csv to random string name"""
        writer(self.csvdestination)

    @cherrypy.expose
    def userinput(self,unique):    
        """user provides unique string to access their db data"""
    @cherrypy.expose
    def geo(self):
        gpsroute(self.csvdestination,self.jsondestination)
        """used as a static geojson sample to test html geojson link load worked"""
        return file(self.jsondestination)


        

if __name__ == '__main__':
  cherrypy.quickstart(App(), '/', config)

        



