"""
Module for fetching salary information from TeamTailor custom fields
"""

import requests
from typing import Optional, Dict, Any, List


class SalaryFetcher:
    """Helper class to fetch salary information from TeamTailor"""
    
    SALARY_FIELD_ID = "75235"  # The Salary custom field ID found in your system
    SALARY_KEYWORDS = ['salary', 'offer', 'compensation', 'pay', 'wage', 'rate', 'annual', 'hourly']
    
    def __init__(self, teamtailor_base_url: str, teamtailor_session: requests.Session):
        self.teamtailor_base_url = teamtailor_base_url
        self.teamtailor_session = teamtailor_session
    
    def get_candidate_salary(self, candidate_id: int) -> Optional[str]:
        """
        Fetch salary from candidate custom fields
        
        Args:
            candidate_id: TeamTailor candidate ID
            
        Returns:
            Salary value as string or None if not found
        """
        try:
            # Try to get custom field values for the candidate
            url = f"{self.teamtailor_base_url}/custom-field-values"
            params = {
                'filter[owner-id]': candidate_id,
                'filter[owner-type]': 'Candidate',
                'filter[custom-field-id]': self.SALARY_FIELD_ID,
                'include': 'custom-field'
            }
            
            response = self.teamtailor_session.get(url, params=params)
            data = response.json()
            
            # Extract salary value if found
            if data.get('data'):
                for field_value in data['data']:
                    value = field_value.get('attributes', {}).get('value')
                    if value:
                        return str(value).strip()
            
            return None
            
        except Exception as e:
            print(f"Error fetching candidate salary: {e}")
            return None
    
    def get_job_application_salary(self, job_application_id: int) -> Optional[str]:
        """
        Fetch salary from job application custom fields
        
        Args:
            job_application_id: TeamTailor job application ID
            
        Returns:
            Salary value as string or None if not found
        """
        try:
            # Try to get custom field values for the job application
            url = f"{self.teamtailor_base_url}/custom-field-values"
            params = {
                'filter[owner-id]': job_application_id,
                'filter[owner-type]': 'JobApplication',
                'filter[custom-field-id]': self.SALARY_FIELD_ID,
                'include': 'custom-field'
            }
            
            response = self.teamtailor_session.get(url, params=params)
            data = response.json()
            
            # Extract salary value if found
            if data.get('data'):
                for field_value in data['data']:
                    value = field_value.get('attributes', {}).get('value')
                    if value:
                        return str(value).strip()
            
            return None
            
        except Exception as e:
            print(f"Error fetching job application salary: {e}")
            return None
    
    def get_all_custom_field_values(self, owner_id: int, owner_type: str) -> Dict[str, Any]:
        """
        Get all custom field values for a given owner
        
        Args:
            owner_id: ID of the owner (candidate or job application)
            owner_type: Type of owner ('Candidate' or 'JobApplication')
            
        Returns:
            Dictionary mapping field names to values
        """
        try:
            url = f"{self.teamtailor_base_url}/custom-field-values"
            params = {
                'filter[owner-id]': owner_id,
                'filter[owner-type]': owner_type,
                'include': 'custom-field'
            }
            
            response = self.teamtailor_session.get(url, params=params)
            data = response.json()
            
            # Build a dictionary of field name -> value
            field_values = {}
            
            if data.get('data'):
                # First, build a map of field ID to field name from included data
                field_names = {}
                for item in data.get('included', []):
                    if item.get('type') == 'custom-fields':
                        field_names[item['id']] = item.get('attributes', {}).get('name', '')
                
                # Now extract values
                for field_value in data['data']:
                    field_id = field_value.get('relationships', {}).get('custom-field', {}).get('data', {}).get('id')
                    value = field_value.get('attributes', {}).get('value')
                    
                    if field_id in field_names and value:
                        field_name = field_names[field_id]
                        field_values[field_name] = value
            
            return field_values
            
        except Exception as e:
            print(f"Error fetching custom field values: {e}")
            return {}
    
    def find_salary_in_any_field(self, candidate_id: int, job_application_ids: List[int]) -> Optional[str]:
        """
        Search for salary information in any custom field for both candidate and job applications
        
        Args:
            candidate_id: TeamTailor candidate ID
            job_application_ids: List of job application IDs for this candidate
            
        Returns:
            Salary value as string or None if not found
        """
        # First try the specific salary field for candidate
        salary = self.get_candidate_salary(candidate_id)
        if salary:
            print(f"Found salary in candidate custom field: {salary}")
            return salary
        
        # Try job applications
        for app_id in job_application_ids:
            salary = self.get_job_application_salary(app_id)
            if salary:
                print(f"Found salary in job application {app_id} custom field: {salary}")
                return salary
        
        # If not found in specific field, search all fields for salary-related keywords
        print("Salary field empty, searching all custom fields for salary information...")
        
        # Check candidate fields
        candidate_fields = self.get_all_custom_field_values(candidate_id, 'Candidate')
        for field_name, value in candidate_fields.items():
            if any(keyword in field_name.lower() for keyword in self.SALARY_KEYWORDS):
                print(f"Found potential salary in candidate field '{field_name}': {value}")
                return str(value)
        
        # Check job application fields
        for app_id in job_application_ids:
            app_fields = self.get_all_custom_field_values(app_id, 'JobApplication')
            for field_name, value in app_fields.items():
                if any(keyword in field_name.lower() for keyword in self.SALARY_KEYWORDS):
                    print(f"Found potential salary in job application field '{field_name}': {value}")
                    return str(value)
        
        print("No salary information found in any custom fields")
        return None
    
    def parse_salary_value(self, salary_str: Optional[str]) -> Optional[float]:
        """
        Parse salary string to numeric value
        
        Args:
            salary_str: Salary as string (e.g., "50000", "$50,000", "50k")
            
        Returns:
            Salary as float or None if parsing fails
        """
        if not salary_str:
            return None
        
        try:
            # Remove common currency symbols and separators
            cleaned = salary_str.strip()
            cleaned = cleaned.replace('$', '').replace('€', '').replace('£', '')
            cleaned = cleaned.replace(',', '').replace(' ', '')
            
            # Handle 'k' notation (e.g., "50k" -> 50000)
            if cleaned.lower().endswith('k'):
                cleaned = cleaned[:-1]
                return float(cleaned) * 1000
            
            # Try to parse as float
            return float(cleaned)
            
        except (ValueError, AttributeError):
            print(f"Could not parse salary value: {salary_str}")
            return None