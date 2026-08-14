import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
K8S = ROOT / "k8s" / "xfoil-worker"


class KubernetesWorkerManifestTests(unittest.TestCase):
    def test_namespace_enforces_restricted_pod_security(self):
        namespace = (K8S / "namespace.yaml").read_text(encoding="utf-8")
        self.assertIn("pod-security.kubernetes.io/enforce: restricted", namespace)
        self.assertIn("pod-security.kubernetes.io/audit: restricted", namespace)

    def test_deployment_applies_restricted_runtime_controls_and_limits(self):
        deployment = (K8S / "deployment.yaml").read_text(encoding="utf-8")
        required = [
            "automountServiceAccountToken: false",
            "runAsNonRoot: true",
            "runAsUser: 10001",
            "type: RuntimeDefault",
            "readOnlyRootFilesystem: true",
            "allowPrivilegeEscalation: false",
            "drop:\n                - ALL",
            "ephemeral-storage: 256Mi",
            "emptyDir:",
            "sizeLimit: 64Mi",
            "XFOIL_WORKER_API_KEY_FILE",
            "path: /readyz",
        ]
        for marker in required:
            self.assertIn(marker, deployment)
        self.assertNotIn("hostNetwork: true", deployment)
        self.assertNotIn("hostPID: true", deployment)
        self.assertNotIn("hostPath:", deployment)
        self.assertNotIn("privileged: true", deployment)

    def test_service_is_internal_and_network_policy_is_allowlisted(self):
        service = (K8S / "service.yaml").read_text(encoding="utf-8")
        policy = (K8S / "networkpolicy.yaml").read_text(encoding="utf-8")
        self.assertIn("type: ClusterIP", service)
        self.assertIn("policyTypes:", policy)
        self.assertIn("- Ingress", policy)
        self.assertIn("- Egress", policy)
        self.assertIn("naca-airfoil-kit/xfoil-client", policy)
        self.assertIn("kube-dns", policy)

    def test_kustomization_excludes_secret_example(self):
        kustomization = (K8S / "kustomization.yaml").read_text(encoding="utf-8")
        self.assertNotIn("secret.example.yaml", kustomization)
        self.assertIn("deployment.yaml", kustomization)


if __name__ == "__main__":
    unittest.main()
