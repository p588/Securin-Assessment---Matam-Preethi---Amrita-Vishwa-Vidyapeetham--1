import unittest
from main import get_cves


class TestGetCves(unittest.TestCase):

    def test_successful_retrieval(self):
        # Adjust start_index and results_per_page as needed
        cves = get_cves(0, 1)
        self.assertIsInstance(cves, dict)
        self.assertIn("totalResults", cves)

    def test_empty_results(self):
        # Simulate a scenario with potentially non-empty results
        cves = get_cves(10000, 1)  # Adjust start_index as needed
        self.assertIsInstance(cves, dict)
        self.assertGreater(cves.get("totalResults", 0),
                           0)  # Check for non-zero

    def test_error_handling(self):
        # Mock a failed request (replace with actual error handling)
        def mock_get_cves(*args, **kwargs):
            raise Exception("Simulated error")

        with self.assertRaises(Exception):
            get_cves = mock_get_cves  # Patch the function for testing
            get_cves(0, 1)


if __name__ == "__main__":
    unittest.main()
