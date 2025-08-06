import os
import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
import base64


class BambooHRClient:
    """
    Python client for BambooHR API
    """
    
    def __init__(self, config_path: str = "config/config.env"):
        """
        Initialize the BambooHR client with credentials from config file
        
        Args:
            config_path: Path to the configuration file
        """
        self.config = self._load_config(config_path)
        self.base_url = f"https://{self.config['BAMBOOHR_COMPANY_DOMAIN']}.bamboohr.com"
        self.api_key = self.config['BAMBOOHR_API_KEY']
        self.session = requests.Session()
        self.session.auth = (self.api_key, 'x')  # Basic auth with API key as username
        
    def _load_config(self, config_path: str) -> Dict[str, str]:
        """
        Load configuration from .env file
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Dictionary with configuration values
        """
        config = {}
        try:
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except Exception as e:
            raise Exception(f"Error loading configuration: {e}")
            
        # Validate required fields
        required_fields = ['BAMBOOHR_COMPANY_DOMAIN', 'BAMBOOHR_API_KEY']
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ValueError(f"Missing required configuration fields: {missing_fields}")
            
        return config
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the API connection by making a simple request
        
        Returns:
            Dictionary with connection test results
        """
        try:
            # Test with company information endpoint
            response = self.session.get(f"{self.base_url}/api/v1/company_information")
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "message": "Connection successful",
                    "company_info": response.json()
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Connection failed with status {response.status_code}",
                    "response_text": response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Network error occurred"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Unexpected error occurred"
            }
    
    def get_employees(self) -> Dict[str, Any]:
        """
        Get employee directory
        
        Returns:
            Dictionary with employee directory data
        """
        try:
            response = self.session.get(f"{self.base_url}/api/v1/employees/directory")
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "employees": response.json()
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to get employees: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error retrieving employees"
            }
    
    def get_time_tracking_projects(self) -> Dict[str, Any]:
        """
        Get time tracking projects (Note: This endpoint may not be available for GET requests)
        
        Returns:
            Dictionary with time tracking projects data
        """
        try:
            # Try to get projects - this might not be available
            response = self.session.get(f"{self.base_url}/api/v1/time_tracking/projects")
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "projects": response.json()
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to get time tracking projects: {response.text}",
                    "note": "This endpoint may only support POST requests for creating projects"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error retrieving time tracking projects"
            }
    
    def get_timesheet_entries(self, start_date: str, end_date: str, employee_ids: Optional[str] = None) -> Dict[str, Any]:
        """
        Get timesheet entries for a date range
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            employee_ids: Comma-separated list of employee IDs (optional)
            
        Returns:
            Dictionary with timesheet entries data
        """
        params = {
            'start': start_date,
            'end': end_date
        }
        
        if employee_ids:
            params['employeeIds'] = employee_ids
            
        try:
            response = self.session.get(f"{self.base_url}/api/v1/time_tracking/timesheet_entries", params=params)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "timesheet_entries": response.json()
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to get timesheet entries: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error retrieving timesheet entries"
            }
    
    def get_webhooks(self) -> Dict[str, Any]:
        """
        Get list of webhooks
        
        Returns:
            Dictionary with webhooks data
        """
        try:
            response = self.session.get(f"{self.base_url}/api/v1/webhooks")
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "webhooks": response.json()
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to get webhooks: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error retrieving webhooks"
            }
    
    def get_datasets(self) -> Dict[str, Any]:
        """
        Get available datasets
        
        Returns:
            Dictionary with datasets data
        """
        try:
            response = self.session.get(f"{self.base_url}/api/v1/datasets")
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "datasets": response.json()
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to get datasets: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error retrieving datasets"
            }


def main():
    """
    Main function to test the BambooHR client
    """
    print("BambooHR API Client Test")
    print("=" * 40)
    
    try:
        # Initialize client
        client = BambooHRClient()
        print(f"✓ Client initialized successfully")
        print(f"  Base URL: {client.base_url}")
        print(f"  Company Domain: {client.config['BAMBOOHR_COMPANY_DOMAIN']}")
        print()
        
        # Test connection
        print("Testing API connection...")
        connection_result = client.test_connection()
        
        if connection_result["success"]:
            print("✓ Connection successful!")
            if "company_info" in connection_result:
                company_info = connection_result["company_info"]
                print(f"  Company: {company_info.get('displayName', 'N/A')}")
                print(f"  Legal Name: {company_info.get('legalName', 'N/A')}")
        else:
            print("✗ Connection failed!")
            print(f"  Error: {connection_result.get('message', 'Unknown error')}")
            if "status_code" in connection_result:
                print(f"  Status Code: {connection_result['status_code']}")
            return
        
        print()
        
        # Test getting employees
        print("Testing employee retrieval...")
        employees_result = client.get_employees()
        if employees_result["success"]:
            employees = employees_result["employees"]
            print(f"✓ Retrieved employee directory")
            if employees:
                print(f"  Employee directory available")
        else:
            print(f"✗ Failed to get employees: {employees_result.get('message', 'Unknown error')}")
            if "note" in employees_result:
                print(f"  Note: {employees_result['note']}")
        
        print()
        
        # Test getting time tracking projects
        print("Testing time tracking projects retrieval...")
        projects_result = client.get_time_tracking_projects()
        if projects_result["success"]:
            projects = projects_result["projects"]
            print(f"✓ Retrieved {len(projects)} time tracking projects")
        else:
            print(f"✗ Failed to get time tracking projects: {projects_result.get('message', 'Unknown error')}")
            if "note" in projects_result:
                print(f"  Note: {projects_result['note']}")
        
        print()
        
        # Test getting webhooks
        print("Testing webhooks retrieval...")
        webhooks_result = client.get_webhooks()
        if webhooks_result["success"]:
            webhooks = webhooks_result["webhooks"]
            print(f"✓ Retrieved {len(webhooks.get('webhooks', []))} webhooks")
        else:
            print(f"✗ Failed to get webhooks: {webhooks_result.get('message', 'Unknown error')}")
        
        print()
        
        # Test getting datasets
        print("Testing datasets retrieval...")
        datasets_result = client.get_datasets()
        if datasets_result["success"]:
            datasets = datasets_result["datasets"]
            print(f"✓ Retrieved {len(datasets.get('datasets', []))} datasets")
        else:
            print(f"✗ Failed to get datasets: {datasets_result.get('message', 'Unknown error')}")
        
        print()
        print("Test completed!")
        
    except Exception as e:
        print(f"✗ Error initializing client: {e}")


if __name__ == "__main__":
    main() 