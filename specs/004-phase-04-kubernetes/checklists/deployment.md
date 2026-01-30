# Deployment Checklist: Phase 4 - Local Kubernetes Deployment

**Purpose**: Pre-deployment validation checklist to ensure successful deployment
**Created**: 2026-01-27
**Feature**: 004-phase-04-kubernetes

## Pre-Deployment Checks

### Environment Prerequisites

- [ ] Docker Desktop is running
- [ ] Minikube is started (`minikube status`)
- [ ] kubectl is configured (`kubectl cluster-info`)
- [ ] Helm is installed (`helm version`)
- [ ] Ingress addon is enabled (`minikube addons enable ingress`)

### Docker Images

- [ ] todo-frontend:latest image exists (`docker images | grep todo-frontend`)
- [ ] todo-backend:latest image exists (`docker images | grep todo-backend`)
- [ ] todo-mcp-server:latest image exists (`docker images | grep todo-mcp-server`)
- [ ] Images loaded into Minikube (`minikube image load <image>` for each)

### Configuration

- [ ] Database URL is set (Neon PostgreSQL connection string)
- [ ] JWT secret is generated (secure random string)
- [ ] Gemini API key is available (for AI chatbot)

## Deployment Steps

### Step 1: Validate Helm Chart

- [ ] Run `helm lint ./deployment/helm/todo-app`
- [ ] Run `helm template todo-app ./deployment/helm/todo-app` (verify no errors)

### Step 2: Deploy Application

- [ ] Run `helm install todo-app ./deployment/helm/todo-app -n todo-app --create-namespace`
- [ ] Or with secrets: `helm install todo-app ./deployment/helm/todo-app -n todo-app --create-namespace --set secrets.databaseUrl=<url> --set secrets.jwtSecret=<secret> --set secrets.geminiApiKey=<key>`

### Step 3: Verify Deployment

- [ ] All pods are Running: `kubectl get pods -n todo-app`
- [ ] All services are created: `kubectl get services -n todo-app`
- [ ] Ingress is configured: `kubectl get ingress -n todo-app`

### Step 4: Configure Access

- [ ] Get Minikube IP: `minikube ip`
- [ ] Add hosts entry: `<minikube-ip>  todo.local` to hosts file
  - Windows: `C:\Windows\System32\drivers\etc\hosts`
  - Linux/Mac: `/etc/hosts`

### Step 5: Test Application

- [ ] Access http://todo.local in browser
- [ ] Login page loads correctly
- [ ] Can create a new user account
- [ ] Can create, read, update, delete tasks
- [ ] AI chatbot responds to messages

## Post-Deployment Validation

### User Story 1 - Deploy Application

- [ ] All three pods are in Running state
- [ ] No pod restarts (restart count = 0)
- [ ] Deployment completed within 5 minutes

### User Story 2 - Single URL Access

- [ ] http://todo.local shows frontend
- [ ] API calls to /api/* route to backend
- [ ] No CORS or routing errors in browser console

### User Story 3 - Self-Healing

- [ ] Delete a pod: `kubectl delete pod -n todo-app -l app=backend`
- [ ] Verify new pod starts within 60 seconds
- [ ] Application remains accessible during restart

### User Story 4 - Scaling

- [ ] Scale backend: `kubectl scale deployment backend -n todo-app --replicas=2`
- [ ] Verify 2 pods running: `kubectl get pods -n todo-app -l app=backend`
- [ ] Scale back down: `kubectl scale deployment backend -n todo-app --replicas=1`

### User Story 5 - Secrets

- [ ] Secrets not visible in pod spec: `kubectl get pod -n todo-app -l app=backend -o yaml | grep -i secret`
- [ ] Shows secretRef, not actual values

### User Story 6 - Monitoring

- [ ] View pod health: `kubectl get pods -n todo-app`
- [ ] View logs: `kubectl logs -n todo-app -l app=backend`
- [ ] Check events: `kubectl get events -n todo-app`

### User Story 7 - Lifecycle

- [ ] Upgrade works: `helm upgrade todo-app ./deployment/helm/todo-app -n todo-app`
- [ ] Rollback works: `helm rollback todo-app -n todo-app`
- [ ] Uninstall works: `helm uninstall todo-app -n todo-app`

## Troubleshooting Quick Reference

| Issue | Check Command | Common Fix |
|-------|---------------|------------|
| Pod not starting | `kubectl describe pod <name> -n todo-app` | Check image name, resources |
| Image pull error | `kubectl get events -n todo-app` | Load images into Minikube |
| Ingress not working | `minikube addons list` | Enable ingress addon |
| Can't access todo.local | `ping todo.local` | Add hosts file entry |
| API errors | `kubectl logs -n todo-app -l app=backend` | Check database connection |

## Success Criteria Verification

| Criteria | Test | Expected Result |
|----------|------|-----------------|
| SC-001 | Single deployment command | All services running < 5 min |
| SC-002 | Browser access | http://todo.local loads |
| SC-003 | CRUD operations | Create/read/update/delete tasks work |
| SC-004 | AI chatbot | Chatbot responds to messages |
| SC-005 | Pod deletion | New pod starts < 60 sec |
| SC-006 | Scaling | 3 replicas running < 2 min |
| SC-007 | Fault tolerance | App works with 1 pod down (2+ replicas) |
| SC-008 | Upgrade/rollback | Both complete successfully |
| SC-009 | Uninstall | All resources removed |
| SC-010 | Secret security | No secrets in pod specs/logs |
