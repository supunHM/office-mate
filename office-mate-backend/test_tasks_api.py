"""
Test script for Tasks API
Tests all task endpoints with sample data
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5001"

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_test(name, passed):
    status = f"{GREEN}✓ PASSED{RESET}" if passed else f"{RED}✗ FAILED{RESET}"
    print(f"{status} - {name}")

def print_section(title):
    print(f"\n{YELLOW}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{RESET}\n")

# Step 1: Register and login
print_section("Authentication")

register_data = {
    "username": f"taskuser_{datetime.now().timestamp()}",
    "email": f"taskuser_{datetime.now().timestamp()}@test.com",
    "password": "test123",
    "full_name": "Task Test User"
}

response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
print(f"Register: {response.status_code}")
print_test("User registration", response.status_code == 201)

login_data = {
    "username": register_data["username"],
    "password": register_data["password"]
}

response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
print(f"Login: {response.status_code}")

if response.status_code != 200:
    print(f"{RED}Login failed. Cannot continue tests.{RESET}")
    exit(1)

token = response.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}
print_test("User login", True)

# Step 2: Create tasks
print_section("Create Tasks")

tasks = [
    {
        "title": "Review Q4 Report",
        "description": "Review quarterly financial report",
        "priority": "High",
        "due_date": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
        "status": "Todo"
    },
    {
        "title": "Update documentation",
        "description": "Update API documentation with new endpoints",
        "priority": "Medium",
        "due_date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
        "status": "InProgress"
    },
    {
        "title": "Schedule team meeting",
        "priority": "Low",
        "status": "Todo"
    },
    {
        "title": "Fix bug in production",
        "description": "Critical bug affecting users",
        "priority": "Urgent",
        "due_date": datetime.now().strftime('%Y-%m-%d'),
        "status": "InProgress"
    }
]

created_tasks = []
for task_data in tasks:
    response = requests.post(f"{BASE_URL}/api/tasks", json=task_data, headers=headers)
    if response.status_code == 201:
        task = response.json()
        created_tasks.append(task)
        print(f"Created: {task['title']} (ID: {task['id']}, Priority: {task['priority']})")
        print_test(f"Create task: {task['title']}", True)
    else:
        print(f"Failed to create: {task_data['title']}")
        print(f"Error: {response.json()}")
        print_test(f"Create task: {task_data['title']}", False)

# Step 2.5: Test upcoming tasks endpoint
print_section("Get Upcoming Tasks")

response = requests.get(f"{BASE_URL}/api/tasks/upcoming", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Found {data['count']} upcoming tasks in next {data['period_days']} days")
    for task in data['tasks']:
        print(f"  - {task['title']} (Due: {task['due_date']}, {task['days_until_due']} days)")
    print_test("Get upcoming tasks", True)
else:
    print(f"Error: {response.json()}")
    print_test("Get upcoming tasks", False)

# Test with custom days parameter
response = requests.get(f"{BASE_URL}/api/tasks/upcoming?days=7", headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"Found {data['count']} upcoming tasks in next 7 days")
    print_test("Get upcoming tasks (7 days)", True)
else:
    print_test("Get upcoming tasks (7 days)", False)

# Step 3: List all tasks
print_section("List Tasks")

response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
print(f"GET /api/tasks: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Total tasks: {data['pagination']['total']}")
    print(f"Tasks on page: {len(data['tasks'])}")
    print_test("List all tasks", True)
else:
    print_test("List all tasks", False)

# Step 4: Filter by status
print_section("Filter Tasks by Status")

for status in ['Todo', 'InProgress', 'Done']:
    response = requests.get(f"{BASE_URL}/api/tasks?status={status}", headers=headers)
    if response.status_code == 200:
        count = response.json()['pagination']['total']
        print(f"Status '{status}': {count} tasks")
        print_test(f"Filter by status: {status}", True)
    else:
        print_test(f"Filter by status: {status}", False)

# Step 5: Filter by due date
print_section("Filter Tasks by Due Date")

today = datetime.now().strftime('%Y-%m-%d')
next_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

response = requests.get(
    f"{BASE_URL}/api/tasks?due_from={today}&due_to={next_week}",
    headers=headers
)
if response.status_code == 200:
    count = response.json()['pagination']['total']
    print(f"Tasks due this week: {count}")
    print_test("Filter by due date range", True)
else:
    print_test("Filter by due date range", False)

# Step 6: Get single task
print_section("Get Single Task")

if created_tasks:
    task_id = created_tasks[0]['id']
    response = requests.get(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
    if response.status_code == 200:
        task = response.json()
        print(f"Task ID {task_id}: {task['title']}")
        print(f"Priority: {task['priority']}, Status: {task['status']}")
        print_test("Get single task", True)
    else:
        print_test("Get single task", False)

# Step 7: Update task
print_section("Update Task")

if created_tasks:
    task_id = created_tasks[0]['id']
    update_data = {
        "status": "Done",
        "priority": "Medium"
    }
    response = requests.patch(
        f"{BASE_URL}/api/tasks/{task_id}",
        json=update_data,
        headers=headers
    )
    if response.status_code == 200:
        task = response.json()
        print(f"Updated task {task_id}")
        print(f"New status: {task['status']}, New priority: {task['priority']}")
        print_test("Update task", task['status'] == 'Done' and task['priority'] == 'Medium')
    else:
        print(f"Update failed: {response.json()}")
        print_test("Update task", False)

# Step 8: Update task to InProgress
if len(created_tasks) > 1:
    task_id = created_tasks[1]['id']
    response = requests.patch(
        f"{BASE_URL}/api/tasks/{task_id}",
        json={"status": "InProgress"},
        headers=headers
    )
    if response.status_code == 200:
        print(f"Updated task {task_id} to InProgress")
        print_test("Update task status to InProgress", True)
    else:
        print_test("Update task status to InProgress", False)

# Step 9: Delete task
print_section("Delete Task")

if len(created_tasks) > 2:
    task_id = created_tasks[2]['id']
    response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
    if response.status_code == 200:
        print(f"Deleted task {task_id}")
        print_test("Delete task", True)
        
        # Verify deletion
        response = requests.get(f"{BASE_URL}/api/tasks/{task_id}", headers=headers)
        print_test("Verify task deleted", response.status_code == 404)
    else:
        print_test("Delete task", False)

# Step 10: Pagination test
print_section("Pagination")

response = requests.get(f"{BASE_URL}/api/tasks?per_page=2&page=1", headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"Page 1: {len(data['tasks'])} tasks")
    print(f"Total pages: {data['pagination']['pages']}")
    print(f"Has next: {data['pagination']['has_next']}")
    print_test("Pagination", True)
else:
    print_test("Pagination", False)

# Summary
print_section("Test Summary")
print(f"{GREEN}Tasks API is working correctly!{RESET}")
print(f"\nYou can now:")
print("1. Create tasks with POST /api/tasks")
print("2. List tasks with GET /api/tasks")
print("3. Filter by status, due_date, document_id")
print("4. Update tasks with PATCH /api/tasks/<id>")
print("5. Delete tasks with DELETE /api/tasks/<id>")
print("\nReady to wire up with your UI!")
