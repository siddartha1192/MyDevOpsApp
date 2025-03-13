
# Text Analyzer App

A FastAPI application with a beautiful UI for analyzing text, deployed on Kubernetes with load balancing.

## Kubernetes Deployment Instructions

### Prerequisites
- Docker installed
- Kubernetes cluster (like Minikube, K3s, or a cloud provider K8s service)
- kubectl configured

### Deployment Steps

1. **Clone the repository**
   ```
   git clone <repository-url>
   cd text-analyzer
   ```

2. **Build the Docker image**
   ```
   docker build -t text-analyzer:latest .
   ```

3. **If using a remote registry, push the image**
   ```
   docker tag text-analyzer:latest your-registry/text-analyzer:latest
   docker push your-registry/text-analyzer:latest
   ```
   
   Then update the `kubernetes.yaml` file to use your image path.

4. **Deploy to Kubernetes**
   ```
   kubectl apply -f kubernetes.yaml
   ```

5. **Verify deployment status**
   ```
   kubectl get deployments
   kubectl get pods
   ```

6. **Check the service and load balancer**
   ```
   kubectl get service text-analyzer-service
   ```
   
   The EXTERNAL-IP column will show the IP address where your application is accessible.

7. **Scale the deployment manually (if needed)**
   ```
   kubectl scale deployment text-analyzer --replicas=5
   ```

8. **View logs from pods**
   ```
   kubectl logs -l app=text-analyzer
   ```

9. **Test the load balancing**
   ```
   curl http://<EXTERNAL-IP>
   ```

10. **Check horizontal pod autoscaler**
    ```
    kubectl get hpa text-analyzer-hpa
    ```

11. **Delete the deployment (when needed)**
    ```
    kubectl delete -f kubernetes.yaml
    ```

## Load Balancing Details

This application is deployed with the following load balancing features:

- **Service Type**: LoadBalancer (distributes traffic to multiple pods)
- **Initial Replicas**: 3 pods running simultaneously
- **Horizontal Pod Autoscaler**: Scales from 1 to 10 pods based on CPU utilization (80%)
- **Resource Limits**: Each pod limited to 0.5 CPU and 512Mi memory

## Features

- Character count
- Letter count
- Word count
- Beautiful UI with animations
- Kubernetes deployment with load balancing
- Horizontal pod autoscaling

## Local Development

Run with:
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Replit Development

This application is configured to run on Replit. Simply hit the Run button to start the development server.
