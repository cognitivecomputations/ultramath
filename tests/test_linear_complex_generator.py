import unittest
import sys
import os
import random
from fractions import Fraction # Needed for checking final answer type

# Add parent directory to path to allow importing 'arithmetic' modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir) # Go up two levels
if grandparent_dir not in sys.path:
    sys.path.insert(0, grandparent_dir)

from arithmetic.generators.linear_complex_generator import LinearComplexGenerator
from arithmetic.helpers import DELIM

class TestLinearComplexGenerator(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.generator = LinearComplexGenerator()
        # random.seed(50) # Optional: for predictable tests

    def test_generate_output_format(self):
        """Test the output format of the generate method."""
        result = self.generator.generate()

        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIsInstance(result["problem_id"], str)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "linear_eq_complex")
        self.assertIn("problem", result)
        self.assertIsInstance(result["problem"], str)
        self.assertIn("steps", result)
        self.assertIsInstance(result["steps"], list)
        self.assertGreater(len(result["steps"]), 0, "Steps list should not be empty")
        self.assertIn("final_answer", result)
        self.assertIsInstance(result["final_answer"], str)

        # Check the final step format
        final_step = result["steps"][-1]
        self.assertTrue(final_step.startswith(f"Z{DELIM}"), f"Final step should start with Z{DELIM}")
        # Check if final answer in step matches the final_answer field
        self.assertEqual(final_step.split(DELIM)[1], result["final_answer"])

    def test_generate_consistency(self):
        """Generate multiple examples and check basic consistency."""
        for _ in range(10): # Generate a few examples
            result = self.generator.generate()
            # Re-run basic format checks
            self.assertIsInstance(result, dict)
            self.assertIn("problem_id", result)
            self.assertIn("operation", result)
            self.assertIn("problem", result)
            self.assertIn("steps", result)
            self.assertIn("final_answer", result)
            self.assertGreater(len(result["steps"]), 0)
            self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
            self.assertEqual(result["steps"][-1].split(DELIM)[1], result["final_answer"])

            # Check if problem string looks reasonable
            self.assertIn("Solve:", result["problem"])
            self.assertIn("=", result["problem"])
            self.assertIn("x", result["problem"]) # Should contain x

            # Check if final answer looks reasonable (starts with x=)
            self.assertTrue(result["final_answer"].startswith("x="))
            # Check if the value part is a valid fraction string
            try:
                Fraction(result["final_answer"].split('=')[1])
            except (ValueError, ZeroDivisionError):
                self.fail(f"Final answer value '{result['final_answer'].split('=')[1]}' is not a valid Fraction string.")


if __name__ == '__main__':
    unittest.main()
