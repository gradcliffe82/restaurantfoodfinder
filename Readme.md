
### Description:
A web application that lets you to query and find any open restaurants based on the current date and time.

### File contents:
* /data - contains the restaurant.csv file.
* /module/etl_script.py - a python etl script. Reads from a raw table and transforms data into json.
* /restaurantfinder - app.
* /sql - contains sql scripts for table creation and other queries.
* /static - contains JS files and CSS files
* /templates - base html file for web page
* .env - environment file used in docker-compose.yml
* Dockerfile - application image
* init_app_data.sh - shell script which is used to create a raw table to load the csv file, perform the etl process and runs django.
  
### ETL process
* The csv file gets loaded as the container initializes.
* The shell script, init_app_data.sh will run to create the raw table where it will load the csv file.
* The script will run the python file: etl_script.py and transform the data to json format.
* The script will load it to the application model.


### To build container

* Builds the django application image or docker file
docker build --no-cache -t restaurant-finder . 

* Builds the docker-compose file.
docker compose up --build --force-recreate  