import unittest

from src.governance import Capability, assess
from src.intake import scan
from pathlib import Path


class GovernanceTests(unittest.TestCase):
    def test_empty_capabilities_can_be_adopted(self):
        self.assertEqual(assess(set()).decision, "adopt")

    def test_single_privileged_capability_requires_review(self):
        self.assertEqual(assess({Capability.BROWSER}).decision, "review")

    def test_credentials_and_network_are_rejected(self):
        result = assess({Capability.CREDENTIALS, Capability.NETWORK})
        self.assertEqual(result.decision, "reject")

    def test_shell_and_repository_write_are_rejected(self):
        result = assess({Capability.SHELL, Capability.REPOSITORY_WRITE})
        self.assertEqual(result.decision, "reject")

    def test_safe_fixture(self):
        self.assertEqual(scan(Path("examples/safe-skill")), set())

    def test_risky_fixture(self):
        capabilities = scan(Path("examples/risky-skill"))
        self.assertIn(Capability.CREDENTIALS, capabilities)
        self.assertIn(Capability.NETWORK, capabilities)
        self.assertIn(Capability.SHELL, capabilities)
        self.assertEqual(assess(capabilities).decision, "reject")


if __name__ == "__main__":
    unittest.main()
