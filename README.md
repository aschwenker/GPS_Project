GPS Project 
 
Increasingly there is an interest to utilize sensors for monitoring and analyzing mobility. This project visualizes line segments generated from GPS traces via a web map. Geovisuliaztion encompases the field of using geographic tools to present detail information about data. As more attempts are being made to analyze the huge volumes of data, there is a great push by the commercial and open source communities to develop methods and approaches that provide value analysis of spatial data (see IBM Watson and Boundless). This web app is inspired by the desired to create an open source tool that is able to provide useful, nuanced information involving travel data. GPS data is very value for travel agencies and being about to use Web GIS to assess the patterns and events in travel information is crucial since this information can lead to improved decision making. This project was also inspired in part by the website mapmyrun.com, a website that that maps the GPs trajectory of cyclists.  
 
Power Point Link
 
Directory Structure -- add script / function ---> I provide example code here for calling the app --have it in my function.py 
 
List the name of the in house functions & functional descriptions
Driver.py 
Included functions :
Index -- returns index.html
Upload -- sends HTTP POST and writes temp csv of files received
Geo -- calls gpsroute which enriches the csv data and writes the temporary geojson file then the geo function returns that geojson
 
Functions.py
Included Functions & Descriptions:
Writer - writes csv from http get request
isTimeFormat -- takes datetime in and determines time format of csv time field
Haversine_np -- takes two lat lon pairs in, formatted as a tuple ((x,y),(x,y)) and finds the great circle distance between, simulates across surface distance. Returns distance between in miles
gpsroute -- takes in csv and json file paths, reads csv, writes list of ((x,y),time) sorts based on time, iterates over this list to create line segments, a dictionary is written for each line segment with lat,lon and properties. Each dictionary is appended to a features list, this list is the body array of what will be the GeoJSON file. A temp geojson is written
Config.py
Sets cherrypy configurations
 
 
 
 
 
main directory -- the core files used to launch the web app and enable functionality
 
static-- stores the css files for the web map
 
misc -- earlier implementations of the code
 
old -- files to soon delete 
 
Built With
Python (Cherrypy) -- Python was used to interact with the frontend and backend of this project. In addition, the cherrypy library was used for process web services request by the client. 
Postgres -- This database is used to stored the mobile data. As this project develop, this database will be connected to an mobile app that will receive smartphone users GPS traces..
Boot Strap responsive HTML, CSS and JS framework 
Leaflet -- Leaflet is an open-source JavaScript library for web mapping 
Carto -- the host of the tiles used to create the base map layer for the project
 
 
 
 
Core Functionality
 
The index html file structures the website and the styleSheet.css defines the style of the layout. The resulting setup will look similar to the image that is below:
 

User Interface Explanation
There are several different option that a user is able to choose when first introduced to the site. Most of these options are located on the left side of the side. The first option is the upload widget that allows the user to navigate to the csv that they would like to use generate the geojson. The file is held temporarily on the cache. 
When the user clicks display GPS path will with then add a geojson map layer of the gps path.  The user can then choose to clear the layer or download the GeoJSON file.
Another way in which the user can load the geojson is by enter a userid that correspond to their mobile phone. This userid will be used to extract the data associated with that user id from the last 2 hours and a geojson map layer of their path is displayed. 
The user can hover over each line segment to view the enriched data relating to speed and distance that is stored in the properties of that geojson line segment. 
 
Future Work
 
There several areas for advancing this project going forward. Hope to provide a detection of activity type (walk, run, or etc) along the segments using gyroscope data. Also, hope to provide animation along the routes that are generate for the segment. Hope to have the animation to move along the path in relation to the speed (similar to here ). In addition, we will look to incorporate machine learning techniques into this application to better userstand which functionality users interact with on the site. We hope that results from such an approach will reveal more trends about how the design and performances of the site attracts users. In addition, this data could then used used to suggest the enabling and disabling of certain widgets of the site. An ultimate goal of this approach is to create a tracking ecosystems that provides a customized and engaging application for user. In addition, future work will look at expanding the database functionality to host geolocated video and tweets data. Being abke to host these datsets make provide important context about the purpose and social aspects related to these trio trajectories. Herein, the benefits of a open sourced project can be utilzed  All assistance and suggestions are welcome for advancing this project. 
 
Authors 
Anne Schwenker
Lerone Savage
 
Acknowledgements
 
http://geniuscarrier.com/how-to-style-a-html-file-upload-button-in-pure-css/
https://stackoverflow.com/questions/26876695/uploading-a-file-in-ajax-to-cherrypy
http://leafletjs.com/examples/choropleth/
