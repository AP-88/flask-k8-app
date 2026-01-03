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
docker-compose up -d

What happens: Docker builds the image and mounts the local /storage directory to the container's /storage path.
Access: Open http://localhost:5000 in your browser.

Verification: Check the ./storage/access_log.txt on your host machine,
You will see logs appearing immediately as you browse.

----------------------------------------------------------------------------

☸️ Option 2: Production Deployment (Kubernetes)
For high availability and autoscaling, deploy the manifests located in the k8/ directory.

1. Initialize Cluster & Storage:

minikube addons enable metrics-server
kubectl apply -f k8/pv.yaml
kubectl apply -f k8/pvc.yaml

3. Deploy Infrastructure:

kubectl apply -f k8/configmap.yaml
kubectl apply -f k8/deployment.yaml
kubectl apply -f k8/service.yaml
kubectl apply -f k8/hpa.yaml
kubectl apply -f k8/cronjob.yaml

📈 Feature Comparison:
Feature			  Docker Compose (Local)				      Kubernetes (Production)
Scaling			  Manual (docker-compose up --scale)	Automatic via HPA
Persistence		Host Bind Mount						          Persistent Volume (PV/PVC)
Health Check	Manual/Docker healthcheck			      CronJob Pinger & Probes
Traffic			  Simple Port Mapping					        Load Balancer (Service)

📝 Key Components Explained
The /storage Strategy
The application is coded to look for access_log.txt in /storage.
- In Docker Compose, this is a direct bind-mount to your project folder.
- In Kubernetes, this is a Persistent Volume Claim mapped to the same host path. 
This ensures that whether you are developing locally or running in a cluster, your logs are always preserved and centralized.

📊 Operations & Testing (K8s)
Access the Application:

minikube service flask-k8-app-service --url

Home (/): Displays content from data.txt.
Logs (/log): Displays real-time access logs.

Testing the Autoscaler
To simulate high traffic and watch the HPA scale the deployment from 2 to 5 or more replicas, run:

kubectl run load-generator --rm -it --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://flask-k8-app-service:5000; done"

Monitor the status in a separate window:

kubectl get hpa flask-k8-app-hpa -w


Monitoring Health Checks
The flask-health-pinger CronJob runs every minute. 
It pings the /health endpoint and appends the HTTP status code to /storage/access_log.txt. 
You can view these entries directly on the /log page of the web app.

Cleanup
- Docker: docker-compose down
- Kubernetes: kubectl delete -f k8/

