import os
import json
import requests
import base64
import random
import string
from datetime import datetime
from typing import Dict, Any, Optional, List
import tempfile
import mimetypes


class TeamTailorBambooHRIntegration:
    """
    Python implementation of the TeamTailor to BambooHR integration workflow
    """
    
    def __init__(self, config_path: str = "config/config.env"):
        """
        Initialize the integration with credentials from config file
        
        Args:
            config_path: Path to the configuration file
        """
        self.config = self._load_config(config_path)
        self.bamboohr_domain = self.config['BAMBOOHR_COMPANY_DOMAIN']
        self.bamboohr_api_key = self.config['BAMBOOHR_API_KEY']
        self.teamtailor_token = self.config['TEAMTAILOR_API_TOKEN']
        
        # API endpoints
        self.bamboohr_base_url = f"https://{self.bamboohr_domain}.bamboohr.com"
        self.teamtailor_base_url = "https://api.teamtailor.com/v1"
        
        # Session setup
        self.bamboohr_session = requests.Session()
        self.bamboohr_session.auth = (self.bamboohr_api_key, 'x')
        
        self.teamtailor_session = requests.Session()
        self.teamtailor_session.headers.update({
            'Authorization': f'Token token={self.teamtailor_token}',
            'X-Api-Version': '20240404',
            'Content-Type': 'application/json'
        })
    
    def _load_config(self, config_path: str) -> Dict[str, str]:
        """Load configuration from .env file"""
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
        
        # Validate required fields
        required_fields = ['BAMBOOHR_COMPANY_DOMAIN', 'BAMBOOHR_API_KEY', 'TEAMTAILOR_API_TOKEN']
        missing_fields = [field for field in required_fields if field not in config]
        if missing_fields:
            raise ValueError(f"Missing required configuration fields: {missing_fields}")
        
        return config
    
    def validate_webhook_payload(self, payload: Dict[str, Any]) -> bool:
        """
        Validate webhook payload matches expected conditions
        
        Args:
            payload: Webhook payload from TeamTailor
            
        Returns:
            True if payload is valid for processing
        """
        try:
            body = payload.get('body', {})
            event_name = body.get('event_name')
            stage_name = body.get('stage_name')
            
            # Check if event is job_application.update and stage is Hired
            return (event_name == 'job_application.update' and 
                   stage_name == 'Hired')
        except Exception as e:
            print(f"Error validating webhook payload: {e}")
            return False
    
    def get_teamtailor_requisition(self, job_id: int) -> Dict[str, Any]:
        """
        Get job requisition from TeamTailor
        
        Args:
            job_id: TeamTailor job ID
            
        Returns:
            Requisition data
        """
        try:
            url = f"{self.teamtailor_base_url}/jobs/{job_id}/requisition"
            
            response = self.teamtailor_session.get(url)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to get requisition: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error retrieving requisition"
            }
    
    def get_teamtailor_department(self, department_url: str) -> Dict[str, Any]:
        """
        Get department information from TeamTailor
        
        Args:
            department_url: Department API URL
            
        Returns:
            Department data
        """
        try:
            response = self.teamtailor_session.get(department_url)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to get department: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error retrieving department"
            }
    
    def get_teamtailor_uploads(self, job_id: int) -> Dict[str, Any]:
        """
        Get uploads (files) from TeamTailor for a specific job
        
        Args:
            job_id: TeamTailor job ID for filtering
            
        Returns:
            Uploads data
        """
        try:
            # Use proper filtering by job_id if provided
            url = f"{self.teamtailor_base_url}/uploads"
            params = {}
            
            if job_id:
                params['filter[job]'] = job_id
            
            response = self.teamtailor_session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                uploads = data.get('data', [])
                
                # Return all uploads for the job (no candidate filtering)
                return {
                    "success": True,
                    "data": {
                        "data": uploads
                    }
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to get uploads: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error retrieving uploads"
            }
    
    def download_file_from_teamtailor(self, file_url: str, filename: str) -> Dict[str, Any]:
        """
        Download file from TeamTailor
        
        Args:
            file_url: URL of the file to download
            filename: Name to save the file as
            
        Returns:
            Download result with file path
        """
        try:
            response = requests.get(file_url, stream=True)
            
            if response.status_code == 200:
                # Create temp directory for downloads
                temp_dir = tempfile.mkdtemp(prefix="tt_downloads_")
                file_path = os.path.join(temp_dir, filename)
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return {
                    "success": True,
                    "file_path": file_path,
                    "filename": filename,
                    "size": os.path.getsize(file_path)
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to download file: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error downloading file"
            }
    
    def build_employee_payload(self, webhook_data: Dict[str, Any], 
                              requisition_data: Dict[str, Any], 
                              department_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build employee payload for BambooHR
        
        Args:
            webhook_data: Webhook payload from TeamTailor
            requisition_data: Job requisition data
            department_data: Department data
            
        Returns:
            Employee payload for BambooHR
        """
        try:
            # Helper function to format date
            def to_ymd(date_str):
                if not date_str:
                    return datetime.now().strftime('%Y-%m-%d')
                try:
                    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    return dt.strftime('%Y-%m-%d')
                except:
                    return datetime.now().strftime('%Y-%m-%d')
            
            # Extract data from webhook
            candidate = webhook_data.get('candidate', {})
            job_title = webhook_data.get('job_title', '')
            
            # Extract requisition data
            requisition = requisition_data.get('data', {})
            req_attrs = requisition.get('attributes', {})
            cfa = req_attrs.get('custom-form-answers', {})
            
            # Extract department name
            department_name = None
            if department_data.get('success'):
                dept_data = department_data['data'].get('data', {})
                dept_attrs = dept_data.get('attributes', {})
                department_name = dept_attrs.get('name')
            
            # Build employee data
            team_name = cfa.get('team')
            candidate_level = cfa.get('level_of_candidate')
            
            # Job title with level prefix
            final_job_title = job_title
            if candidate_level and job_title:
                final_job_title = f"{candidate_level} {job_title}".strip()
            
            # Hire date
            hire_date = to_ymd(candidate.get('updated_at') or webhook_data.get('updated_at'))
            
            # Generate random email to avoid duplicates
            random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            test_email = f"test.{random_suffix}@example.com"
            
            # Build employee payload
            employee = {
                'firstName': f"TEST_{candidate.get('first_name')}",
                'lastName': candidate.get('last_name'),
                'workEmail': test_email,
                'hireDate': hire_date,
                'jobTitle': final_job_title,
                'employmentHistoryStatus': 'Full-Time',
                'payType': 'Salary',
                'payPer': 'Year',
                'exempt': 'Exempt',
                'location': 'Remote'
            }
            
            # Add optional fields
            if department_name:
                employee['department'] = department_name
            
            if team_name:
                employee['division'] = team_name
            
            if candidate.get('phone'):
                employee['mobilePhone'] = candidate['phone']
            
            return {
                "success": True,
                "employee": employee
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error building employee payload"
            }
    
    def get_bamboohr_meta_fields(self) -> Dict[str, Any]:
        """
        Get BambooHR meta fields for field mapping
        
        Returns:
            Meta fields data
        """
        try:
            url = f"{self.bamboohr_base_url}/api/v1/meta/lists"
            headers = {'Accept': 'application/json'}
            
            response = self.bamboohr_session.get(url, headers=headers)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to get meta fields: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error retrieving meta fields"
            }
    
    def validate_and_create_meta_field_options(self, employee_data: Dict[str, Any], 
                                             meta_fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate meta field options and create missing ones
        
        Args:
            employee_data: Employee data
            meta_fields: BambooHR meta fields
            
        Returns:
            Validation and creation results
        """
        try:
            # Field mapping
            field_mapping = {}
            # Handle both list and dict responses from BambooHR
            if isinstance(meta_fields, list):
                meta_fields_list = meta_fields
            else:
                meta_fields_list = meta_fields.get('lists', [])
            
            for field in meta_fields_list:
                if field.get('manageable') != 'yes':
                    continue
                
                field_id = int(field.get('fieldId', 0))
                alias = (field.get('alias') or '').lower()
                name = (field.get('name') or '').lower()
                
                # Map fields by alias or name
                if alias in ['department', 'division', 'jobtitle']:
                    field_mapping[alias] = field_id
                elif name == 'job title' and 'jobtitle' not in field_mapping:
                    field_mapping['jobtitle'] = field_id
            
            # Validate required fields
            required_fields = ['department', 'division', 'jobtitle']
            missing_options = []
            
            for field_name in required_fields:
                field_id = field_mapping.get(field_name)
                if not field_id:
                    continue
                
                field_value = employee_data.get(field_name)
                if not field_value:
                    continue
                
                # Check if option exists
                field = next((f for f in meta_fields_list if f.get('fieldId') == field_id), None)
                if field:
                    options = field.get('options', [])
                    option_exists = any(
                        (opt.get('value') or '').lower() == field_value.lower() or
                        (opt.get('name') or '').lower() == field_value.lower()
                        for opt in options
                    )
                    
                    if not option_exists:
                        missing_options.append({
                            'field_name': field_name,
                            'field_id': field_id,
                            'value': field_value
                        })
            
            # Create missing options
            created_options = []
            for option in missing_options:
                result = self.create_meta_field_option(option['field_id'], option['value'])
                if result['success']:
                    created_options.append(option)
            
            return {
                "success": True,
                "field_mapping": field_mapping,
                "missing_options": missing_options,
                "created_options": created_options
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error validating meta field options"
            }
    
    def create_meta_field_option(self, field_id: int, value: str) -> Dict[str, Any]:
        """
        Create a new option for a meta field
        
        Args:
            field_id: BambooHR field ID
            value: Option value to create
            
        Returns:
            Creation result
        """
        try:
            url = f"{self.bamboohr_base_url}/api/v1/meta/lists/{field_id}"
            headers = {'Content-Type': 'application/json'}
            
            # Get current options first
            response = self.bamboohr_session.get(url, headers={'Accept': 'application/json'})
            if response.status_code != 200:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to get current options: {response.text}"
                }
            
            current_data = response.json()
            current_options = current_data.get('options', [])
            
            # Add new option
            new_options = current_options + [{"value": value}]
            
            # Update field
            payload = {"options": new_options}
            response = self.bamboohr_session.put(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": f"Created option '{value}' for field {field_id}"
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to create option: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error creating meta field option"
            }
    
    def create_bamboohr_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create employee in BambooHR
        
        Args:
            employee_data: Employee data to create
            
        Returns:
            Creation result
        """
        try:
            url = f"{self.bamboohr_base_url}/api/v1/employees"
            headers = {'Content-Type': 'application/json'}
            
            response = self.bamboohr_session.post(url, headers=headers, json=employee_data)
            
            if response.status_code == 201:
                # Extract employee ID from Location header
                employee_id = None
                location_header = response.headers.get('Location')
                if location_header:
                    import re
                    match = re.search(r'/employees/(\d+)', location_header)
                    if match:
                        employee_id = int(match.group(1))
                
                return {
                    "success": True,
                    "employee_id": employee_id,
                    "message": "Employee created successfully",
                    "bamboo_hr_url": f"https://{self.bamboohr_domain}.bamboohr.com/employees/{employee_id}" if employee_id else None
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to create employee: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error creating employee"
            }
    
    def upload_file_to_bamboohr(self, employee_id: int, file_path: str, 
                                filename: str, category: str = "16") -> Dict[str, Any]:
        """
        Upload file to BambooHR employee
        
        Args:
            employee_id: BambooHR employee ID
            file_path: Path to file to upload
            filename: Name of the file
            category: File category ID in BambooHR (default: "16" for Employee Uploads)
            
        Returns:
            Upload result
        """
        try:
            url = f"{self.bamboohr_base_url}/api/v1/employees/{employee_id}/files"
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(file_path)
            if not content_type:
                content_type = 'application/octet-stream'
            
            # Read file
            with open(file_path, 'rb') as f:
                files = {
                    'file': (filename, f, content_type)
                }
                
                data = {
                    'category': category,
                    'fileName': filename
                }
                
                response = self.bamboohr_session.post(url, files=files, data=data)
            
            if response.status_code == 201:
                return {
                    "success": True,
                    "message": f"File '{filename}' uploaded successfully",
                    "file_id": response.json().get('id') if response.json() else None
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": f"Failed to upload file: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error uploading file: {str(e)}"
            }
    
    def process_webhook_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main method to process webhook payload from TeamTailor
        
        Args:
            payload: Webhook payload from TeamTailor
            
        Returns:
            Processing result
        """
        try:
            print("Starting webhook payload processing...")
            
            # Validate payload
            if not self.validate_webhook_payload(payload):
                return {
                    "success": False,
                    "message": "Invalid webhook payload - not a 'Hired' job application update"
                }
            
            webhook_data = payload.get('body', {})
            candidate = webhook_data.get('candidate', {})
            job_id = webhook_data.get('job_id')
            candidate_id = candidate.get('id')
            
            print(f"Processing candidate {candidate_id} for job {job_id}")
            
            # Step 1: Get TeamTailor requisition
            print("Getting TeamTailor requisition...")
            requisition_result = self.get_teamtailor_requisition(job_id)
            if not requisition_result['success']:
                return {
                    "success": False,
                    "message": f"Failed to get requisition: {requisition_result.get('message')}"
                }
            
            # Step 2: Get department information
            print("Getting department information...")
            requisition_data = requisition_result['data']
            dept_url = None
            
            # Extract department URL from requisition
            if requisition_data.get('data', {}).get('relationships', {}).get('department', {}).get('links', {}).get('related'):
                dept_url = requisition_data['data']['relationships']['department']['links']['related']
            
            department_result = None
            if dept_url:
                department_result = self.get_teamtailor_department(dept_url)
            
            # Step 3: Get uploads (files) for the job
            print("Getting uploads for the job...")
            uploads_result = self.get_teamtailor_uploads(job_id)
            downloaded_files = []
            
            if uploads_result['success']:
                uploads_data = uploads_result['data']
                print(f"Found {len(uploads_data.get('data', []))} uploads")
                for upload in uploads_data.get('data', []):
                    upload_attrs = upload.get('attributes', {})
                    file_url = upload_attrs.get('url')
                    filename = upload_attrs.get('file-name', 'unknown_file')
                    
                    if file_url:
                        print(f"Downloading file: {filename}")
                        download_result = self.download_file_from_teamtailor(file_url, filename)
                        if download_result['success']:
                            downloaded_files.append(download_result)
                            print(f"Successfully downloaded: {filename}")
                        else:
                            print(f"Failed to download: {filename} - {download_result.get('message')}")
            else:
                print(f"Failed to get uploads: {uploads_result.get('message')}")
            
            # Step 4: Build employee payload
            print("Building employee payload...")
            employee_payload_result = self.build_employee_payload(
                webhook_data, 
                requisition_data, 
                department_result or {'success': False}
            )
            
            if not employee_payload_result['success']:
                return {
                    "success": False,
                    "message": f"Failed to build employee payload: {employee_payload_result.get('message')}"
                }
            
            employee_data = employee_payload_result['employee']
            
            # Step 5: Get BambooHR meta fields
            print("Getting BambooHR meta fields...")
            meta_fields_result = self.get_bamboohr_meta_fields()
            if not meta_fields_result['success']:
                return {
                    "success": False,
                    "message": f"Failed to get meta fields: {meta_fields_result.get('message')}"
                }
            
            # Step 6: Validate and create meta field options
            print("Validating meta field options...")
            validation_result = self.validate_and_create_meta_field_options(
                employee_data, 
                meta_fields_result['data']
            )
            
            if not validation_result['success']:
                return {
                    "success": False,
                    "message": f"Failed to validate meta fields: {validation_result.get('message')}"
                }
            
            # Step 7: Create employee in BambooHR
            print("Creating employee in BambooHR...")
            create_result = self.create_bamboohr_employee(employee_data)
            
            if not create_result['success']:
                return {
                    "success": False,
                    "message": f"Failed to create employee: {create_result.get('message')}"
                }
            
            employee_id = create_result.get('employee_id')
            
            # Step 8: Upload files to BambooHR employee
            uploaded_files = []
            if employee_id and downloaded_files:
                print(f"Uploading {len(downloaded_files)} files to BambooHR employee...")
                for file_info in downloaded_files:
                    print(f"Uploading file: {file_info['filename']}")
                    upload_result = self.upload_file_to_bamboohr(
                        employee_id,
                        file_info['file_path'],
                        file_info['filename']
                    )
                    
                    if upload_result['success']:
                        uploaded_files.append({
                            'filename': file_info['filename'],
                            'file_id': upload_result.get('file_id')
                        })
                        print(f"Successfully uploaded: {file_info['filename']}")
                    else:
                        print(f"Failed to upload: {file_info['filename']} - {upload_result.get('message')}")
                    
                    # Clean up downloaded file
                    try:
                        os.remove(file_info['file_path'])
                    except:
                        pass
            else:
                print(f"No files to upload. Employee ID: {employee_id}, Downloaded files: {len(downloaded_files)}")
            
            # Return success result
            return {
                "success": True,
                "message": "Employee created successfully",
                "employee": {
                    "id": employee_id,
                    "name": f"{employee_data.get('firstName', '')} {employee_data.get('lastName', '')}",
                    "email": employee_data.get('workEmail'),
                    "department": employee_data.get('department'),
                    "division": employee_data.get('division'),
                    "job_title": employee_data.get('jobTitle')
                },
                "bamboo_hr_url": create_result.get('bamboo_hr_url'),
                "files_uploaded": uploaded_files,
                "meta_fields_created": validation_result.get('created_options', []),
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Unexpected error during processing"
            }


def main():
    """
    Main function to test the integration
    """
    print("TeamTailor to BambooHR Integration Test")
    print("=" * 50)
    
    try:
        # Initialize integration
        integration = TeamTailorBambooHRIntegration()
        print("✓ Integration initialized successfully")
        print()
        
        # Load test payload
        with open('src/payload_for_test.json', 'r') as f:
            test_payloads = json.load(f)
        
        # Process each payload
        for i, payload in enumerate(test_payloads):
            print(f"Processing payload {i+1}/{len(test_payloads)}...")
            print("-" * 30)
            
            result = integration.process_webhook_payload(payload)
            
            if result['success']:
                print("✓ Processing successful!")
                employee = result['employee']
                print(f"  Employee: {employee['name']}")
                print(f"  Email: {employee['email']}")
                print(f"  Department: {employee['department']}")
                print(f"  Job Title: {employee['job_title']}")
                print(f"  BambooHR URL: {result['bamboo_hr_url']}")
                
                if result['files_uploaded']:
                    print(f"  Files uploaded: {len(result['files_uploaded'])}")
                    for file_info in result['files_uploaded']:
                        print(f"    - {file_info['filename']}")
                
                if result['meta_fields_created']:
                    print(f"  Meta fields created: {len(result['meta_fields_created'])}")
                    for field_info in result['meta_fields_created']:
                        print(f"    - {field_info['field_name']}: {field_info['value']}")
            else:
                print("✗ Processing failed!")
                print(f"  Error: {result.get('message', 'Unknown error')}")
            
            print()
        
        print("Test completed!")
        
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    main() 