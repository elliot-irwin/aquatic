import subprocess
import sys
import pytest


def run_tests():
    """Run pytest and additional checks"""
    # Run pytest
    pytest_result = pytest.main(['-v', 'weather_test.py'])
    
    # Additional checks can be added here
    return pytest_result == 0


def run_linters():
    """Run code quality checks"""
    try:
        # You might need to install these: pip install flake8 pylint
        subprocess.run([sys.executable, '-m', 'flake8', '.'], check=True)
        subprocess.run([sys.executable, '-m', 'pylint', '.'], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Linting failed")
        return False


def main():
    """Main entry point for test and lint operations"""
    print("Running tests...")
    tests_passed = run_tests()
    
    print("Running linters...")
    linters_passed = run_linters()
    
    if tests_passed and linters_passed:
        print("All checks passed!")
        sys.exit(0)
    else:
        print("Some checks failed.")
        sys.exit(1)


if __name__ == '__main__':
    main()
