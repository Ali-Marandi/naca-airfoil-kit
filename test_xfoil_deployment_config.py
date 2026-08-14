import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class XFoilDeploymentConfigTests(unittest.TestCase):
    def test_worker_dockerfile_applies_required_process_isolation_controls(self):
        dockerfile = (ROOT / "Dockerfile.xfoil-worker").read_text(encoding="utf-8")
        self.assertIn("apt-get install --no-install-recommends -y xfoil", dockerfile)
        self.assertIn("USER 10001:10001", dockerfile)
        self.assertIn("HEALTHCHECK", dockerfile)
        self.assertIn('CMD ["uvicorn"', dockerfile)
        self.assertIn("XFOIL_TEMP_ROOT=/tmp/xfoil-runs", dockerfile)

    def test_compose_keeps_worker_internal_and_restricts_runtime(self):
        compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertIn("xfoil-worker:", compose)
        self.assertIn("profiles: [\"xfoil\"]", compose)
        self.assertIn("expose:", compose)
        self.assertNotIn("      - \"8080:8080\"", compose)
        self.assertIn("read_only: true", compose)
        self.assertIn("cap_drop:", compose)
        self.assertIn("- ALL", compose)
        self.assertIn("no-new-privileges:true", compose)
        self.assertIn("XFOIL_WORKER_API_KEY_FILE", compose)
        self.assertNotIn("XFOIL_WORKER_API_KEY: ${", compose)
        self.assertIn("xfoil_worker_api_key:", compose)
        self.assertIn("user: \"10001:10001\"", compose)
        self.assertIn("ulimits:", compose)
        self.assertIn("max-size: \"10m\"", compose)

    def test_ci_tests_before_publish_and_generates_supply_chain_metadata(self):
        workflow = (ROOT / ".github/workflows/xfoil-worker.yml").read_text(encoding="utf-8")
        self.assertIn("python-tests:", workflow)
        self.assertIn("image-smoke-test:", workflow)
        self.assertIn("needs: python-tests", workflow)
        self.assertIn("publish:", workflow)
        self.assertIn("needs: image-smoke-test", workflow)
        self.assertIn("provenance: mode=max", workflow)
        self.assertIn("sbom: true", workflow)
        self.assertIn("packages: write", workflow)


if __name__ == "__main__":
    unittest.main()
