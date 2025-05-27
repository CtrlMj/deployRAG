# Deployment guide (local deployment)

### Step 1: Start docker daemon

### Step 2: Start minikube
``` 
minikube start
```

### Step 3: Build Docker image within minikube

```
eval $(minikube docker-env)
docker build -t pdf-chatbot:latest .
```
### Step 4: add your openai token as secret
```
kubectl create secret generic openai-secret --from-literal=OPENAI_API_KEY='your-api-key-here'
```

### Step 5: Deploy to kubernetes
```
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

### Step 6: Access the app
```
minikube service pdf-chatbot-service
or
kubectl port-forward service/pdf-chatbot-service 8501:8501 8502:8502
```
### Deployment considerations for prod
- Stack: Streamlit is probably not ideal for prod. Next.js or Node.js or FastAPI behind NGINX to handle concurrent requests and authentication is better. 
- Caching, batch jobs, Volumes: Use Redis to cache frequent or recent requests, bach jobs to update the vectordb, and mount volumes for data that needs to persistent beyond node crashes or updates.
- Cloud clusters: In prod we likely use AWS EKS or GKE rather than a local cluster which offers better scaling, reliability, and node management as well as better integration with logging and monitoring tools. Note that scaling here refers to node scaling and not pod scaling which is defined by the HPA. Typically load testing informs the scaling decisions
- Container registry: The docker images are likely pushed to a private container registry such as AWS ECR, GCR. Keep images as minimal as possible and check for security vulnerabilities reguraly. 
- Ingress or Extenral service: We'd need to setup a controller to manage external access to the pods, provide load balancing, 
- Secret manager: We'd likely use AWS secret manager to store secrets such as API keys rather than storing in kubernetes directly
- Tests and CI/CD: Define tests and set up CI/CD pipelines (e.g., Jenkins, Github Actions, etc.) to preclude breaking changes and provide consistent deployments
- Logging: Enable extensive logging and store in Elastic search or cloud native logging services.

# Monitoring
`servicemonitoring.yaml` and `custom-values.yaml` are configured to monitor the deployments via Prometheus and Grafana.

### Step 1: Install Prometheus and Grafana from heml charts
```
brew install helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack
```
Note that this creates kubernetes resources for Prometheus and Grafana in the "default" namespace. Pass -n flag for a different namespace (More appropriate for production)

### Step 2: Access the Grafana service
```
minikube service monitoring-grafana
```
Username: admin
Password: prom-operator

### Monitroing considerations for prod
**Note:** Besides the default CPU and memory metrics for the deployment pods, Custom metrics such as token_count, number_of_requests, and latency are being tracked as per /app/metrics.py for demo purposes
For production, we should add more comprehensive metrics such as:
- Latency percentiles
- Requests per user/IP
- Error count/types
- VectorDB latency
- LLM API latency
- Source document match count
- Prompt/response length
- etc.

**Dashboards and Alerts:** 
- Create dashboards for intuitve visualization of metrics and logs
- Setup alerts for critical metrics such as high latency, high error rate, Low availability, LLM API timeouts,etc.




