GPS Project 

Increasingly there is an interest to utilize sensors for monitoring and analyzing mobility. This project visualizes line segments generated from GPS traces via a web map. (This web app is inspired in part by the website mapmyrun.com)  

Directory Structure

main directory -- the core files used to launch the web app and enable functionality

static-- stores the css files for the web map

misc -- earlier implementations of the code

old -- files to soon delete 



Core Functionality

The web app will allow the used to either enter a file or enter a userid (which is used to access the user data from a database). These inputs will be used to create the line segments generated from the GPS points. The user will be able to hover the geojson to see information relating to speed and distance The user will be able download a copy of the geojson as well as be able to clear the cache of  geojson in the web app. 



Future Work

There several areas for advancing this project going forward. Hope to provide a detection of activity type (walk, run, or etc) along the segments using gyroscope data. Also, hope to provide animation along the routes that are generate for the segment. Hope to have the animation to move along the path in relation to the speed (similar to: http://zevross.com/blog/2014/09/30/use-the-amazing-d3-library-to-animate-a-path-on-a-leaflet-map/ ). All assistance and suggestions are welcome for advancing this project.
