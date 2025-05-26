# Deployment guide (local deployment)

## Step 1: Start docker daemon

## Step 2: Start minikube
``` minikube start --driver=docker
```

## Step 3: Build Docker image within minikube

```eval $(minikube docker-env)
docker build -t pdf-chatbot:latest .
```

## Step 4: Deploy to kubernetes:
```kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

## Step 5: Access the app
```minikube service pdf-chatbot-service
```

