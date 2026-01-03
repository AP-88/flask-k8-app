Flask Kubernetes & Docker Scalable App
A hybrid demonstration of a Flask application designed for both Local Docker Development and Production Kubernetes Orchestration.

📂 Project Structure
├── app/                    # Application Source Code
│   ├── app.py              # Flask app with Pod-aware logging
│   ├── requirements.txt    # Python dependencies
│   └── templates/          # HTML interfaces (Home & Logs)
├── k8/                     # Kubernetes Manifests (Production)
│   ├── pv.yaml             # Persistent Volume (HostPath)
│   ├── pvc.yaml            # Persistent Volume Claim
│   ├── deployment.yaml     # Flask Deployment (Probes, Mounts, Resources)
│   ├── service.yaml        # NodePort Service (Port 30001)
│   ├── hpa.yaml            # Autoscaling rules (CPU > 50%)
│   ├── configmap.yaml      # App environment variables
│   └── cronjob.yaml        # Automated 1-min Health Pinger
├── storage/                # Shared Persistent Data (Host Mount)
│   ├── access_log.txt      # Centralized logging file
│   └── data.txt            # Application input data
├── Dockerfile              # Shared Image definition
└── docker-compose.yaml     # Local Development for standalone container

🐳 Option 1: Local Development (Docker Compose)
If you want to run the application without Kubernetes, use the Docker Compose setup. 
This mimics the persistent storage behavior by mounting your local ./storage folder into the container.

Run the App:
Bash

docker-compose up -d

What happens: Docker builds the image and mounts the local /storage directory to the container's /storage path.
Access: Open http://localhost:5000 in your browser.

Verification: Check the ./storage/access_log.txt on your host machine,
You will see logs appearing immediately as you browse.

----------------------------------------------------------------------------

☸️ Option 2: Production Deployment (Kubernetes)
For high availability and autoscaling, deploy the manifests located in the k8/ directory.

1. Initialize Cluster & Storage
Bash

minikube addons enable metrics-server
kubectl apply -f k8/pv.yaml
kubectl apply -f k8/pvc.yaml
2. Deploy Infrastructure
Bash

kubectl apply -f k8/configmap.yaml
kubectl apply -f k8/deployment.yaml
kubectl apply -f k8/service.yaml
kubectl apply -f k8/hpa.yaml
kubectl apply -f k8/cronjob.yaml

📈 Feature Comparison:
Feature	Docker Compose (Local)	Kubernetes (Production)
Scaling	Manual (docker-compose up --scale)	Automatic via HPA
Persistence	Host Bind Mount	Persistent Volume (PV/PVC)
Health Check	Manual/Docker healthcheck	CronJob Pinger & Probes
Traffic	Simple Port Mapping	Load Balancer (Service)




📈 Feature Comparison
Feature		Docker Compose (Local)Kubernetes (Production)ScalingManual (docker-compose up --scale)Automatic via HPAPersistenceHost Bind MountPersistent Volume (PV/PVC)Health CheckManual/Docker healthcheckCronJob Pinger & ProbesTrafficSimple Port MappingLoad Balancer (Service)



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

