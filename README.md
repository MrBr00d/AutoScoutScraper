# Car scraper
The aim of this project is to provide the setup of a batteries-included approach of webscraping. This means the docker compose file contains all that is needed for the scraping process. This project contains:
* An Apache Airflow environment to manage and schedule scraping jobs.
* A python DAG to scrape the Dutch `Autoscout24.nl` website.
* A postgres + adminer environment to store and access the database.
To expand this project you can contribute by adding a DAG + python script for a new website which contains the same columns as the provided DAG.
# Installation
This repo is as much pre-setup as possible however certain steps need to be taken in order to make this project work.
*This project requires [Docker](https://www.docker.com) to work.*
1. Clone this repo.
2. Rename `template.env` to `.env`.
3. Modify the `.env` file by changing the Airflow and postgreSQL passwords to something secure.
4. In the terminal run `sudo docker compose build` followed by `sudo docker compose up -d`. This will build and start the docker containers in deamon (background) mode.
5. Access the airflow installation by going to *IP_OF_THE_HOST_MACHINE:8080*. e.g. *https://172.0.0.1:8080* and logging in with your credentials.
6. Go to connections and add the postgres connection with connection id: `postgres_default`. *Host* is postgres and *port* is 5432.
7. Start and run the DAG. If successful this will now populate the database.
