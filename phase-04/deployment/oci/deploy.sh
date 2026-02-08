#!/bin/bash
# [Task]: T032 | [Spec]: specs/005-phase-05-cloud-native/spec.md
# OpenShift Deployment Script for Todo App
# Usage: ./deploy.sh [build|deploy|all]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo -e "${GREEN}=== Todo App OpenShift Deployment ===${NC}"
echo "Project Root: $PROJECT_ROOT"
echo "OpenShift Project: $(oc project -q)"
echo ""

# Function to apply BuildConfigs
apply_buildconfigs() {
    echo -e "${YELLOW}Applying BuildConfigs...${NC}"
    oc apply -f "$SCRIPT_DIR/buildconfigs/"
    echo -e "${GREEN}BuildConfigs applied successfully${NC}"
}

# Function to build images
build_images() {
    echo -e "${YELLOW}Building images on OpenShift...${NC}"

    echo "Building frontend..."
    oc start-build frontend --from-dir="$PROJECT_ROOT/frontend" --follow

    echo "Building backend..."
    oc start-build backend --from-dir="$PROJECT_ROOT/backend" --follow

    echo "Building mcp-server..."
    oc start-build mcp-server --from-dir="$PROJECT_ROOT/mcp-server" --follow

    echo -e "${GREEN}All images built successfully${NC}"
}

# Function to deploy services
deploy_services() {
    echo -e "${YELLOW}Deploying services...${NC}"

    # Get current project name and substitute in deployment files
    PROJECT_NAME=$(oc project -q)

    # Apply deployments with project name substitution
    for file in "$SCRIPT_DIR/deployments/"*.yaml; do
        echo "Applying $file..."
        sed "s/\$(PROJECT_NAME)/$PROJECT_NAME/g" "$file" | oc apply -f -
    done

    echo -e "${GREEN}Deployments applied successfully${NC}"
}

# Function to create routes
create_routes() {
    echo -e "${YELLOW}Creating Routes...${NC}"
    oc apply -f "$SCRIPT_DIR/routes/"
    echo -e "${GREEN}Routes created successfully${NC}"
}

# Function to show status
show_status() {
    echo -e "${YELLOW}=== Deployment Status ===${NC}"
    echo ""
    echo "Pods:"
    oc get pods
    echo ""
    echo "Services:"
    oc get svc
    echo ""
    echo "Routes:"
    oc get routes
    echo ""
    echo "ImageStreams:"
    oc get is
}

# Main logic
case "${1:-all}" in
    build)
        apply_buildconfigs
        build_images
        ;;
    deploy)
        deploy_services
        create_routes
        show_status
        ;;
    all)
        apply_buildconfigs
        build_images
        deploy_services
        create_routes
        show_status
        ;;
    status)
        show_status
        ;;
    *)
        echo "Usage: $0 [build|deploy|all|status]"
        echo "  build  - Create BuildConfigs and build images"
        echo "  deploy - Deploy services and create routes"
        echo "  all    - Do everything (default)"
        echo "  status - Show deployment status"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}=== Deployment Complete ===${NC}"
echo ""
echo "Access your application at:"
oc get routes -o jsonpath='{range .items[*]}https://{.spec.host}{"\n"}{end}'
