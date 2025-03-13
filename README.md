
# Text Analyzer App

A FastAPI application with a beautiful UI for analyzing text, deployed on Kubernetes with load balancing.

## Kubernetes Deployment Instructions

### Prerequisites

#### Installing Docker
1. **Install Docker**
   ```
   # For Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io
   
   # For macOS
   brew install docker
   
   # For Windows
   # Download and install Docker Desktop from https://www.docker.com/products/docker-desktop
   ```

2. **Verify Docker installation**
   ```
   docker --version
   docker run hello-world
   ```

#### Setting up a Kubernetes Cluster
Choose one of the following options:

1. **Minikube (local development)**
   ```
   # Install Minikube
   curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
   sudo install minikube-linux-amd64 /usr/local/bin/minikube
   
   # Start a cluster
   minikube start
   
   # Enable the Ingress addon for external access
   minikube addons enable ingress
   ```

2. **K3s (lightweight Kubernetes)**
   ```
   # Install K3s
   curl -sfL https://get.k3s.io | sh -
   
   # Set up kubeconfig 
   mkdir -p ~/.kube
   sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
   sudo chown $(id -u):$(id -g) ~/.kube/config
   export KUBECONFIG=~/.kube/config
   ```

3. **Cloud Provider K8s Services**
   - **Google Kubernetes Engine (GKE)**
     ```
     # Install Google Cloud SDK
     curl https://sdk.cloud.google.com | bash
     gcloud init
     gcloud container clusters create text-analyzer-cluster --num-nodes=3
     gcloud container clusters get-credentials text-analyzer-cluster
     ```
   
   - **Amazon EKS**
     ```
     # Install AWS CLI and eksctl
     pip install awscli
     curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
     sudo mv /tmp/eksctl /usr/local/bin
     
     # Create an EKS cluster
     eksctl create cluster --name text-analyzer --nodes=3
     ```

#### Installing and configuring kubectl
1. **Install kubectl**
   ```
   # For Ubuntu/Debian
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   
   # For macOS
   brew install kubectl
   
   # For Windows
   # Download and install from https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
   ```

2. **Verify kubectl installation**
   ```
   kubectl version --client
   ```

3. **Configure kubectl**
   ```
   # Minikube automatically configures kubectl
   
   # For other setups, you may need to manually configure:
   mkdir -p $HOME/.kube
   # Copy the config file from your cluster to ~/.kube/config
   
   # Test your configuration
   kubectl cluster-info
   kubectl get nodes
   ```

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

## Troubleshooting

### Common Docker Issues
- **Permission denied**: Run Docker commands with sudo or add your user to the docker group: `sudo usermod -aG docker $USER`
- **Image not found**: Ensure you've built the image with the correct tag
- **Container fails to start**: Check logs with `docker logs <container-id>`

### Common Kubernetes Issues
- **Unauthorized**: Check your kubeconfig file and ensure proper authentication
- **Pods stuck in pending**: Check resources with `kubectl describe pod <pod-name>`
- **Service not accessible**: Verify service with `kubectl get svc` and check if LoadBalancer has an external IP
- **ImagePullBackOff**: Ensure the container registry is accessible and image exists

### Kubectl Configuration Issues
- **No connection**: Run `kubectl cluster-info` to verify connection
- **Context errors**: List contexts with `kubectl config get-contexts` and switch if needed with `kubectl config use-context <context-name>`
