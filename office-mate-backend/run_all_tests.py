#!/usr/bin/env python
"""
Comprehensive test suite for Office Mate Backend
Runs all tests sequentially and generates a report
"""
import subprocess
import sys
import time
from datetime import datetime

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ️  {text}{RESET}")

def run_test(test_file, description):
    """Run a single test file and capture results"""
    print(f"\n{BOLD}Running: {description}{RESET}")
    print(f"File: {test_file}")
    print("-" * 70)
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            timeout=30,
            capture_output=True,
            text=True
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"{YELLOW}Stderr:{RESET}\n{result.stderr}")
        
        # Check result
        if result.returncode == 0:
            print_success(f"{description} completed")
            return True, result.stdout
        else:
            print_error(f"{description} failed with code {result.returncode}")
            return False, result.stdout
            
    except subprocess.TimeoutExpired:
        print_error(f"{description} timed out (>30 seconds)")
        return False, "Timeout"
    except Exception as e:
        print_error(f"{description} error: {str(e)}")
        return False, str(e)

def main():
    print_header(f"🧪 OFFICE MATE BACKEND TEST SUITE\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if server is running
    print("Checking Flask server...")
    result = subprocess.run(
        ["curl", "-s", "http://localhost:8000/"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print_error("Flask server is not running on http://localhost:8000/")
        print_info("Starting Flask server...")
        subprocess.Popen(
            [sys.executable, "flask_app.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(4)
    else:
        print_success("Flask server is running")
        print(f"Response: {result.stdout[:100]}")
    
    # List of tests to run
    tests = [
        ("test_auth.py", "Authentication API Tests"),
        ("test_flask_api.py", "Flask API Tests"),
        ("test_search_api.py", "Document Search API Tests"),
        ("test_tasks_api.py", "Task Management API Tests"),
        ("test_task_api_complete.py", "Complete Task API Tests"),
        ("test_model.py", "Model Validation Tests"),
    ]
    
    # Run all tests
    results = []
    for test_file, description in tests:
        success, output = run_test(test_file, description)
        results.append({
            'file': test_file,
            'description': description,
            'success': success,
            'output': output
        })
        time.sleep(1)  # Brief pause between tests
    
    # Print summary
    print_header("📊 TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for r in results if r['success'])
    failed = total - passed
    
    for result in results:
        status = f"{GREEN}PASS{RESET}" if result['success'] else f"{RED}FAIL{RESET}"
        print(f"{status} - {result['description']}")
    
    print(f"\n{BOLD}Total: {total} | {GREEN}Passed: {passed}{RESET} | {RED}Failed: {failed}{RESET}")
    
    # Overall result
    print_header("✨ FINAL RESULT")
    if failed == 0:
        print_success(f"All {passed} tests passed! 🎉")
        print_info("Backend is ready for deployment")
        return 0
    else:
        print_error(f"{failed} test(s) failed")
        print_info("Review the errors above and fix issues before deployment")
        return 1

if __name__ == "__main__":
    sys.exit(main())
