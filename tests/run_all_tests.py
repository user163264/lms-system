#!/usr/bin/env python3
"""
Script Name: run_all_tests.py
Description: Runs all LMS tests with different options

Usage:
    python tests/run_all_tests.py [options]
    
Options:
    --unit           Run only unit tests
    --integration    Run only integration tests
    --api            Run only API tests
    --all            Run all tests (default)
    --coverage       Generate test coverage report
    
Dependencies:
    - pytest
    - pytest-cov
    
Output:
    Test results and optional coverage report
    
Author: LMS Team
Last Modified: 2025-03-20
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run LMS tests")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--api", action="store_true", help="Run only API tests")
    parser.add_argument("--all", action="store_true", help="Run all tests (default)")
    parser.add_argument("--coverage", action="store_true", help="Generate test coverage report")
    return parser.parse_args()

def run_tests(test_type=None, coverage=False):
    """Run tests with pytest."""
    # Change to the project root directory
    os.chdir(Path(__file__).parents[1])
    
    cmd = ["python", "-m", "pytest"]
    
    # Add coverage if requested
    if coverage:
        cmd.extend([
            "--cov=backend", 
            "--cov=database", 
            "--cov-report=term", 
            "--cov-report=html:tests/coverage_html"
        ])
    
    # Add test type marker if specified
    if test_type:
        cmd.append(f"-m {test_type}")
    
    # Run the command
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode

def main():
    """Main function."""
    args = parse_args()
    
    # Determine which tests to run
    if args.unit:
        return run_tests("unit", args.coverage)
    elif args.integration:
        return run_tests("integration", args.coverage)
    elif args.api:
        return run_tests("api", args.coverage)
    else:  # Run all tests by default
        return run_tests(None, args.coverage)

if __name__ == "__main__":
    sys.exit(main()) 