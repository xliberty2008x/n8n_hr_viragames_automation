#!/usr/bin/env python3
"""
Script to check BambooHR employee and their uploaded files
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/config.env')

# Get BambooHR credentials
bamboohr_domain = os.getenv('BAMBOOHR_COMPANY_DOMAIN')
bamboohr_api_key = os.getenv('BAMBOOHR_API_KEY')

if not bamboohr_domain or not bamboohr_api_key:
    print("❌ BambooHR credentials not found in config/config.env")
    sys.exit(1)

# Setup session
session = requests.Session()
session.auth = (bamboohr_api_key, 'x')
session.headers.update({
    'Accept': 'application/json',
    'Content-Type': 'application/json'
})

bamboohr_base_url = f"https://{bamboohr_domain}.bamboohr.com/api/v1"

def get_employee_with_fields(employee_id):
    """Get employee details with specific fields from BambooHR"""
    url = f"{bamboohr_base_url}/employees/{employee_id}"
    params = {
        'fields': 'firstName,lastName,workEmail,jobTitle,department,hireDate'
    }
    response = session.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to get employee with fields: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def list_employee_files(employee_id):
    """List employee files using the correct endpoint"""
    url = f"{bamboohr_base_url}/employees/{employee_id}/files/view"
    response = session.get(url)
    
    print(f"List files response status: {response.status_code}")
    print(f"List files response: {response.text}")
    
    return response.status_code == 200

def test_file_upload(employee_id):
    """Test file upload to BambooHR"""
    url = f"{bamboohr_base_url}/employees/{employee_id}/files"
    
    # Create a simple test file
    test_content = "This is a test file for BambooHR upload"
    files = {
        'file': ('test.txt', test_content, 'text/plain')
    }
    
    data = {
        'category': 'Documents',
        'name': 'test.txt'
    }
    
    print(f"Testing file upload to: {url}")
    response = session.post(url, files=files, data=data)
    
    print(f"Upload response status: {response.status_code}")
    print(f"Upload response: {response.text}")
    
    return response.status_code == 201

def main():
    # Test with the latest employee ID (297)
    employee_id = 297
    
    print(f"Checking BambooHR Employee {employee_id}")
    print("=" * 40)
    
    # Get employee details with fields
    print("Getting employee details with fields...")
    employee_with_fields = get_employee_with_fields(employee_id)
    
    if employee_with_fields:
        print("✅ Employee with fields found:")
        print(f"  Raw employee data: {json.dumps(employee_with_fields, indent=2)}")
        print()
    
    # Test file listing
    print("Testing file listing...")
    list_success = list_employee_files(employee_id)
    
    if list_success:
        print("✅ File listing successful!")
    else:
        print("❌ File listing failed!")
    
    # Test file upload
    print("\nTesting file upload...")
    upload_success = test_file_upload(employee_id)
    
    if upload_success:
        print("✅ File upload test successful!")
    else:
        print("❌ File upload test failed!")
    
    print("\nCheck completed!")

if __name__ == "__main__":
    main() 