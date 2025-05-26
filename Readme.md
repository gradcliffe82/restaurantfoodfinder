
### Description:
A web application that lets you query and find any open restaurants based on the current date and time, or date/time string.

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
  
### ETL process:
* The restaurant.csv file is loaded and processed as the container initializes.
* The shell script: init_app_data.sh is executed as the container starts, and it includes the following process:
  * The script will create a raw table called restaurants_raw, where it will copy the csv data.
  * It will then run the python file: etl_script.py and transform the data to json format.
  * It will run makemigrations and migrate to create the models.
  * It will load data from the raw table into the application table.
  * The script will only execute the etl process if the raw table is empty.
  * Finally, it will execute python manage.py runserver 0.0.0.0:8000


### To build container:

* Builds the django application image or docker file:
  * docker build --no-cache -t restaurant-finder . 

* Builds the docker-compose file:
  * docker compose up --build or docker compose up --build --force-recreate  