#!/usr/bin/env python3
"""
Example usage of the BambooHR Python client
"""

from src.bamboohr_client import BambooHRClient
import json


def example_basic_usage():
    """Example of basic client usage"""
    print("=== Basic Client Usage ===")
    
    # Initialize the client
    client = BambooHRClient()
    
    # Test the connection
    connection_result = client.test_connection()
    
    if connection_result["success"]:
        print("✅ Connection successful!")
        company_info = connection_result["company_info"]
        print(f"Company: {company_info.get('displayName', 'N/A')}")
        print(f"Legal Name: {company_info.get('legalName', 'N/A')}")
        print(f"Phone: {company_info.get('phone', 'N/A')}")
    else:
        print("❌ Connection failed!")
        print(f"Error: {connection_result.get('message', 'Unknown error')}")
        return False
    
    return True


def example_webhooks():
    """Example of working with webhooks"""
    print("\n=== Webhooks Example ===")
    
    client = BambooHRClient()
    result = client.get_webhooks()
    
    if result["success"]:
        webhooks_data = result["webhooks"]
        webhooks = webhooks_data.get('webhooks', [])
        
        if webhooks:
            print(f"Found {len(webhooks)} webhooks:")
            for i, webhook in enumerate(webhooks):
                print(f"  {i+1}. {webhook.get('name', 'N/A')}")
                print(f"     URL: {webhook.get('url', 'N/A')}")
                print(f"     Created: {webhook.get('created', 'N/A')}")
        else:
            print("No webhooks configured")
    else:
        print(f"Failed to get webhooks: {result.get('message', 'Unknown error')}")


def example_datasets():
    """Example of working with datasets"""
    print("\n=== Datasets Example ===")
    
    client = BambooHRClient()
    result = client.get_datasets()
    
    if result["success"]:
        datasets_data = result["datasets"]
        datasets = datasets_data.get('datasets', [])
        
        if datasets:
            print(f"Found {len(datasets)} datasets:")
            for i, dataset in enumerate(datasets):
                print(f"  {i+1}. {dataset.get('name', 'N/A')}")
                print(f"     Label: {dataset.get('label', 'N/A')}")
        else:
            print("No datasets available")
    else:
        print(f"Failed to get datasets: {result.get('message', 'Unknown error')}")


def example_timesheet_entries():
    """Example of getting timesheet entries"""
    print("\n=== Timesheet Entries Example ===")
    
    client = BambooHRClient()
    
    # Get timesheet entries for the last 30 days
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    result = client.get_timesheet_entries(
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d')
    )
    
    if result["success"]:
        entries = result["timesheet_entries"]
        print(f"Retrieved timesheet entries for {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        print(f"Found {len(entries)} entries")
    else:
        print(f"Failed to get timesheet entries: {result.get('message', 'Unknown error')}")


def example_error_handling():
    """Example of error handling"""
    print("\n=== Error Handling Example ===")
    
    client = BambooHRClient()
    
    # Try to get employees (this might fail due to permissions)
    result = client.get_employees()
    
    if result["success"]:
        print("✅ Successfully retrieved employee directory")
    else:
        print("❌ Failed to retrieve employees")
        print(f"   Error: {result.get('message', 'Unknown error')}")
        print(f"   Status Code: {result.get('status_code', 'N/A')}")
        
        # Check if there's a note about the endpoint
        if "note" in result:
            print(f"   Note: {result['note']}")


def main():
    """Run all examples"""
    print("BambooHR API Client Examples")
    print("=" * 50)
    
    # Basic usage
    if not example_basic_usage():
        print("Cannot proceed without successful connection")
        return
    
    # Other examples
    example_webhooks()
    example_datasets()
    example_timesheet_entries()
    example_error_handling()
    
    print("\n" + "=" * 50)
    print("All examples completed!")


if __name__ == "__main__":
    main() 