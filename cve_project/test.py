import unittest
from main import get_cves


class TestGetCves(unittest.TestCase):

    def test_successful_retrieval(self):
        # Adjust start_index and results_per_page as needed
        cves = get_cves(0, 1)
        self.assertIsInstance(cves, dict)
        self.assertIn("totalResults", cves)

    # Add more test cases for different scenarios (e.g., error handling)


if __name__ == "__main__":
    unittest.main()
