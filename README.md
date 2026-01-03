Flask k8 App

A containerized Flask web application. 
This project is configured to run seamlessly using Docker and Docker Compose, or as K8s cluster app,
pulling the pre-built image from Docker Hub.


Quick Start

# To run it as stand alone docker container:
Prerequisites:
    Docker installed on your machine.

	Docker Compose (included with Docker Desktop).

Running the App:

1 -The docker-compose file will download the image from Docker hub, but if you want to download the image manually, 
please run: docker pull ap88/flask-k8-app:005

2 - unzip the attached folder and navigate into it, 
And run the docker-compose.yaml file with the following command: docker-compose up -d

3 - Access the application: Open your browser and navigate to http://localhost:5000

# To run it as K8s cluster
:

