#!/usr/bin/env python3
"""
Test script to explore TeamTailor custom fields
This script helps identify what custom fields are available in your TeamTailor instance
and how to fetch salary/offer data from them.
"""

import os
import sys
import json
import requests
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from teamtailor_bamboohr_integration import TeamTailorBambooHRIntegration


class TeamTailorCustomFieldExplorer:
    """Utility class to explore TeamTailor custom fields"""
    
    def __init__(self, integration: TeamTailorBambooHRIntegration):
        self.integration = integration
        self.teamtailor_base_url = integration.teamtailor_base_url
        self.teamtailor_session = integration.teamtailor_session
    
    def get_all_custom_fields(self) -> Dict[str, Any]:
        """Fetch all custom fields defined in TeamTailor"""
        print("\n🔍 Fetching all custom fields...")
        url = f"{self.teamtailor_base_url}/custom-fields"
        response = self.teamtailor_session.get(url)
        return response.json()
    
    def get_candidate_custom_field_values(self, candidate_id: int) -> Dict[str, Any]:
        """Get custom field values for a specific candidate"""
        print(f"\n🔍 Fetching custom field values for candidate {candidate_id}...")
        url = f"{self.teamtailor_base_url}/custom-field-values"
        params = {
            'filter[owner-id]': candidate_id,
            'filter[owner-type]': 'Candidate',
            'include': 'custom-field'
        }
        response = self.teamtailor_session.get(url, params=params)
        return response.json()
    
    def get_job_application_custom_field_values(self, job_application_id: int) -> Dict[str, Any]:
        """Get custom field values for a specific job application"""
        print(f"\n🔍 Fetching custom field values for job application {job_application_id}...")
        url = f"{self.teamtailor_base_url}/custom-field-values"
        params = {
            'filter[owner-id]': job_application_id,
            'filter[owner-type]': 'JobApplication',
            'include': 'custom-field'
        }
        response = self.teamtailor_session.get(url, params=params)
        return response.json()
    
    def get_recent_hired_candidates(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recently hired candidates to test with"""
        print(f"\n🔍 Fetching {limit} recently hired candidates...")
        url = f"{self.teamtailor_base_url}/candidates"
        params = {
            'page[size]': limit,
            'sort': '-updated-at',
            'include': 'job-applications'
        }
        response = self.teamtailor_session.get(url, params=params)
        data = response.json()
        
        # Filter for hired candidates
        hired_candidates = []
        for candidate in data.get('data', []):
            # Check if any job applications have hired status
            candidate_data = {
                'id': candidate['id'],
                'name': f"{candidate['attributes'].get('first-name', '')} {candidate['attributes'].get('last-name', '')}",
                'email': candidate['attributes'].get('email', ''),
                'job_application_ids': []
            }
            
            # Get job application IDs
            job_apps = candidate.get('relationships', {}).get('job-applications', {}).get('data', [])
            candidate_data['job_application_ids'] = [app['id'] for app in job_apps]
            
            hired_candidates.append(candidate_data)
        
        return hired_candidates
    
    def analyze_custom_field(self, field: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a custom field and extract relevant information"""
        attributes = field.get('attributes', {})
        return {
            'id': field.get('id'),
            'name': attributes.get('name'),
            'field_type': attributes.get('field-type'),
            'api_key': attributes.get('api-key'),
            'required': attributes.get('required'),
            'owner_type': attributes.get('owner-resource')
        }
    
    def find_salary_related_fields(self, custom_fields: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find custom fields that might contain salary information"""
        salary_keywords = ['salary', 'offer', 'compensation', 'pay', 'wage', 'rate', 'annual', 'hourly']
        salary_fields = []
        
        for field in custom_fields.get('data', []):
            field_info = self.analyze_custom_field(field)
            field_name = (field_info.get('name') or '').lower()
            
            if any(keyword in field_name for keyword in salary_keywords):
                salary_fields.append(field_info)
        
        return salary_fields
    
    def display_field_value(self, field_value: Dict[str, Any], custom_fields: List[Dict[str, Any]]) -> None:
        """Display a custom field value with its metadata"""
        field_id = field_value.get('relationships', {}).get('custom-field', {}).get('data', {}).get('id')
        value = field_value.get('attributes', {}).get('value')
        
        # Find the custom field definition
        field_def = None
        for field in custom_fields:
            if field.get('id') == field_id:
                field_def = self.analyze_custom_field(field)
                break
        
        if field_def:
            print(f"  📌 {field_def['name']} ({field_def['field_type']}): {value}")
        else:
            print(f"  📌 Field ID {field_id}: {value}")
    
    def run_exploration(self):
        """Run the complete exploration process"""
        print("=" * 80)
        print("TeamTailor Custom Fields Explorer")
        print("=" * 80)
        
        try:
            # Step 1: Get all custom fields
            custom_fields_response = self.get_all_custom_fields()
            all_fields = custom_fields_response.get('data', [])
            
            print(f"\n✅ Found {len(all_fields)} custom fields in total")
            
            # Display all custom fields
            print("\n📋 All Custom Fields:")
            for field in all_fields:
                field_info = self.analyze_custom_field(field)
                print(f"\n  Field: {field_info['name']}")
                print(f"    - Type: {field_info['field_type']}")
                print(f"    - API Key: {field_info['api_key']}")
                print(f"    - Owner Type: {field_info['owner_type']}")
                print(f"    - Required: {field_info['required']}")
            
            # Step 2: Find salary-related fields
            salary_fields = self.find_salary_related_fields(custom_fields_response)
            
            if salary_fields:
                print(f"\n💰 Found {len(salary_fields)} potential salary-related fields:")
                for field in salary_fields:
                    print(f"  - {field['name']} (Type: {field['field_type']}, Owner: {field['owner_type']})")
            else:
                print("\n⚠️  No salary-related custom fields found (based on field names)")
            
            # Step 3: Get recent candidates to check their custom fields
            recent_candidates = self.get_recent_hired_candidates(3)
            
            if recent_candidates:
                print(f"\n👥 Checking custom fields for {len(recent_candidates)} recent candidates:")
                
                for candidate in recent_candidates:
                    print(f"\n  Candidate: {candidate['name']} ({candidate['email']})")
                    print(f"  ID: {candidate['id']}")
                    
                    # Get candidate custom fields
                    candidate_fields = self.get_candidate_custom_field_values(candidate['id'])
                    field_values = candidate_fields.get('data', [])
                    
                    if field_values:
                        print(f"  Found {len(field_values)} custom field values:")
                        for field_value in field_values:
                            self.display_field_value(field_value, all_fields)
                    else:
                        print("  No custom field values found for this candidate")
                    
                    # Check job application custom fields
                    if candidate['job_application_ids']:
                        for app_id in candidate['job_application_ids'][:1]:  # Check first application
                            app_fields = self.get_job_application_custom_field_values(app_id)
                            app_field_values = app_fields.get('data', [])
                            
                            if app_field_values:
                                print(f"\n  Job Application {app_id} custom fields:")
                                for field_value in app_field_values:
                                    self.display_field_value(field_value, all_fields)
            
            # Step 4: Provide implementation suggestions
            print("\n" + "=" * 80)
            print("💡 Implementation Suggestions:")
            print("=" * 80)
            
            if salary_fields:
                print("\n✅ Salary fields found! Here's how to implement:")
                for field in salary_fields:
                    print(f"\n  For field '{field['name']}' (ID: {field['id']}):")
                    print(f"  - Owner type: {field['owner_type']}")
                    print(f"  - Use filter[owner-type]={field['owner_type']} when fetching")
                    print(f"  - Field type: {field['field_type']}")
            else:
                print("\n⚠️  No salary fields found. Options:")
                print("  1. Create a custom field in TeamTailor for salary/offer data")
                print("  2. Use existing number/text fields to store salary information")
                print("  3. Check if salary data is stored in other systems")
            
            print("\n📝 To fetch salary data in your integration:")
            print("  1. Use the custom-field-values endpoint with appropriate filters")
            print("  2. Include 'custom-field' in the include parameter")
            print("  3. Parse the response to find the salary field by ID or name")
            print("  4. Extract the value and add it to the BambooHR employee payload")
            
        except Exception as e:
            print(f"\n❌ Error during exploration: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main function to run the custom fields exploration"""
    # Load environment variables
    env_path = os.path.join(os.path.dirname(__file__), 'config', 'config.env')
    load_dotenv(env_path)
    
    # Verify required environment variables
    required_vars = ['TEAMTAILOR_API_TOKEN', 'BAMBOOHR_API_KEY', 'BAMBOOHR_COMPANY_DOMAIN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please ensure config/config.env contains all required credentials.")
        sys.exit(1)
    
    # Initialize the integration
    integration = TeamTailorBambooHRIntegration()
    
    # Create and run the explorer
    explorer = TeamTailorCustomFieldExplorer(integration)
    explorer.run_exploration()


if __name__ == "__main__":
    main()