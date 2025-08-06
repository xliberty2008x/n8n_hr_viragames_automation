#!/usr/bin/env python3
"""
Script to list and delete test employees created during integration testing
"""

import os
import sys
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/config.env')

# BambooHR configuration
BAMBOOHR_API_KEY = os.getenv('BAMBOOHR_API_KEY')
BAMBOOHR_DOMAIN = os.getenv('BAMBOOHR_COMPANY_DOMAIN')

if not BAMBOOHR_API_KEY or not BAMBOOHR_DOMAIN:
    print("Error: Missing BambooHR API credentials in config/config.env")
    sys.exit(1)

# Base URL for BambooHR API
BASE_URL = f"https://api.bamboohr.com/api/gateway.php/{BAMBOOHR_DOMAIN}/v1"

# Authentication
auth = HTTPBasicAuth(BAMBOOHR_API_KEY, 'x')

def get_employee_by_email(email):
    """Get employee details by email"""
    url = f"{BASE_URL}/employees/directory"
    headers = {'Accept': 'application/json'}
    
    response = requests.get(url, auth=auth, headers=headers)
    
    if response.status_code == 200:
        employees = response.json().get('employees', [])
        
        # Search for employee with matching email
        for employee in employees:
            if employee.get('workEmail') == email:
                return employee
    
    return None

def get_employee_by_id(employee_id):
    """Get employee details by ID"""
    url = f"{BASE_URL}/employees/{employee_id}"
    headers = {'Accept': 'application/json'}
    
    response = requests.get(url, auth=auth, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    
    return None

def delete_employee(employee_id):
    """Delete an employee by ID"""
    url = f"{BASE_URL}/employees/{employee_id}"
    
    response = requests.delete(url, auth=auth)
    
    return response.status_code == 200

def main():
    print("BambooHR Test Employee Cleanup")
    print("=" * 50)
    
    # Test employee IDs from the integration tests
    test_employee_ids = [301, 302, 304]
    test_email = "irynamunchak02@gmail.com"
    
    print(f"\nChecking for test employees...")
    print(f"Test email: {test_email}")
    print(f"Known test employee IDs: {test_employee_ids}")
    
    # Check by email first
    print(f"\nSearching for employee with email: {test_email}")
    employee = get_employee_by_email(test_email)
    
    if employee:
        print(f"Found employee: {employee.get('displayName')} (ID: {employee.get('id')})")
        test_employee_ids.append(int(employee.get('id')))
    else:
        print(f"No employee found with email: {test_email}")
    
    # Check all test employee IDs
    found_employees = []
    print(f"\nChecking employee IDs: {list(set(test_employee_ids))}")
    
    for emp_id in set(test_employee_ids):
        employee = get_employee_by_id(emp_id)
        if employee:
            found_employees.append({
                'id': emp_id,
                'name': f"{employee.get('firstName', '')} {employee.get('lastName', '')}",
                'email': employee.get('workEmail', 'N/A')
            })
            print(f"  - ID {emp_id}: {employee.get('firstName')} {employee.get('lastName')} ({employee.get('workEmail')})")
        else:
            print(f"  - ID {emp_id}: Not found")
    
    if not found_employees:
        print("\nNo test employees found to delete.")
        return
    
    # Ask for confirmation
    print(f"\nFound {len(found_employees)} test employee(s) to delete:")
    for emp in found_employees:
        print(f"  - {emp['name']} (ID: {emp['id']}, Email: {emp['email']})")
    
    confirm = input("\nDo you want to delete these employees? (yes/no): ").lower()
    
    if confirm == 'yes':
        print("\nDeleting employees...")
        for emp in found_employees:
            if delete_employee(emp['id']):
                print(f"  ✓ Deleted: {emp['name']} (ID: {emp['id']})")
            else:
                print(f"  ✗ Failed to delete: {emp['name']} (ID: {emp['id']})")
    else:
        print("\nDeletion cancelled.")

if __name__ == "__main__":
    main()