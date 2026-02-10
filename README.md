# Sample Python GKE App

A production-ready Python Flask application designed for deployment on Google Kubernetes Engine (GKE).

## Features

- Flask web application with RESTful API endpoints
- Health check and readiness probe endpoints for Kubernetes
- Containerized with Docker using best practices
- Complete Kubernetes manifests for GKE deployment
- Horizontal Pod Autoscaler (HPA) configuration
- Cloud Build configuration for CI/CD
- Environment-based configuration management

## Project Structure

```
.
├── app.py                  # Main Flask application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container image definition
├── .dockerignore         # Docker ignore patterns
├── .env.example          # Example environment variables
├── cloudbuild.yaml       # Cloud Build configuration
├── k8s/                  # Kubernetes manifests
│   ├── deployment.yaml   # Deployment and ConfigMap
│   ├── service.yaml      # LoadBalancer Service
│   └── hpa.yaml         # Horizontal Pod Autoscaler
└── README.md            # This file
```

## Prerequisites

- Python 3.11+
- Docker
- Google Cloud SDK (gcloud)
- kubectl
- A GCP project with GKE enabled
- Container Registry API enabled

## Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ramgopal-tummala/sample-python-gke-app.git
   cd sample-python-gke-app
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

   The app will be available at `http://localhost:8080`

## Docker Build and Run

1. **Build the Docker image:**
   ```bash
   docker build -t sample-python-gke-app:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8080:8080 sample-python-gke-app:latest
   ```

## GCP/GKE Deployment

### Step 1: Setup GCP Project

```bash
# Set your project ID
export PROJECT_ID=your-project-id
export REGION=us-central1
export CLUSTER_NAME=your-cluster-name

# Set the project
gcloud config set project $PROJECT_ID
```

### Step 2: Create GKE Cluster

```bash
# Create a GKE cluster
gcloud container clusters create $CLUSTER_NAME \
    --region $REGION \
    --num-nodes 3 \
    --machine-type n1-standard-2 \
    --enable-autoscaling \
    --min-nodes 2 \
    --max-nodes 5 \
    --enable-autorepair \
    --enable-autoupgrade

# Get credentials
gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION
```

### Step 3: Build and Push Docker Image

```bash
# Build and tag the image
docker build -t gcr.io/$PROJECT_ID/sample-python-gke-app:latest .

# Configure Docker to use gcloud as a credential helper
gcloud auth configure-docker

# Push to Container Registry
docker push gcr.io/$PROJECT_ID/sample-python-gke-app:latest
```

### Step 4: Deploy to GKE

```bash
# Update the deployment.yaml with your PROJECT_ID
sed -i "s/YOUR_PROJECT_ID/$PROJECT_ID/g" k8s/deployment.yaml

# Apply Kubernetes manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services
```

### Step 5: Access the Application

```bash
# Get the external IP
kubectl get service sample-python-app-service

# Wait for external IP to be assigned, then access:
# http://<EXTERNAL-IP>
```

## CI/CD with Cloud Build

### Setup Cloud Build Trigger

1. **Connect your repository to Cloud Build**

2. **Create a trigger:**
   ```bash
   gcloud builds triggers create github \
       --repo-name=sample-python-gke-app \
       --repo-owner=ramgopal-tummala \
       --branch-pattern="^main$" \
       --build-config=cloudbuild.yaml \
       --substitutions=_GKE_CLUSTER=$CLUSTER_NAME,_GKE_REGION=$REGION
   ```

3. **Manual build:**
   ```bash
   gcloud builds submit --config cloudbuild.yaml .
   ```

## API Endpoints

- `GET /` - Home endpoint with app information
- `GET /health` - Health check endpoint
- `GET /readiness` - Readiness probe endpoint
- `GET /api/data` - Sample GET endpoint
- `POST /api/data` - Sample POST endpoint

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `DEBUG` | Debug mode | `False` |
| `PORT` | Application port | `8080` |
| `APP_NAME` | Application name | `Sample Python GKE App` |
| `APP_VERSION` | Application version | `1.0.0` |
| `GCP_PROJECT_ID` | GCP project ID | - |
| `GCP_REGION` | GCP region | `us-central1` |
| `GKE_CLUSTER_NAME` | GKE cluster name | - |

## Monitoring and Logging

View logs in GCP:
```bash
# View application logs
kubectl logs -l app=sample-python-app --tail=100 -f

# View logs in Cloud Logging
gcloud logging read "resource.type=k8s_container AND resource.labels.cluster_name=$CLUSTER_NAME" --limit 50
```

## Scaling

The application includes HPA configuration for automatic scaling based on CPU and memory usage.

Manual scaling:
```bash
kubectl scale deployment sample-python-app --replicas=5
```

## Cleanup

```bash
# Delete Kubernetes resources
kubectl delete -f k8s/

# Delete GKE cluster
gcloud container clusters delete $CLUSTER_NAME --region $REGION

# Delete container images
gcloud container images delete gcr.io/$PROJECT_ID/sample-python-gke-app:latest
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
