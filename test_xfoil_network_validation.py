import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TESTS = ROOT / "k8s" / "xfoil-worker" / "tests"
SCRIPT = ROOT / "scripts" / "validate_xfoil_worker_networkpolicy.sh"
POLICY = ROOT / "k8s" / "xfoil-worker" / "networkpolicy.yaml"


class XFoilNetworkValidationTests(unittest.TestCase):
    def test_runner_is_shell_valid_and_has_required_network_checks(self):
        subprocess.run(["bash", "-n", str(SCRIPT)], check=True)
        content = SCRIPT.read_text(encoding="utf-8")
        required = [
            "xfoil-worker-restricted-traffic",
            "--for=condition=available deployment/xfoil-worker",
            "kubernetes.default.svc.cluster.local",
            "for attempt in 1 2 3 4 5",
            "xfoil-allowed-client",
            "xfoil-blocked-client",
            "/healthz",
            "/readyz",
            "NetworkPolicy validation failed",
            "--connect-timeout 3",
            "--max-time 8",
        ]
        for marker in required:
            self.assertIn(marker, content)

    def test_fixture_contract_matches_networkpolicy_allowlist(self):
        namespace = (TESTS / "client-namespace.yaml").read_text(encoding="utf-8")
        clients = (TESTS / "networkpolicy-clients.yaml").read_text(encoding="utf-8")
        policy = POLICY.read_text(encoding="utf-8")
        self.assertIn('naca-airfoil-kit/xfoil-client: "true"', namespace)
        self.assertIn('naca-airfoil-kit/xfoil-client: "true"', clients)
        self.assertEqual(clients.count('naca-airfoil-kit/xfoil-client: "true"'), 1)
        self.assertIn('naca-airfoil-kit/xfoil-client: "true"', policy)
        self.assertIn("allowPrivilegeEscalation: false", clients)
        self.assertIn("readOnlyRootFilesystem: true", clients)

    def test_policy_remains_internal_with_dns_only_egress(self):
        policy = POLICY.read_text(encoding="utf-8")
        self.assertIn("policyTypes:", policy)
        self.assertIn("- Ingress", policy)
        self.assertIn("- Egress", policy)
        self.assertIn("kube-dns", policy)
        self.assertIn("port: 53", policy)
        self.assertNotIn("0.0.0.0/0", policy)


if __name__ == "__main__":
    unittest.main()
