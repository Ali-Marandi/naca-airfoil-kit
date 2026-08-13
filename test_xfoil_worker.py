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

    def make_client(self, api_key=""):
        temporary_dir = tempfile.TemporaryDirectory()
        settings = WorkerSettings(
            api_key=api_key,
            xfoil_executable="/not/a/real/xfoil",
            max_concurrency=1,
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

    def test_health_exposes_degraded_state_when_solver_is_missing(self):
        temporary_dir, client = self.make_client()
        with temporary_dir, client:
            response = client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "degraded")
        self.assertFalse(response.json()["xfoil_executable_available"])

    def test_polar_endpoint_requires_key_when_configured(self):
        temporary_dir, client = self.make_client(api_key="test-secret")
        with temporary_dir, client:
            denied = client.post("/v1/polar", json=self.polar_payload())
            accepted = client.post("/v1/polar", json=self.polar_payload(), headers={"X-API-Key": "test-secret"})
        self.assertEqual(denied.status_code, 401)
        self.assertEqual(accepted.status_code, 200)
        self.assertEqual(accepted.json()["status"], "executable_not_found")
        self.assertEqual(accepted.json()["solver"], "xfoil")

    def test_polar_schema_rejects_extra_field_and_invalid_alpha_range(self):
        temporary_dir, client = self.make_client()
        with temporary_dir, client:
            extra_payload = self.polar_payload() | {"shell_command": "not allowed"}
            extra_response = client.post("/v1/polar", json=extra_payload)
            invalid_payload = self.polar_payload() | {"alpha_end": -2.0}
            invalid_response = client.post("/v1/polar", json=invalid_payload)
        self.assertEqual(extra_response.status_code, 422)
        self.assertEqual(invalid_response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
