import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from airfoil_pro import NACAGeneratorPro
from xfoil_adapter import XFoilAdapter, XFoilRunSpec, XFoilValidationError


POLAR_TEXT = """\n XFOIL polar\n\n  alpha     CL        CD       CDp       CM    Top_Xtr Bot_Xtr\n -------- -------- --------- -------- -------- -------- --------\n  -2.000  -0.2200   0.00800  0.00400  -0.0010 0.8500   0.9000\n   0.000   0.0000   0.00700  0.00320   0.0000 0.7500   0.8000\n   2.000   0.2200   0.00810  0.00410  -0.0010 0.6500   0.7000\n"""


class XFoilAdapterTests(unittest.TestCase):
    def setUp(self):
        self.coords = NACAGeneratorPro.naca4("0012", 30)
        self.spec = XFoilRunSpec.from_surfaces(
            "NACA 0012",
            *self.coords,
            reynolds=100_000,
            alpha_start=-2.0,
            alpha_end=2.0,
            alpha_step=2.0,
        )

    def test_build_batch_commands_is_allowlisted(self):
        hostile = XFoilRunSpec.from_surfaces(
            "NACA 0012; QUIT; ! arbitrary command",
            *self.coords,
            reynolds=100_000,
            alpha_start=-2.0,
            alpha_end=2.0,
            alpha_step=2.0,
        )
        commands = XFoilAdapter.build_batch_commands(hostile)
        self.assertIn("LOAD airfoil.dat", commands)
        self.assertIn("PACC\npolar.txt", commands)
        self.assertIn("ASEQ -2 2 2", commands)
        self.assertNotIn("arbitrary", commands)
        self.assertNotIn("NACA 0012", commands)

    def test_rejects_unsafe_sweep(self):
        bad_spec = XFoilRunSpec.from_surfaces(
            "NACA 0012",
            *self.coords,
            reynolds=100_000,
            alpha_start=-30.0,
            alpha_end=30.0,
            alpha_step=0.05,
        )
        with self.assertRaises(XFoilValidationError):
            bad_spec.validate()

    def test_parser_reads_standard_polar_columns(self):
        rows = XFoilAdapter.parse_polar_text(POLAR_TEXT)
        self.assertEqual(len(rows), 3)
        self.assertAlmostEqual(rows[0]["alpha_deg"], -2.0)
        self.assertAlmostEqual(rows[1]["cd"], 0.007)
        self.assertAlmostEqual(rows[2]["bottom_xtr"], 0.7)
        self.assertTrue(rows[0]["converged"])

    def test_run_uses_disposable_directory_and_shell_false(self):
        with tempfile.TemporaryDirectory() as temporary_root:
            adapter = XFoilAdapter("/bin/echo", temp_root=temporary_root)

            def fake_run(args, **kwargs):
                self.assertEqual(args, ["/bin/echo"])
                self.assertFalse(kwargs["shell"])
                self.assertEqual(Path(kwargs["cwd"]).parent, Path(temporary_root))
                self.assertIn("ASEQ -2 2 2", kwargs["input"])
                (Path(kwargs["cwd"]) / "polar.txt").write_text(POLAR_TEXT, encoding="utf-8")
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="ok", stderr="")

            with patch("xfoil_adapter.subprocess.run", side_effect=fake_run):
                result = adapter.run(self.spec)
            self.assertTrue(result.completed)
            self.assertEqual(len(result.rows), 3)
            self.assertEqual(list(Path(temporary_root).iterdir()), [])
            self.assertEqual(result.manifest["command_policy"], "allowlisted-batch-only")

    def test_missing_executable_is_reported_without_execution(self):
        adapter = XFoilAdapter("definitely-not-an-xfoil-binary")
        result = adapter.run(self.spec)
        self.assertEqual(result.status, "executable_not_found")
        self.assertFalse(result.completed)


if __name__ == "__main__":
    unittest.main()
