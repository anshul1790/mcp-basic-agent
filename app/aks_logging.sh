#!/bin/bash

# this later be converted to func tool for LLM

# Configuration
RESOURCE_GROUP="<load from env variables>"
CLUSTER_NAME="<load from env variables>"

# Check Azure login
if ! az account show > /dev/null 2>&1; then
  echo "❌ You are not logged in to Azure."
  echo "👉 Please run 'az login' and try again."
  exit 1
fi

echo "✅ Azure login verified. Continuing..."

# Display current Azure subscription
echo "✅ Using Azure subscription:"
az account show --query "{Name:name, ID:id}" -o table

# Logging to AKS using get credentials
echo "🔗 Getting AKS credentials for cluster: $CLUSTER_NAME"
az aks get-credentials --resource-group "$RESOURCE_GROUP" --name "$CLUSTER_NAME" --overwrite-existing

## Caching the credentials
echo "🔧 Converting kubeconfig to use Azure CLI token (to avoid repeated logins)..."
kubelogin convert-kubeconfig -l azurecli


# Fetching namespaces and Giving User option to select namespace
echo ""
echo "📦 Fetching namespaces..."
NAMESPACES=($(kubectl get namespaces -o custom-columns=NAME:.metadata.name --no-headers))

echo ""
echo "👉 Select a namespace:"
select NAMESPACE in "${NAMESPACES[@]}"; do
  if [ -n "$NAMESPACE" ]; then
    echo "✅ You selected namespace: $NAMESPACE"
    break
  else
    echo "❗ Invalid selection. Try again."
  fi
done

# Fetching workloads and Giving User option to select workload
echo ""
echo "🔍 Fetching workloads (deployments) in namespace '$NAMESPACE'..."
DEPLOYMENTS=($(kubectl get deployments -n "$NAMESPACE" -o custom-columns=NAME:.metadata.name --no-headers))

if [ ${#DEPLOYMENTS[@]} -eq 0 ]; then
  echo "❌ No deployments found in namespace '$NAMESPACE'."
  exit 1
fi



while true; do
  echo ""
  echo "🔍 Fetching workloads (deployments) in namespace '$NAMESPACE'..."
  DEPLOYMENTS=($(kubectl get deployments -n "$NAMESPACE" -o custom-columns=NAME:.metadata.name --no-headers))

  if [ ${#DEPLOYMENTS[@]} -eq 0 ]; then
    echo "❌ No deployments found in namespace '$NAMESPACE'."
    exit 1
  fi

  echo ""
  echo "👉 Select a workload (deployment):"
  select WORKLOAD in "${DEPLOYMENTS[@]}"; do
    if [ -n "$WORKLOAD" ]; then
      echo "✅ You selected workload: $WORKLOAD"
      break
    else
      echo "❗ Invalid selection. Try again."
    fi
  done

  while true; do
    echo ""
    echo "📦 Fetching pods for workload '$WORKLOAD' in namespace '$NAMESPACE'..."
    PODS=($(kubectl get pods -n "$NAMESPACE" --no-headers | grep "$WORKLOAD" | awk '{print $1}'))

    if [ ${#PODS[@]} -eq 0 ]; then
      echo "❌ No pods found for workload '$WORKLOAD'."
      break
    fi

    echo ""
    echo "👉 Select a pod:"
    select POD_NAME in "${PODS[@]}"; do
      if [ -n "$POD_NAME" ]; then
        echo "✅ You selected pod: $POD_NAME"
        break
      else
        echo "❗ Invalid selection. Try again."
      fi
    done

    read -p "⏱️ Enter how many minutes back you want logs (default: 30): " MINUTES
    MINUTES=${MINUTES:-30}

    echo ""
    echo "📄 Fetching logs from pod '$POD_NAME' in namespace '$NAMESPACE' for the last $MINUTES minutes..."
    echo "------------------------------------------------------------"
    kubectl logs -n "$NAMESPACE" "$POD_NAME" --since=${MINUTES}m --timestamps

    echo ""
    read -p "🔁 Do you want to view logs for another pod in the same workload? (y/n): " AGAIN
    [[ "$AGAIN" =~ ^[Yy]$ ]] || break
  done

  echo ""
  read -p "🔁 Do you want to select a different workload? (y/n): " AGAIN_WORKLOAD
  [[ "$AGAIN_WORKLOAD" =~ ^[Yy]$ ]] || break
done
