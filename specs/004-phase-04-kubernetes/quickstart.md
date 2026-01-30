# Quickstart: Phase 4 - Local Kubernetes Deployment

**Feature**: 004-phase-04-kubernetes
**Date**: 2026-01-22

## Prerequisites

| Tool | Version | Check Command |
|------|---------|---------------|
| Docker Desktop | Latest | `docker --version` |
| Minikube | v1.32+ | `minikube version` |
| kubectl | v1.29+ | `kubectl version --client` |
| Helm | v3.14+ | `helm version` |

## Quick Deploy

### 1. Start Minikube

```bash
minikube start --driver=docker
minikube addons enable ingress
```

### 2. Load Docker Images

```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
minikube image load todo-mcp-server:latest
```

### 3. Deploy with Helm

```bash
cd deployment/helm
helm install todo-app ./todo-app -n todo-app --create-namespace
```

### 4. Configure Host Entry

Get Minikube IP:
```bash
minikube ip
```

Add to hosts file (`C:\Windows\System32\drivers\etc\hosts`):
```
<minikube-ip>  todo.local
```

### 5. Access Application

Open browser: http://todo.local

## Common Operations

### Check Status

```bash
kubectl get pods -n todo-app
kubectl get services -n todo-app
kubectl get ingress -n todo-app
```

### Pod Health Checks (US6)

Check if pods are healthy and ready:
```bash
# Quick health overview
kubectl get pods -n todo-app -o wide

# Detailed pod status with conditions
kubectl get pods -n todo-app -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\t"}{range .status.conditions[*]}{.type}={.status}{" "}{end}{"\n"}{end}'

# Check specific pod health
kubectl describe pod -n todo-app -l app=backend | grep -A5 "Conditions:"

# View liveness/readiness probe status
kubectl describe pod -n todo-app -l app=frontend | grep -A10 "Liveness:"
kubectl describe pod -n todo-app -l app=frontend | grep -A10 "Readiness:"

# Check recent events (shows probe failures, restarts)
kubectl get events -n todo-app --sort-by='.lastTimestamp' | tail -20

# Check restart counts (indicates health issues)
kubectl get pods -n todo-app -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}Restarts: {range .status.containerStatuses[*]}{.restartCount}{end}{"\n"}{end}'
```

### View Logs (US6)

```bash
# View logs by service
kubectl logs -n todo-app -l app=frontend
kubectl logs -n todo-app -l app=backend
kubectl logs -n todo-app -l app=mcp-server

# Follow logs in real-time
kubectl logs -n todo-app -l app=backend -f

# View logs from all containers with timestamps
kubectl logs -n todo-app -l app=backend --timestamps

# View previous container logs (after restart)
kubectl logs -n todo-app -l app=backend --previous

# View last 100 lines
kubectl logs -n todo-app -l app=backend --tail=100

# View logs from specific time
kubectl logs -n todo-app -l app=backend --since=1h
```

### Scale Service

```bash
kubectl scale deployment backend -n todo-app --replicas=3
```

### Helm Upgrade (US7)

```bash
# Basic upgrade (uses current values)
helm upgrade todo-app ./todo-app -n todo-app

# Upgrade with new values
helm upgrade todo-app ./todo-app -n todo-app --set backend.replicas=3

# Upgrade with values file
helm upgrade todo-app ./todo-app -n todo-app -f custom-values.yaml

# Upgrade and wait for pods to be ready
helm upgrade todo-app ./todo-app -n todo-app --wait --timeout=5m

# Dry-run to preview changes
helm upgrade todo-app ./todo-app -n todo-app --dry-run

# View upgrade history
helm history todo-app -n todo-app
```

### Helm Rollback (US7)

```bash
# Rollback to previous revision
helm rollback todo-app -n todo-app

# Rollback to specific revision
helm rollback todo-app 1 -n todo-app

# View revision history first
helm history todo-app -n todo-app

# Rollback and wait for completion
helm rollback todo-app -n todo-app --wait --timeout=5m
```

### Helm Uninstall and Cleanup (US7)

```bash
# Uninstall the release
helm uninstall todo-app -n todo-app

# Delete the namespace (removes all resources)
kubectl delete namespace todo-app

# Complete cleanup (uninstall + delete namespace)
helm uninstall todo-app -n todo-app && kubectl delete namespace todo-app

# Keep history for potential reinstall
helm uninstall todo-app -n todo-app --keep-history

# Verify cleanup
kubectl get all -n todo-app  # Should show "No resources found"
helm list -n todo-app        # Should show nothing
```

## Troubleshooting

### Pods Not Starting

```bash
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

### Ingress Not Working

```bash
minikube addons enable ingress
kubectl get ingress -n todo-app
```

### Image Not Found

```bash
minikube image load todo-frontend:latest
kubectl set image deployment/frontend frontend=todo-frontend:latest -n todo-app
```

## Environment Configuration

### Default values.yaml

```yaml
# Replica counts
frontend:
  replicas: 1
backend:
  replicas: 1
mcpServer:
  replicas: 1

# Ingress
ingress:
  host: todo.local

# Resource limits
resources:
  frontend:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 512Mi
```

### Override Values

```bash
helm install todo-app ./todo-app -n todo-app \
  --set backend.replicas=2 \
  --set ingress.host=myapp.local
```
