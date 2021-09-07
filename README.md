# yamdb_final
![yamdb workflow](https://github.com/pochtennov/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)

This is my study project where I work with docker/docker-compose.

It's deployed here: https://pochtennov.com/redoc


Steps to set everything up locally:

1. To build and start docker container of the project:
``make build``


2. To apply migrations and collect static files for nginx server:
``make setup``


3. (Optional step) Add fixture data to the database:
``make add-fixtures``


4. Create Super User (SU):
``make createsu``


After all these steps are done the u can access the admin panel via the following link: 
``http://127.0.0.1/admin``

Also you can get documentation regarding API endpoints here:
``http://127.0.0.1/redoc``

6. To stop all running containers:
``make stop``


