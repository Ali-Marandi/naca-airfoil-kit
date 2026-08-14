#!/usr/bin/env bash
# Validate the XFOIL worker's Kubernetes NetworkPolicy in an already deployed cluster.
# The script performs no public exposure and removes its test namespace by default.
set -euo pipefail

WORKER_NAMESPACE="naca-xfoil"
TEST_NAMESPACE="naca-xfoil-network-test"
KEEP_FIXTURES=false
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_URL="http://xfoil-worker.${WORKER_NAMESPACE}.svc.cluster.local:8080"

usage() {
  cat <<'EOF'
Usage: scripts/validate_xfoil_worker_networkpolicy.sh [options]

Options:
  --worker-namespace NAME   Namespace containing xfoil-worker (default: naca-xfoil)
  --test-namespace NAME     Ephemeral test namespace (default: naca-xfoil-network-test)
  --keep-fixtures           Keep the test namespace and pods for diagnosis
  -h, --help                Show this message

Preconditions: kubectl points to a non-production test/staging cluster, the worker
is deployed and ready, and its CNI enforces Kubernetes NetworkPolicy.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --worker-namespace) WORKER_NAMESPACE="$2"; shift 2 ;;
    --test-namespace) TEST_NAMESPACE="$2"; shift 2 ;;
    --keep-fixtures) KEEP_FIXTURES=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done
SERVICE_URL="http://xfoil-worker.${WORKER_NAMESPACE}.svc.cluster.local:8080"

for command in kubectl; do
  command -v "$command" >/dev/null || { echo "Missing required command: $command" >&2; exit 127; }
done

cleanup() {
  if [[ "$KEEP_FIXTURES" == false ]]; then
    kubectl delete namespace "$TEST_NAMESPACE" --ignore-not-found --wait=false >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

if ! kubectl -n "$WORKER_NAMESPACE" get networkpolicy xfoil-worker-restricted-traffic >/dev/null; then
  echo "Required NetworkPolicy is not present in namespace ${WORKER_NAMESPACE}." >&2
  exit 1
fi
if ! kubectl -n "$WORKER_NAMESPACE" get deployment xfoil-worker >/dev/null; then
  echo "Required xfoil-worker Deployment is not present in namespace ${WORKER_NAMESPACE}." >&2
  exit 1
fi
kubectl -n "$WORKER_NAMESPACE" wait --for=condition=available deployment/xfoil-worker --timeout=90s

# Verify that the worker itself can perform its explicitly allowlisted DNS egress.
# This does not grant the worker arbitrary external network access.
kubectl -n "$WORKER_NAMESPACE" exec deployment/xfoil-worker -- python -c "import socket; socket.gethostbyname('kubernetes.default.svc.cluster.local')"

# The fixture manifest has a fixed test namespace name; create a small rendered copy
# when the caller asks for a different isolated namespace.
fixture_dir="${ROOT_DIR}/k8s/xfoil-worker/tests"
if [[ "$TEST_NAMESPACE" == "naca-xfoil-network-test" ]]; then
  kubectl apply -f "${fixture_dir}/client-namespace.yaml"
  kubectl apply -f "${fixture_dir}/networkpolicy-clients.yaml"
else
  sed "s/naca-xfoil-network-test/${TEST_NAMESPACE}/g" "${fixture_dir}/client-namespace.yaml" | kubectl apply -f -
  sed "s/naca-xfoil-network-test/${TEST_NAMESPACE}/g" "${fixture_dir}/networkpolicy-clients.yaml" | kubectl apply -f -
fi

kubectl -n "$TEST_NAMESPACE" wait --for=condition=Ready pod/xfoil-allowed-client --timeout=90s
kubectl -n "$TEST_NAMESPACE" wait --for=condition=Ready pod/xfoil-blocked-client --timeout=90s

# Five consecutive calls prove DNS/service routing and short-lived connection stability
# from an allowlisted caller. /readyz additionally proves that the worker can accept work.
for attempt in 1 2 3 4 5; do
  code="$(kubectl -n "$TEST_NAMESPACE" exec pod/xfoil-allowed-client -- curl --silent --show-error --connect-timeout 3 --max-time 8 --output /dev/null --write-out '%{http_code}' "${SERVICE_URL}/healthz")"
  [[ "$code" == "200" ]] || { echo "Allowed client health attempt ${attempt} returned HTTP ${code}." >&2; exit 1; }
done
ready_code="$(kubectl -n "$TEST_NAMESPACE" exec pod/xfoil-allowed-client -- curl --silent --show-error --connect-timeout 3 --max-time 8 --output /dev/null --write-out '%{http_code}' "${SERVICE_URL}/readyz")"
[[ "$ready_code" == "200" ]] || { echo "Allowed client readiness returned HTTP ${ready_code}." >&2; exit 1; }

# A caller in the allowlisted namespace but without the allowlisted Pod label must fail
# to connect. A successful connection would indicate that the NetworkPolicy is not being
# enforced as designed.
if kubectl -n "$TEST_NAMESPACE" exec pod/xfoil-blocked-client -- curl --silent --show-error --connect-timeout 3 --max-time 8 --output /dev/null --fail "${SERVICE_URL}/healthz" >/dev/null 2>&1; then
  echo "Blocked client unexpectedly reached the worker; NetworkPolicy validation failed." >&2
  exit 1
fi

echo "PASS: worker DNS egress, 5/5 allowlisted health calls, allowlisted readiness, and blocked-client denial were verified."
