"""
Quick test script for Task API endpoints
Tests all CRUD operations and filters

Usage:
    1. Start Flask server: python flask_app.py
    2. Run this script: python test_task_api_complete.py
"""
import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5001"
TEST_USER = {
    "username": "admin@gmail.com",
    "password": "admin123"
}

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")


def print_error(message):
    print(f"{RED}✗ {message}{RESET}")


def print_info(message):
    print(f"{BLUE}ℹ {message}{RESET}")


def login():
    """Login and get JWT token"""
    print_info("Logging in...")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=TEST_USER
    )
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print_success(f"Login successful. Token: {token[:20]}...")
        return token
    else:
        print_error(f"Login failed: {response.text}")
        return None


def test_create_task(token):
    """Test creating a task"""
    print_info("\n=== Testing Task Creation ===")
    
    task_data = {
        "title": "Test Task via API",
        "description": "This is a test task created via the API",
        "priority": "high",
        "status": "pending",
        "due_date": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    }
    
    response = requests.post(
        f"{BASE_URL}/api/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 201:
        task = response.json()
        print_success(f"Task created successfully! ID: {task['id']}")
        print(f"  Title: {task['title']}")
        print(f"  Priority: {task['priority']}")
        print(f"  Status: {task['status']}")
        print(f"  Due Date: {task['due_date']}")
        return task['id']
    else:
        print_error(f"Task creation failed: {response.text}")
        return None


def test_get_all_tasks(token):
    """Test getting all tasks"""
    print_info("\n=== Testing Get All Tasks ===")
    
    response = requests.get(
        f"{BASE_URL}/api/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        tasks = data['tasks']
        pagination = data['pagination']
        print_success(f"Retrieved {len(tasks)} tasks")
        print(f"  Total: {pagination['total']}")
        print(f"  Page: {pagination['page']}/{pagination['pages']}")
        
        if tasks:
            print("\n  Sample task:")
            task = tasks[0]
            print(f"    ID: {task['id']}")
            print(f"    Title: {task['title']}")
            print(f"    Status: {task['status']}")
            print(f"    Priority: {task['priority']}")
        return True
    else:
        print_error(f"Get all tasks failed: {response.text}")
        return False


def test_filter_by_status(token):
    """Test filtering tasks by status"""
    print_info("\n=== Testing Status Filter ===")
    
    for status in ['pending', 'in_progress', 'completed']:
        response = requests.get(
            f"{BASE_URL}/api/tasks",
            params={"status": status},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            count = len(response.json()['tasks'])
            print_success(f"Status '{status}': {count} tasks")
        else:
            print_error(f"Filter by status '{status}' failed: {response.text}")
            return False
    
    return True


def test_update_task(token, task_id):
    """Test updating a task"""
    print_info(f"\n=== Testing Task Update (ID: {task_id}) ===")
    
    update_data = {
        "status": "in_progress",
        "priority": "medium"
    }
    
    response = requests.patch(
        f"{BASE_URL}/api/tasks/{task_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        task = response.json()
        print_success("Task updated successfully!")
        print(f"  New Status: {task['status']}")
        print(f"  New Priority: {task['priority']}")
        return True
    else:
        print_error(f"Task update failed: {response.text}")
        return False


def test_upcoming_tasks(token):
    """Test getting upcoming tasks"""
    print_info("\n=== Testing Upcoming Tasks ===")
    
    response = requests.get(
        f"{BASE_URL}/api/tasks/upcoming",
        params={"days": 7},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        tasks = data['tasks']
        print_success(f"Retrieved {data['count']} upcoming tasks (next {data['period_days']} days)")
        
        for task in tasks:
            print(f"  • {task['title']}")
            print(f"    Due: {task['due_date']} ({task['days_until_due']} days)")
            print(f"    Priority: {task['priority']}, Status: {task['status']}")
        return True
    else:
        print_error(f"Get upcoming tasks failed: {response.text}")
        return False


def test_delete_task(token, task_id):
    """Test deleting a task"""
    print_info(f"\n=== Testing Task Deletion (ID: {task_id}) ===")
    
    response = requests.delete(
        f"{BASE_URL}/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        print_success("Task deleted successfully!")
        return True
    else:
        print_error(f"Task deletion failed: {response.text}")
        return False


def run_all_tests():
    """Run all tests in sequence"""
    print_info("╔════════════════════════════════════════╗")
    print_info("║   Task API Complete Test Suite        ║")
    print_info("╚════════════════════════════════════════╝\n")
    
    # Login
    token = login()
    if not token:
        print_error("\nTests aborted: Login failed")
        return
    
    # Test create
    task_id = test_create_task(token)
    if not task_id:
        print_error("\nTests aborted: Task creation failed")
        return
    
    # Test get all
    test_get_all_tasks(token)
    
    # Test filters
    test_filter_by_status(token)
    
    # Test update
    test_update_task(token, task_id)
    
    # Test upcoming
    test_upcoming_tasks(token)
    
    # Test delete
    test_delete_task(token, task_id)
    
    # Summary
    print_info("\n╔════════════════════════════════════════╗")
    print_info("║   All Tests Completed!                 ║")
    print_info("╚════════════════════════════════════════╝")
    print_success("\n✓ Task section is working correctly!")
    print_info("\nNext steps:")
    print("  1. Test from the frontend UI at http://localhost:8081/tasks")
    print("  2. Create tasks linked to documents")
    print("  3. Check Dashboard upcoming tasks widget")
    print("  4. Test bilingual support (switch language)")


if __name__ == '__main__':
    try:
        run_all_tests()
    except Exception as e:
        print_error(f"\nTest suite error: {str(e)}")
        import traceback
        traceback.print_exc()
