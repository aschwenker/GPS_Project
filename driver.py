
from functions import *

html = 'C:\Users\ASchwenker\Documents\GitHub\GPS_Project\index.html'

class App:
    directory_name = tempfile.mkdtemp()
    csvfilename    = str(uuid.uuid4())
    jsonfilename = str(uuid.uuid4())
    jsondestination = os.path.join(directory_name, jsonfilename)
    csvdestination = os.path.join(directory_name, csvfilename)
    @cherrypy.expose
    def index(self):
        """loads the index file"""
        return file(html)
        
    @cherrypy.expose
    def upload(self):
        """uploads csv from request,wrtites a temporary csv to random string name"""
        writer(self.csvdestination)

    @cherrypy.expose
    def geo(self):
        gpsroute(self.csvdestination,self.jsondestination)
        """used as a static geojson sample to test html geojson link load worked"""
        return file(self.jsondestination)

    @cherrypy.expose
    def generate(self, name):
        data = ProcessMobileData(str(name))
        return json.dumps(ReturnGeoJSON(data))


        

if __name__ == '__main__':
  cherrypy.quickstart(App(), '/', conf.config)

        



