# GKE Deployment Guide

## What's Configured

### GCP Settings
- **Project ID:** deployment-487002
- **Cluster Name:** sample-gke-cluster
- **Region:** us-central1
- **Container Registry:** gcr.io/deployment-487002

### GitHub Secrets (Already Added)
- ✅ `GCP_PROJECT_ID`
- ✅ `GCP_SA_KEY`
- ✅ `GKE_CLUSTER_NAME`
- ✅ `GKE_REGION`

## Deployment Workflow

The GitHub Actions workflow automatically:

1. **Builds** Docker image from your code
2. **Pushes** to Google Container Registry (GCR)
3. **Deploys** to GKE cluster
4. **Updates** application with zero downtime

### Triggers
- Push to `testbranch`
- Pull request to `testbranch`

## What Gets Deployed

- **Deployment:** 3 replicas with health checks
- **Service:** LoadBalancer (external access)
- **HPA:** Auto-scaling (2-10 pods based on CPU/memory)

## After Deployment

### Get External IP
```bash
kubectl get service sample-python-app-service
```

Wait for EXTERNAL-IP to appear (may take 2-3 minutes).

### Access Your App
```bash
http://<EXTERNAL-IP>/
http://<EXTERNAL-IP>/health
http://<EXTERNAL-IP>/api/info
http://<EXTERNAL-IP>/api/metrics
```

### Monitor Deployment
```bash
# Watch deployment status
kubectl get deployments -w

# View pods
kubectl get pods

# View logs
kubectl logs -l app=sample-python-app --tail=100 -f

# Check service
kubectl get svc sample-python-app-service
```

### Scaling
```bash
# Manual scaling
kubectl scale deployment sample-python-app --replicas=5

# Check HPA
kubectl get hpa
```

## Troubleshooting

### Check workflow logs
https://github.com/ramgopal-tummala/sample-python-gke-app/actions

### Common issues

**Image pull errors:**
```bash
# Verify image exists
gcloud container images list --repository=gcr.io/deployment-487002
```

**Pod not starting:**
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Service no external IP:**
```bash
# Check service
kubectl describe service sample-python-app-service

# May take 2-3 minutes for LoadBalancer to provision
```

## Rolling Back

```bash
# View deployment history
kubectl rollout history deployment/sample-python-app

# Rollback to previous version
kubectl rollout undo deployment/sample-python-app

# Rollback to specific revision
kubectl rollout undo deployment/sample-python-app --to-revision=2
```

## Clean Up

```bash
# Delete all resources
kubectl delete -f k8s/

# Or delete cluster
gcloud container clusters delete sample-gke-cluster --region us-central1
```
