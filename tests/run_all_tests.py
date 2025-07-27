#!/usr/bin/env python3
"""
Test runner for the Ultimate AI Personal Assistant.
Runs all tests in the organized test structure.
"""

import sys
import os
import subprocess
import unittest
from pathlib import Path

def discover_and_run_tests():
    """Discover and run all tests in the test directories."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    tests_dir = project_root / 'tests'
    
    # Add the project root to Python path so imports work
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(project_root / 'src'))
    
    # Discover tests in each category
    test_categories = ['unit', 'integration', 'api', 'debug']
    all_tests = unittest.TestSuite()
    
    for category in test_categories:
        category_dir = tests_dir / category
        if category_dir.exists():
            print(f"🔍 Discovering tests in {category}/...")
            loader = unittest.TestLoader()
            suite = loader.discover(str(category_dir), pattern='test_*.py')
            all_tests.addTests(suite)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(all_tests)
    
    return result.wasSuccessful()

def main():
    """Main test runner function."""
    print("🧪 Running Ultimate AI Personal Assistant Tests")
    print("=" * 50)
    
    success = discover_and_run_tests()
    
    print("=" * 50)
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 