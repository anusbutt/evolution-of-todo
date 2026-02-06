# DigitalOcean Kubernetes (DOKS) Cluster Configuration

**[Task]: T037a | [Spec]: specs/005-phase-05-cloud-native/spec.md**

## Cluster Details

| Property | Value |
|----------|-------|
| Cluster Name | todo-app-cluster |
| Cluster ID | 2a1d1bab-72b2-4fd5-b628-ed7b48f1607b |
| Region | Frankfurt (fra1) |
| Kubernetes Version | v1.34.1-do.3 |
| Node Pool | worker-pool (2 nodes) |
| Node Size | s-2vcpu-2gb ($12/month each) |
| Architecture | amd64 (x86_64) |
| Container Registry | registry.digitalocean.com/todo-app |
| Load Balancer IP | 209.38.115.191 |
| Namespace | todo-app |

## Budget

| Resource | Monthly Cost |
|----------|-------------|
| DOKS Control Plane | Free |
| Worker Nodes (2x) | $24 |
| Load Balancer (1x) | $12 |
| DOCR (Starter) | Free |
| **Total** | **~$36/month** |
| Credit Available | $200 (60 days) |

## Setup Steps

### 1. Install doctl CLI

```bash
# Download and install
curl -sL https://github.com/digitalocean/doctl/releases/download/v1.150.0/doctl-1.150.0-windows-amd64.zip -o doctl.zip
unzip doctl.zip -d ~/bin/

# Authenticate
doctl auth init --access-token <YOUR_API_TOKEN>
```

### 2. Create DOKS Cluster

```bash
doctl kubernetes cluster create todo-app-cluster \
  --region fra1 \
  --version latest \
  --node-pool "name=worker-pool;size=s-2vcpu-2gb;count=2" \
  --wait
```

### 3. Create Container Registry

```bash
doctl registry create todo-app --region fra1
```

### 4. Integrate Registry with Cluster

```bash
kubectl create namespace todo-app
doctl registry kubernetes-manifest --namespace todo-app | kubectl apply -f -
```

### 5. Build and Push Images

```bash
doctl registry login

docker build -t registry.digitalocean.com/todo-app/frontend:latest ./frontend
docker build -t registry.digitalocean.com/todo-app/backend:latest ./backend
docker build -t registry.digitalocean.com/todo-app/mcp-server:latest ./mcp-server

docker push registry.digitalocean.com/todo-app/frontend:latest
docker push registry.digitalocean.com/todo-app/backend:latest
docker push registry.digitalocean.com/todo-app/mcp-server:latest
```

### 6. Deploy with Helm

```bash
helm upgrade --install todo-app ./deployment/helm/todo-app \
  -f ./deployment/helm/todo-app/values-prod.yaml \
  --namespace todo-app \
  --set secrets.databaseUrl='<DATABASE_URL>' \
  --set secrets.jwtSecret='<JWT_SECRET>' \
  --set secrets.geminiApiKey='<GEMINI_API_KEY>'
```

### 7. Verify Deployment

```bash
kubectl get pods -n todo-app        # All pods Running 1/1
kubectl get svc -n todo-app         # Frontend has external IP
curl http://<EXTERNAL_IP>:3000/     # Returns HTTP 200
```

## Useful Commands

```bash
# View logs
kubectl logs -n todo-app -l app=frontend
kubectl logs -n todo-app -l app=backend
kubectl logs -n todo-app -l app=mcp-server

# Restart a deployment
kubectl rollout restart deployment/backend -n todo-app

# Scale
kubectl scale deployment backend -n todo-app --replicas=2

# Update images (after rebuild/push)
helm upgrade todo-app ./deployment/helm/todo-app \
  -f ./deployment/helm/todo-app/values-prod.yaml \
  --namespace todo-app

# Delete everything
helm uninstall todo-app -n todo-app
doctl kubernetes cluster delete todo-app-cluster
doctl registry delete todo-app
```

## Migration Notes

Migrated from Oracle Cloud Infrastructure (OCI) OKE on 2026-02-05.
- **Reason**: ARM64 (Ampere A1) capacity exhausted in ap-mumbai-1; free tier limited to 1 region
- **Impact**: ARM64 → amd64, OCIR → DOCR, oci CLI → doctl CLI
- **ADR**: Pending (cloud-provider-migration-oci-to-digitalocean)
