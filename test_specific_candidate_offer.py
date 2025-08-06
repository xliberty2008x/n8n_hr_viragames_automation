#!/usr/bin/env python3
"""
Test script to check if we can fetch offer/salary data for a specific candidate
who was hired (Iryna Munchak from the test payload)
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


def check_candidate_offer_data(integration: TeamTailorBambooHRIntegration):
    """Check all possible places where offer/salary data might be stored"""
    
    # Test candidate details from payload
    candidate_id = 138804865  # Iryna Munchak
    job_application_id = 162933420
    job_id = 6065241  # Marketing Data Analyst
    
    print("=" * 80)
    print("Checking offer/salary data for Iryna Munchak (hired candidate)")
    print("=" * 80)
    print(f"Candidate ID: {candidate_id}")
    print(f"Job Application ID: {job_application_id}")
    print(f"Job ID: {job_id}")
    print()
    
    # 1. Check custom field values for the candidate
    print("1. Checking candidate custom field values...")
    url = f"{integration.teamtailor_base_url}/custom-field-values"
    params = {
        'filter[owner-id]': candidate_id,
        'filter[owner-type]': 'Candidate',
        'include': 'custom-field'
    }
    response = integration.teamtailor_session.get(url, params=params)
    candidate_fields = response.json()
    
    if candidate_fields.get('data'):
        print(f"   Found {len(candidate_fields['data'])} custom field values:")
        for field_value in candidate_fields['data']:
            value = field_value.get('attributes', {}).get('value')
            field_id = field_value.get('relationships', {}).get('custom-field', {}).get('data', {}).get('id')
            
            # Find field name from included data
            field_name = None
            for item in candidate_fields.get('included', []):
                if item.get('id') == field_id and item.get('type') == 'custom-fields':
                    field_name = item.get('attributes', {}).get('name')
                    break
            
            print(f"   - {field_name or f'Field {field_id}'}: {value}")
    else:
        print("   No custom field values found for this candidate")
    
    # 2. Check custom field values for the job application
    print("\n2. Checking job application custom field values...")
    params = {
        'filter[owner-id]': job_application_id,
        'filter[owner-type]': 'JobApplication',
        'include': 'custom-field'
    }
    response = integration.teamtailor_session.get(url, params=params)
    app_fields = response.json()
    
    if app_fields.get('data'):
        print(f"   Found {len(app_fields['data'])} custom field values:")
        for field_value in app_fields['data']:
            value = field_value.get('attributes', {}).get('value')
            field_id = field_value.get('relationships', {}).get('custom-field', {}).get('data', {}).get('id')
            
            # Find field name from included data
            field_name = None
            for item in app_fields.get('included', []):
                if item.get('id') == field_id and item.get('type') == 'custom-fields':
                    field_name = item.get('attributes', {}).get('name')
                    break
            
            print(f"   - {field_name or f'Field {field_id}'}: {value}")
    else:
        print("   No custom field values found for this job application")
    
    # 3. Check job application details with offers included
    print("\n3. Checking job application with offers relationship...")
    url = f"{integration.teamtailor_base_url}/job-applications/{job_application_id}"
    params = {
        'include': 'offers,custom-field-values,candidate'
    }
    response = integration.teamtailor_session.get(url, params=params)
    app_data = response.json()
    
    if app_data.get('data'):
        app_attrs = app_data['data'].get('attributes', {})
        print(f"   Application status: {app_attrs.get('status', 'N/A')}")
        print(f"   Rejected at: {app_attrs.get('rejected-at', 'N/A')}")
        print(f"   Updated at: {app_attrs.get('updated-at', 'N/A')}")
        
        # Check for offers relationship
        offers_rel = app_data['data'].get('relationships', {}).get('offers', {})
        if offers_rel.get('data'):
            print(f"   ✅ Found offers relationship! {len(offers_rel['data'])} offers")
            # Look for offer details in included data
            for offer in offers_rel['data']:
                offer_id = offer.get('id')
                print(f"   Offer ID: {offer_id}")
                
                # Find offer details in included data
                for item in app_data.get('included', []):
                    if item.get('id') == offer_id and item.get('type') == 'offers':
                        offer_attrs = item.get('attributes', {})
                        print(f"      - Status: {offer_attrs.get('status', 'N/A')}")
                        print(f"      - Created at: {offer_attrs.get('created-at', 'N/A')}")
                        print(f"      - Details: {json.dumps(offer_attrs, indent=8)}")
        else:
            print("   ❌ No offers found in job application")
    
    # 4. Try to get offers directly (if endpoint exists)
    print("\n4. Trying to fetch offers directly...")
    url = f"{integration.teamtailor_base_url}/offers"
    params = {
        'filter[job-application-id]': job_application_id
    }
    try:
        response = integration.teamtailor_session.get(url, params=params)
        if response.status_code == 200:
            offers_data = response.json()
            if offers_data.get('data'):
                print(f"   ✅ Found {len(offers_data['data'])} offers!")
                for offer in offers_data['data']:
                    offer_attrs = offer.get('attributes', {})
                    print(f"   Offer {offer.get('id')}:")
                    print(f"      - Status: {offer_attrs.get('status', 'N/A')}")
                    print(f"      - Created: {offer_attrs.get('created-at', 'N/A')}")
                    print(f"      - All attributes: {json.dumps(offer_attrs, indent=8)}")
            else:
                print("   No offers found")
        else:
            print(f"   ❌ Offers endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing offers endpoint: {e}")
    
    # 5. Check candidate's attachments/documents
    print("\n5. Checking candidate attachments/documents...")
    url = f"{integration.teamtailor_base_url}/candidates/{candidate_id}"
    params = {
        'include': 'attachments,documents'
    }
    response = integration.teamtailor_session.get(url, params=params)
    candidate_data = response.json()
    
    attachments = []
    if candidate_data.get('included'):
        for item in candidate_data['included']:
            if item.get('type') in ['attachments', 'documents']:
                attachments.append(item)
    
    if attachments:
        print(f"   Found {len(attachments)} attachments/documents:")
        for att in attachments:
            att_attrs = att.get('attributes', {})
            print(f"   - {att_attrs.get('name', 'N/A')} ({att_attrs.get('file-size', 'N/A')} bytes)")
            print(f"     Type: {att_attrs.get('content-type', 'N/A')}")
            
            # Check if it might be an offer letter
            name_lower = (att_attrs.get('name', '') or '').lower()
            if any(keyword in name_lower for keyword in ['offer', 'salary', 'compensation', 'contract']):
                print(f"     ⚠️  This might be an offer document!")
    else:
        print("   No attachments found")
    
    # 6. Check job requisition for salary range
    print("\n6. Checking job requisition salary range...")
    result = integration.get_teamtailor_requisition(job_id)
    if result['success']:
        requisition = result.get('data', {})
        attrs = requisition.get('attributes', {})
        
        # Check various salary fields
        salary_fields = ['min-salary', 'max-salary', 'salary', 'salary-currency']
        found_salary = False
        for field in salary_fields:
            if field in attrs and attrs[field]:
                print(f"   - {field}: {attrs[field]}")
                found_salary = True
        
        if not found_salary:
            print("   No salary information in job requisition")
    else:
        print(f"   Failed to get requisition: {result.get('error', 'Unknown error')}")
    
    # 7. Search all custom fields for any with salary in the name
    print("\n7. Checking ALL custom fields for salary-related fields...")
    url = f"{integration.teamtailor_base_url}/custom-fields"
    response = integration.teamtailor_session.get(url)
    all_fields = response.json()
    
    salary_fields = []
    for field in all_fields.get('data', []):
        field_name = field.get('attributes', {}).get('name', '').lower()
        if any(keyword in field_name for keyword in ['salary', 'offer', 'compensation', 'pay']):
            salary_fields.append({
                'id': field.get('id'),
                'name': field.get('attributes', {}).get('name'),
                'type': field.get('attributes', {}).get('field-type')
            })
    
    if salary_fields:
        print(f"   Found {len(salary_fields)} salary-related custom fields:")
        for field in salary_fields:
            print(f"   - {field['name']} (ID: {field['id']}, Type: {field['type']})")
            
            # Check if this candidate has a value for this field
            url = f"{integration.teamtailor_base_url}/custom-field-values"
            params = {
                'filter[custom-field-id]': field['id'],
                'filter[owner-id]': candidate_id,
                'filter[owner-type]': 'Candidate'
            }
            response = integration.teamtailor_session.get(url, params=params)
            values = response.json()
            
            if values.get('data'):
                for val in values['data']:
                    print(f"     ✅ Candidate has value: {val.get('attributes', {}).get('value')}")
            else:
                # Try job application
                params['filter[owner-id]'] = job_application_id
                params['filter[owner-type]'] = 'JobApplication'
                response = integration.teamtailor_session.get(url, params=params)
                values = response.json()
                
                if values.get('data'):
                    for val in values['data']:
                        print(f"     ✅ Job application has value: {val.get('attributes', {}).get('value')}")
                else:
                    print(f"     ❌ No value found for this field")


def main():
    """Main function"""
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
    
    # Run the check
    check_candidate_offer_data(integration)
    
    print("\n" + "=" * 80)
    print("Analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()