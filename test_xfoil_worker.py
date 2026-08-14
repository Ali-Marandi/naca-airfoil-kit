import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from airfoil_pro import NACAGeneratorPro
from xfoil_worker_app import WorkerSettings, create_app


class XFoilWorkerTests(unittest.TestCase):
    def setUp(self):
        xu, yu, xl, yl = NACAGeneratorPro.naca4("0012", 30)
        self.coordinates = list(zip(xu[::-1], yu[::-1])) + list(zip(xl[1:], yl[1:]))

    def make_client(self, api_key="", allow_insecure_no_auth=False, requests_per_minute=30, request_body_limit_bytes=262_144, xfoil_executable="/not/a/real/xfoil"):
        temporary_dir = tempfile.TemporaryDirectory()
        settings = WorkerSettings(
            api_key=api_key,
            allow_insecure_no_auth=allow_insecure_no_auth,
            xfoil_executable=xfoil_executable,
            max_concurrency=1,
            requests_per_minute=requests_per_minute,
            request_body_limit_bytes=request_body_limit_bytes,
            temp_root=Path(temporary_dir.name),
        )
        return temporary_dir, TestClient(create_app(settings))

    def polar_payload(self):
        return {
            "airfoil_name": "NACA 0012",
            "coordinates": self.coordinates,
            "reynolds": 100_000,
            "alpha_start": -2.0,
            "alpha_end": 2.0,
            "alpha_step": 2.0,
        }

    def test_health_is_misconfigured_without_key_or_explicit_dev_override(self):
        temporary_dir, client = self.make_client()
        with temporary_dir, client:
            response = client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "misconfigured")
        self.assertNotIn("xfoil_executable_available", response.json())

    def test_health_exposes_degraded_state_in_explicit_insecure_development_mode(self):
        temporary_dir, client = self.make_client(allow_insecure_no_auth=True)
        with temporary_dir, client:
            response = client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "degraded")

    def test_readiness_rejects_misconfigured_or_solver_missing_worker(self):
        temporary_dir, client = self.make_client(api_key="test-secret")
        with temporary_dir, client:
            response = client.get("/readyz")
        self.assertEqual(response.status_code, 503)

    def test_readiness_accepts_configured_worker_with_solver_file(self):
        with tempfile.TemporaryDirectory() as executable_dir:
            executable = Path(executable_dir) / "xfoil"
            executable.touch()
            temporary_dir, client = self.make_client(api_key="test-secret", xfoil_executable=str(executable))
            with temporary_dir, client:
                response = client.get("/readyz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_polar_endpoint_fails_closed_without_auth_configuration(self):
        temporary_dir, client = self.make_client()
        with temporary_dir, client:
            response = client.post("/v1/polar", json=self.polar_payload())
        self.assertEqual(response.status_code, 503)

    def test_polar_endpoint_requires_key_when_configured(self):
        temporary_dir, client = self.make_client(api_key="test-secret")
        with temporary_dir, client:
            denied = client.post("/v1/polar", json=self.polar_payload())
            accepted = client.post("/v1/polar", json=self.polar_payload(), headers={"X-API-Key": "test-secret"})
        self.assertEqual(denied.status_code, 401)
        self.assertEqual(accepted.status_code, 200)
        self.assertEqual(accepted.json()["status"], "executable_not_found")
        self.assertEqual(accepted.json()["solver"], "xfoil")
        self.assertEqual(accepted.headers["cache-control"], "no-store")
        self.assertEqual(accepted.headers["x-content-type-options"], "nosniff")

    def test_polar_schema_rejects_extra_field_and_invalid_alpha_range(self):
        temporary_dir, client = self.make_client(api_key="test-secret")
        headers = {"X-API-Key": "test-secret"}
        with temporary_dir, client:
            extra_payload = self.polar_payload() | {"shell_command": "not allowed"}
            extra_response = client.post("/v1/polar", json=extra_payload, headers=headers)
            invalid_payload = self.polar_payload() | {"alpha_end": -2.0}
            invalid_response = client.post("/v1/polar", json=invalid_payload, headers=headers)
        self.assertEqual(extra_response.status_code, 422)
        self.assertEqual(invalid_response.status_code, 422)

    def test_worker_enforces_per_credential_rate_limit(self):
        temporary_dir, client = self.make_client(api_key="test-secret", requests_per_minute=1)
        headers = {"X-API-Key": "test-secret"}
        with temporary_dir, client:
            first = client.post("/v1/polar", json=self.polar_payload(), headers=headers)
            second = client.post("/v1/polar", json=self.polar_payload(), headers=headers)
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 429)

    def test_worker_rejects_oversize_body_before_json_parsing(self):
        temporary_dir, client = self.make_client(api_key="test-secret", request_body_limit_bytes=1024)
        with temporary_dir, client:
            response = client.post(
                "/v1/polar",
                content="x" * 2048,
                headers={"X-API-Key": "test-secret", "content-type": "application/json"},
            )
        self.assertEqual(response.status_code, 413)


if __name__ == "__main__":
    unittest.main()
