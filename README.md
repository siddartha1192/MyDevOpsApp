
# Text Analyzer App

A FastAPI application with a beautiful UI for analyzing text.

## Kubernetes Deployment Instructions

### Prerequisites
- Docker installed
- Kubernetes cluster (like Minikube, K3s, or a cloud provider K8s service)
- kubectl configured

### Deployment Steps

1. **Build the Docker image**
   ```
   docker build -t text-analyzer:latest .
   ```

2. **If using a remote registry, push the image**
   ```
   docker tag text-analyzer:latest your-registry/text-analyzer:latest
   docker push your-registry/text-analyzer:latest
   ```
   
   Then update the `kubernetes.yaml` file to use your image path.

3. **Deploy to Kubernetes**
   ```
   kubectl apply -f kubernetes.yaml
   ```

4. **Access the application**
   ```
   kubectl get service text-analyzer-service
   ```
   
   The EXTERNAL-IP column will show the IP address where your application is accessible.

## Features

- Character count
- Letter count
- Word count
- Beautiful UI with animations

## Local Development

Run with:
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
