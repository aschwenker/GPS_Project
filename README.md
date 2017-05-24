Overview:
 
Increasingly, there is an interest to utilize sensors for monitoring and analyzing mobility. This project visualizes line segments generated from GPS traces via a web map. This web app is inspired by the desired to create an open source geovisualization tool that is able to provide useful insights for travel data. GPS data is very value for travel agencies and being about to use Web GIS to assess the patterns and events in travel information is crucial since this information can lead to great decision making.
 
Powerpoint: https://docs.google.com/presentation/d/1QPi1aH-0lawi2n0zIj8_4MDytogNLvCmdaqR5GyoRHw/edit?usp=sharing
 
Built With

Python (Cherrypy) was used to interact with the frontend and backend of this project. In addition, the cherrypy library was used for process web services request by the client. 

Postgres -- This database is used to stored the mobile data. As this project develop, this database will be connected to an mobile app that will receive smartphone users GPS traces.

Boot Strap responsive HTML, CSS and JS framework 

Leaflet -- Leaflet is an open-source JavaScript library for web mapping 

Carto -- the host of the tiles used to create the base map layer for the project
 

User Interface Explanation

There are several different option that a user is able to choose when first introduced to the site. Most of these options are located on the left side of the site. The first option is the upload widget that allows the user to navigate to the csv that they would like to use generate the geojson. The file is held temporarily on the cache.When the user clicks display GPS path will with then add a geojson map layer of the gps path.  The user can then choose to clear the layer or download the GeoJSON file.

Another way in which the user can load the geojson is by enter a userid that correspond to their mobile phone. This userid will be used to extract the data associated with that user id and a geojson map layer of their path is displayed. The user can hover over each line segment to view the enriched data relating to speed and distance that is stored in the properties of that geojson line segment. 
 
Future Work
 
There several areas for advancing this project going forward. Hope to provide a detection of activity type (walk, run, or etc) along the segments using gyroscope data. Also, hope to provide animation along the routes that are generate for the segment. Hope to have the animation to move along the path in relation to the speed. In addition, we will look to incorporate machine learning techniques into this application to better userstand which functionality users interact with on the site. We hope that results from such an approach will reveal more trends about how the design and performances of the site attracts users. In addition, this data could then used used to suggest the enabling and disabling of certain widgets of the site. An ultimate goal of this approach is to provide a customized and engaging application for user. In addition, future work will look at expanding the database functionality to host geolocated video and tweets. Being abke to host those datsets make provide important context about the purpose and social aspects related to users trip trajectories. All assistance and suggestions are welcome for advancing this project. 
 
Authors 
Anne Schwenker|
Lerone Savage |lerone.savage23@myhunter.cuny.edu
 
Acknowledgements
 
http://geniuscarrier.com/how-to-style-a-html-file-upload-button-in-pure-css/
https://stackoverflow.com/questions/26876695/uploading-a-file-in-ajax-to-cherrypy
http://leafletjs.com/examples/choropleth/
