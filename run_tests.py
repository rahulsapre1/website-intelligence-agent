#!/usr/bin/env python3
"""
Test runner script for the Website Intelligence Agent
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🧪 {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings/Info:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def main():
    """Run all tests."""
    print("🚀 Website Intelligence Agent - Test Suite")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Install test dependencies if needed
    if not os.path.exists("venv"):
        print("❌ Virtual environment not found. Please run './start.sh' first")
        sys.exit(1)
    
    tests_passed = []
    
    # Run unit tests
    tests_passed.append(run_command(
        "source venv/bin/activate && python -m pytest tests/unit/ -v --tb=short",
        "Running Unit Tests"
    ))
    
    # Run integration tests
    tests_passed.append(run_command(
        "source venv/bin/activate && python -m pytest tests/integration/ -v --tb=short",
        "Running Integration Tests"
    ))
    
    # Run all tests with coverage (optional)
    try:
        tests_passed.append(run_command(
            "source venv/bin/activate && python -m pytest tests/ --cov=app --cov-report=term-missing",
            "Running Tests with Coverage"
        ))
    except:
        print("⚠️  Coverage not available, skipping coverage report")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    if all(tests_passed):
        print("✅ All tests passed!")
        print("🎉 Test suite completed successfully")
        return 0
    else:
        print("❌ Some tests failed!")
        print("🔧 Please check the output above for details")
        return 1


if __name__ == "__main__":
    sys.exit(main())
