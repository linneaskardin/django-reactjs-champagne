This is the Toolgate Maps project for the CPU group.

CHAMAPGNE-MASTER is the master branch of this repository. 

This is the file-structure of the project. Only some of the files are expalined explicitly. 
- django
    - djreact - has the stucture of a djang app. 
        templates - contains the templates for the fron-end
    - map - contains the map-page
        - management - contains scripts in the command file for uploading data or translating property borders between coordinate systems. The scripts are run by typing *python manage.py [scriptname]* in the terminal
        - models.py - conatins the models for the data displayed on the map
    - menuapp - has the structure of a react app and contains the creation of the navigation bar. 


References to the code:

Merge between Django and React was done with the help from: 
https://github.com/mbrochh/django-reactjs-boilerplate

Navigation bar was created with Bootstrap with the help from: 
https://getbootstrap.com/docs/4.0/components/navbar/

Translation of coordinates in load_data was made with help from:
http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/ 

The merge of multidimensional dictionaries in load_data was made with help from:
https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression

The login funciton and the sign up function was made with help from:
https://wsvincent.com/django-user-authentication-tutorial-login-and-logout/
and 
https://wsvincent.com/django-user-authentication-tutorial-signup/

Map marker icons are taken from:
http://map-icons.com

The map is from:
https://developers.google.com/maps/documentation/javascript

The search box of the map is from:
https://developers.google.com/maps/documentation/javascript/examples/places-searchbox

The geolocation function in index was made with help from:
https://developers.google.com/maps/documentation/javascript/geolocation
