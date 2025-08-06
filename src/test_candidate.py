#!/usr/bin/env python3
"""
Test TeamTailor candidate data
"""

import requests

# Test the candidate endpoint
candidate_id = 139634312
url = f"https://api.teamtailor.com/v1/candidates/{candidate_id}"
headers = {
    'Authorization': 'Token token=rddtbCpJh6CBefTGkNTalKDdLOaVyVQ-3m86RcU7',
    'X-Api-Version': '20240404'
}

print(f"Testing TeamTailor candidate {candidate_id}...")
print(f"URL: {url}")

try:
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:1000]}...")
    
    if response.status_code == 200:
        data = response.json()
        candidate = data.get('data', {})
        attributes = candidate.get('attributes', {})
        
        print(f"Candidate: {attributes.get('first-name')} {attributes.get('last-name')}")
        print(f"Email: {attributes.get('email')}")
        
        # Check relationships
        relationships = candidate.get('relationships', {})
        print(f"Relationships: {list(relationships.keys())}")
        
        # Check if there are uploads relationship
        if 'uploads' in relationships:
            uploads_rel = relationships['uploads']
            uploads_data = uploads_rel.get('data', [])
            print(f"Found {len(uploads_data)} uploads for this candidate")
            
            for upload in uploads_data:
                upload_id = upload.get('id')
                print(f"  Upload ID: {upload_id}")
        else:
            print("No uploads relationship found")
            
    else:
        print("Failed to get candidate")
        
except Exception as e:
    print(f"Error: {e}") 