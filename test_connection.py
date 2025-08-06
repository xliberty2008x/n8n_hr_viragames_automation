#!/usr/bin/env python3
"""
Simple test script for BambooHR API client
"""

from src.bamboohr_client import BambooHRClient
import json


def test_basic_connection():
    """Test basic connection to BambooHR API"""
    print("Testing BambooHR API Connection")
    print("=" * 50)
    
    try:
        # Initialize client
        client = BambooHRClient()
        print("✓ Client initialized successfully")
        
        # Test connection
        result = client.test_connection()
        
        if result["success"]:
            print("✓ API connection successful!")
            if "company_info" in result:
                company = result["company_info"]
                print(f"  Company: {company.get('displayName', 'N/A')}")
                print(f"  Legal Name: {company.get('legalName', 'N/A')}")
                print(f"  Phone: {company.get('phone', 'N/A')}")
        else:
            print("✗ API connection failed!")
            print(f"  Error: {result.get('message', 'Unknown error')}")
            if "status_code" in result:
                print(f"  Status Code: {result['status_code']}")
            if "response_text" in result:
                print(f"  Response: {result['response_text']}")
                
    except Exception as e:
        print(f"✗ Error: {e}")


def test_employee_retrieval():
    """Test retrieving employee data"""
    print("\nTesting Employee Data Retrieval")
    print("=" * 50)
    
    try:
        client = BambooHRClient()
        
        # Get basic employee information
        result = client.get_employees()
        
        if result["success"]:
            employees = result["employees"]
            print(f"✓ Retrieved {len(employees)} employees")
            
            if employees:
                print("\nFirst 3 employees:")
                for i, emp in enumerate(employees[:3]):
                    print(f"  {i+1}. {emp.get('firstName', 'N/A')} {emp.get('lastName', 'N/A')} - {emp.get('jobTitle', 'N/A')}")
        else:
            print(f"✗ Failed to get employees: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def test_time_tracking():
    """Test time tracking functionality"""
    print("\nTesting Time Tracking")
    print("=" * 50)
    
    try:
        client = BambooHRClient()
        
        # Get time tracking projects
        result = client.get_time_tracking_projects()
        
        if result["success"]:
            projects = result["projects"]
            print(f"✓ Retrieved {len(projects)} time tracking projects")
            
            if projects:
                print("\nAvailable projects:")
                for i, project in enumerate(projects[:5]):  # Show first 5 projects
                    print(f"  {i+1}. {project.get('name', 'N/A')} (Billable: {project.get('billable', 'N/A')})")
        else:
            print(f"✗ Failed to get time tracking projects: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def test_webhooks():
    """Test webhook functionality"""
    print("\nTesting Webhooks")
    print("=" * 50)
    
    try:
        client = BambooHRClient()
        
        # Get webhooks
        result = client.get_webhooks()
        
        if result["success"]:
            webhooks_data = result["webhooks"]
            webhooks = webhooks_data.get('webhooks', [])
            print(f"✓ Retrieved {len(webhooks)} webhooks")
            
            if webhooks:
                print("\nConfigured webhooks:")
                for i, webhook in enumerate(webhooks[:3]):  # Show first 3 webhooks
                    print(f"  {i+1}. {webhook.get('name', 'N/A')} - {webhook.get('url', 'N/A')}")
            else:
                print("  No webhooks configured")
        else:
            print(f"✗ Failed to get webhooks: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Run all tests"""
    test_basic_connection()
    test_employee_retrieval()
    test_time_tracking()
    test_webhooks()
    
    print("\n" + "=" * 50)
    print("All tests completed!")


if __name__ == "__main__":
    main() 