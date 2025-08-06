#!/usr/bin/env python3
"""
Test TeamTailor uploads endpoint
"""

import requests

# Test the uploads endpoint
url = "https://api.teamtailor.com/v1/uploads"
headers = {
    'Authorization': 'Token token=rddtbCpJh6CBefTGkNTalKDdLOaVyVQ-3m86RcU7',
    'X-Api-Version': '20240404'
}

print("Testing TeamTailor uploads endpoint...")
print(f"URL: {url}")

try:
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:1000]}...")
    
    if response.status_code == 200:
        data = response.json()
        uploads = data.get('data', [])
        print(f"Found {len(uploads)} uploads")
        
        for upload in uploads[:3]:  # Show first 3 uploads
            upload_id = upload.get('id')
            filename = upload.get('attributes', {}).get('file-name', 'No filename')
            file_url = upload.get('attributes', {}).get('url', 'No URL')
            print(f"  Upload {upload_id}: {filename}")
            print(f"    URL: {file_url}")
            
            # Check candidate relationship
            relationships = upload.get('relationships', {})
            candidate_rel = relationships.get('candidate', {})
            candidate_data = candidate_rel.get('data', {})
            candidate_id = candidate_data.get('id')
            print(f"    Candidate ID: {candidate_id}")
    else:
        print("Failed to get uploads")
        
except Exception as e:
    print(f"Error: {e}") 