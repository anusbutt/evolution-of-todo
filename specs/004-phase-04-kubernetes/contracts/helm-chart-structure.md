# Helm Chart Contract: Todo Application

**Feature**: 004-phase-04-kubernetes
**Date**: 2026-01-22

## Chart Structure

```
deployment/helm/todo-app/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Default configuration values
├── templates/
│   ├── _helpers.tpl        # Template helpers
│   ├── namespace.yaml      # Namespace definition
│   ├── configmap.yaml      # ConfigMap for non-sensitive config
│   ├── secret.yaml         # Secret for sensitive config
│   ├── frontend/
│   │   ├── deployment.yaml # Frontend deployment
│   │   └── service.yaml    # Frontend service
│   ├── backend/
│   │   ├── deployment.yaml # Backend deployment
│   │   └── service.yaml    # Backend service
│   ├── mcp-server/
│   │   ├── deployment.yaml # MCP server deployment
│   │   └── service.yaml    # MCP server service
│   └── ingress.yaml        # Ingress for external access
└── .helmignore             # Files to ignore during packaging
```

## Chart.yaml Contract

```yaml
apiVersion: v2
name: todo-app
description: Todo Application with AI Chatbot
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - todo
  - kubernetes
  - helm
maintainers:
  - name: Developer
```

## values.yaml Contract

```yaml
# Namespace
namespace: todo-app

# Image configuration
images:
  frontend:
    repository: todo-frontend
    tag: latest
    pullPolicy: Never  # Use local images
  backend:
    repository: todo-backend
    tag: latest
    pullPolicy: Never
  mcpServer:
    repository: todo-mcp-server
    tag: latest
    pullPolicy: Never

# Replica configuration
replicas:
  frontend: 1
  backend: 1
  mcpServer: 1

# Resource limits
resources:
  frontend:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 512Mi
  backend:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 1000m
      memory: 1Gi
  mcpServer:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 512Mi

# Service ports
ports:
  frontend: 3000
  backend: 8000
  mcpServer: 5001

# Ingress configuration
ingress:
  enabled: true
  host: todo.local
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /

# Health check configuration
healthCheck:
  frontend:
    path: /
    initialDelaySeconds: 30
    periodSeconds: 10
  backend:
    path: /api/health
    initialDelaySeconds: 30
    periodSeconds: 10
  mcpServer:
    path: /health
    initialDelaySeconds: 30
    periodSeconds: 10

# Secrets (base64 encoded in actual deployment)
secrets:
  databaseUrl: ""      # Set via --set or values override
  jwtSecret: ""        # Set via --set or values override
  geminiApiKey: ""     # Set via --set or values override

# ConfigMap values
config:
  mcpServerUrl: "http://mcp-server:5001"
  internalApiUrl: "http://backend:8000"
```

## Template Contracts

### Deployment Template Contract

Each deployment MUST include:
- `metadata.name`: Service name
- `metadata.namespace`: `{{ .Values.namespace }}`
- `spec.replicas`: From values
- `spec.selector.matchLabels`: `app: <service-name>`
- `spec.template.spec.containers[0].image`: From values
- `spec.template.spec.containers[0].ports[0].containerPort`: From values
- `spec.template.spec.containers[0].resources`: From values
- `spec.template.spec.containers[0].livenessProbe`: HTTP health check
- `spec.template.spec.containers[0].readinessProbe`: HTTP health check
- `spec.template.spec.containers[0].envFrom`: ConfigMap and Secret references

### Service Template Contract

Each service MUST include:
- `metadata.name`: Service name
- `metadata.namespace`: `{{ .Values.namespace }}`
- `spec.type`: ClusterIP
- `spec.selector`: `app: <service-name>`
- `spec.ports[0].port`: Service port
- `spec.ports[0].targetPort`: Container port

### Ingress Template Contract

Ingress MUST include:
- `metadata.name`: `todo-ingress`
- `metadata.namespace`: `{{ .Values.namespace }}`
- `spec.ingressClassName`: `nginx`
- `spec.rules[0].host`: `{{ .Values.ingress.host }}`
- `spec.rules[0].http.paths`: Frontend and backend routing

## Helm Commands Contract

| Operation | Command | Expected Result |
|-----------|---------|-----------------|
| Install | `helm install todo-app ./todo-app -n todo-app --create-namespace` | All resources created |
| Status | `helm status todo-app -n todo-app` | Shows release status |
| Upgrade | `helm upgrade todo-app ./todo-app -n todo-app` | Rolling update |
| Rollback | `helm rollback todo-app -n todo-app` | Previous version restored |
| Uninstall | `helm uninstall todo-app -n todo-app` | All resources deleted |
| Dry Run | `helm install --dry-run --debug todo-app ./todo-app` | Template rendered |
