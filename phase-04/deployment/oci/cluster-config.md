# Oracle Cloud Infrastructure (OCI) Configuration Guide

This guide documents the setup steps for deploying the Todo App to Oracle Kubernetes Engine (OKE) Free Tier.

## Prerequisites

- Oracle Cloud account (Free Tier)
- OCI CLI installed
- kubectl installed
- Docker installed (with buildx for multi-arch)
- Helm 3.x installed

## Phase 1: OCI Account Setup

### T021: Create Oracle Cloud Account

1. Go to: https://www.oracle.com/cloud/free/
2. Click "Start for free"
3. Fill in account details (name, email, country)
4. Add payment method (verification only - $0 charge or small hold that's refunded)
5. Wait for account provisioning (**can take up to 48 hours for review**)

**Important Notes:**
- If account goes to "Pending Review", wait up to 48 hours
- Don't retry signup while pending (causes errors)
- Contact Oracle Support Chat if pending > 48 hours

**Free Tier Resources (Always Free):**
- 4 ARM Ampere A1 cores + 24 GB RAM (flexible allocation)
- 2 AMD VMs (1/8 OCPU, 1GB RAM each)
- 200 GB block storage
- 10 GB object storage
- 10 TB outbound data transfer/month
- 1 Load Balancer (10 Mbps)

### T022: Install OCI CLI

**Windows (PowerShell as Admin):**
```powershell
# Download installer
Invoke-WebRequest https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.ps1 -OutFile install.ps1

# Run installer
powershell -ExecutionPolicy Bypass -File install.ps1 -AcceptAllDefaults

# Restart terminal, then configure
oci setup config
```

**During `oci setup config`, you'll need:**
- User OCID: Profile → User Settings → OCID (copy)
- Tenancy OCID: Profile → Tenancy → OCID (copy)
- Region: e.g., `us-ashburn-1`, `ap-mumbai-1`, `eu-frankfurt-1`
- Generate new API key: Yes (follow prompts to upload public key)

**Verify CLI:**
```bash
oci iam region list --output table
```

## Phase 2: Network Setup

### T023: Create VCN (Virtual Cloud Network)

**Via OCI Console (Recommended for beginners):**
1. Go to: Networking → Virtual Cloud Networks
2. Click "Start VCN Wizard"
3. Select "Create VCN with Internet Connectivity"
4. Configure:
   - Name: `todo-app-vcn`
   - Compartment: root (or your compartment)
   - VCN CIDR: `10.0.0.0/16`
5. Click "Next" → "Create"

This creates:
- Public subnet (for Load Balancer)
- Private subnet (for worker nodes)
- Internet Gateway
- NAT Gateway
- Service Gateway
- Route tables and security lists

## Phase 3: Create OKE Cluster

### T024: Create Kubernetes Cluster

**Via OCI Console:**
1. Go to: Developer Services → Kubernetes Clusters (OKE)
2. Click "Create Cluster"
3. Select **"Quick Create"** (recommended)
4. Configure:
   ```
   Name: todo-app-cluster
   Compartment: (your compartment)
   Kubernetes Version: v1.28.2 (or latest)
   Kubernetes API Endpoint: Public
   Kubernetes Worker Nodes: Public
   Shape: VM.Standard.A1.Flex (ARM - FREE TIER!)
   Number of nodes: 2
   OCPUs per node: 2 (total 4 = within free tier)
   Memory per node: 12 GB (total 24 GB = within free tier)
   Image: Oracle Linux 8
   ```
5. Click "Next" → "Create Cluster"

**Wait 10-15 minutes** for cluster to be ACTIVE.

### T025: Configure kubectl

```bash
# Get cluster OCID from OCI Console (Cluster Details page)

# Create kubeconfig
oci ce cluster create-kubeconfig \
  --cluster-id ocid1.cluster.oc1.xxx... \
  --file $HOME/.kube/config \
  --region us-ashburn-1 \
  --token-version 2.0.0 \
  --kube-endpoint PUBLIC_ENDPOINT

# Verify connection
kubectl get nodes

# Expected output:
# NAME          STATUS   ROLES   AGE   VERSION
# 10.0.10.x     Ready    node    5m    v1.28.2
# 10.0.10.y     Ready    node    5m    v1.28.2
```

## Phase 4: Container Registry Setup

### T029: Configure OCIR Access

```bash
# Get your tenancy namespace
oci os ns get

# Generate Auth Token (OCI Console):
# Profile → User Settings → Auth Tokens → Generate Token
# SAVE THIS TOKEN! It's only shown once.

# Login to OCIR
docker login <region-key>.ocir.io

# Username format: <tenancy-namespace>/oracleidentitycloudservice/<email>
# Password: <auth-token>

# Region keys:
# us-ashburn-1 = iad
# us-phoenix-1 = phx
# ap-mumbai-1 = bom
# eu-frankfurt-1 = fra
```

### T030: Build and Push ARM64 Images

```bash
# Set variables (replace with your values)
export REGION="iad"  # your region key
export NAMESPACE="your-tenancy-namespace"
export REPO="${REGION}.ocir.io/${NAMESPACE}/todo-app"

# Create buildx builder for multi-arch
docker buildx create --name armbuilder --use
docker buildx inspect --bootstrap

# Build and push frontend (ARM64)
docker buildx build \
  --platform linux/arm64 \
  -t ${REPO}/frontend:latest \
  --push \
  ./frontend

# Build and push backend (ARM64)
docker buildx build \
  --platform linux/arm64 \
  -t ${REPO}/backend:latest \
  --push \
  ./backend

# Build and push mcp-server (ARM64)
docker buildx build \
  --platform linux/arm64 \
  -t ${REPO}/mcp-server:latest \
  --push \
  ./mcp-server
```

## Phase 5: Deploy Application

### T032: Create Namespace and Secrets

```bash
# Create namespace
kubectl create namespace todo-app

# Create application secrets
kubectl create secret generic todo-secrets \
  --namespace todo-app \
  --from-literal=DATABASE_URL='postgresql://user:pass@neon-host:5432/dbname?sslmode=require' \
  --from-literal=JWT_SECRET='your-super-secure-jwt-secret-at-least-32-chars' \
  --from-literal=GEMINI_API_KEY='your-gemini-api-key'

# Create OCIR pull secret
kubectl create secret docker-registry ocir-secret \
  --namespace todo-app \
  --docker-server=${REGION}.ocir.io \
  --docker-username="${NAMESPACE}/oracleidentitycloudservice/<email>" \
  --docker-password="<auth-token>" \
  --docker-email="<email>"
```

### T033: Deploy with Helm

```bash
# First, update values-prod.yaml with your OCIR paths
# Then install:
helm install todo-app ./deployment/helm/todo-app \
  -f ./deployment/helm/todo-app/values-prod.yaml \
  --namespace todo-app \
  --set images.frontend.repository=${REPO}/frontend \
  --set images.backend.repository=${REPO}/backend \
  --set images.mcpServer.repository=${REPO}/mcp-server
```

### T034: Create LoadBalancer (External Access)

The Helm chart should create LoadBalancer services. Verify:

```bash
# Check services
kubectl get svc -n todo-app

# Get Load Balancer IP (wait 2-3 minutes for provisioning)
kubectl get svc frontend -n todo-app -w

# Once EXTERNAL-IP appears, access your app:
# http://<EXTERNAL-IP>:3000
```

### T035: Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n todo-app

# Expected:
# NAME                          READY   STATUS    RESTARTS   AGE
# backend-xxx-xxx               1/1     Running   0          2m
# frontend-xxx-xxx              1/1     Running   0          2m
# mcp-server-xxx-xxx            1/1     Running   0          2m

# Check logs if issues
kubectl logs -n todo-app deployment/backend
kubectl logs -n todo-app deployment/frontend

# Describe pod for events
kubectl describe pod -n todo-app <pod-name>
```

## Troubleshooting

### Account Pending Review
- Wait up to 48 hours
- Don't retry signup
- Contact Oracle Support Chat after 48h
- Use Support Chat, not Sales Chat

### Image Pull Errors (ErrImagePull)
```bash
# Check secret exists
kubectl get secret ocir-secret -n todo-app

# Verify image path format
# Correct: iad.ocir.io/tenancy-namespace/todo-app/frontend:latest

# Check pod events
kubectl describe pod <pod-name> -n todo-app
```

### ARM64 Compatibility Issues
- Ensure base images support ARM64 (most official images do)
- Use `docker buildx` with `--platform linux/arm64`
- Check with: `docker buildx imagetools inspect <image>`

### Node Not Ready
```bash
kubectl describe node <node-name>
# Check for disk pressure, memory pressure, or network issues
```

### LoadBalancer Pending
```bash
# Check OCI Console → Networking → Load Balancers
# Ensure subnet has proper security list rules
# Port 3000, 8000, 5001 need to be allowed
```

## Resource Limits (Free Tier)

| Resource | Free Tier Limit | Our Usage |
|----------|-----------------|-----------|
| ARM Compute | 4 OCPU, 24 GB RAM | ~1.3 OCPU, ~1.6 GB |
| Block Storage | 200 GB | ~50 GB |
| Load Balancer | 1 × 10 Mbps | 1 |
| Outbound Data | 10 TB/month | Minimal |

**Our deployment is well within free tier limits!**

## Useful Commands

```bash
# View all resources
kubectl get all -n todo-app

# Delete deployment (keep secrets)
helm uninstall todo-app -n todo-app

# Reinstall
helm install todo-app ./deployment/helm/todo-app -f values-prod.yaml -n todo-app

# Port forward for local testing
kubectl port-forward svc/backend 8000:8000 -n todo-app

# View logs
kubectl logs -f deployment/backend -n todo-app

# Execute shell in pod
kubectl exec -it deployment/backend -n todo-app -- /bin/bash

# Scale deployment
kubectl scale deployment/frontend --replicas=2 -n todo-app

# View resource usage
kubectl top pods -n todo-app
kubectl top nodes
```

## OCI Console Navigation

- **Clusters**: Developer Services → Kubernetes Clusters (OKE)
- **Images**: Developer Services → Container Registry
- **Load Balancers**: Networking → Load Balancers
- **VCN**: Networking → Virtual Cloud Networks
- **Compute**: Compute → Instances (see node VMs)
- **Logs**: Observability → Logging
