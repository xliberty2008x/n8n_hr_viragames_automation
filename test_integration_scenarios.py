import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List

# Add src to path to import the integration module
sys.path.append('src')
from teamtailor_bamboohr_integration import TeamTailorBambooHRIntegration

class IntegrationTestSuite:
    """
    Comprehensive test suite for TeamTailor to BambooHR integration
    """
    
    def __init__(self):
        self.integration = None
        self.test_results = []
        
    def setup(self):
        """Initialize the integration"""
        try:
            self.integration = TeamTailorBambooHRIntegration()
            return True
        except Exception as e:
            print(f"Failed to initialize integration: {e}")
            return False
    
    def test_scenario_1_no_documents(self):
        """Test scenario: Employee created but no documents uploaded"""
        print("\n=== Test Scenario 1: No Documents Uploaded ===")
        
        # Create a payload with no uploads
        payload = {
            "body": {
                "event_name": "job_application.update",
                "stage_name": "Hired",
                "candidate": {
                    "id": 999999,
                    "first_name": "Test",
                    "last_name": "NoDocs",
                    "phone": "1234567890",
                    "updated_at": "2025-01-15T10:00:00Z"
                },
                "job_id": 6065241,
                "job_title": "Test Analyst",
                "updated_at": "2025-01-15T10:00:00Z"
            }
        }
        
        # Mock the uploads method to return no files
        original_get_uploads = self.integration.get_teamtailor_uploads
        
        def mock_get_uploads(job_id):
            return {
                "success": True,
                "data": {
                    "data": []  # No uploads
                }
            }
        
        self.integration.get_teamtailor_uploads = mock_get_uploads
        
        try:
            result = self.integration.process_webhook_payload(payload)
            
            test_result = {
                "scenario": "No Documents Uploaded",
                "success": result.get('success', False),
                "employee_created": result.get('success', False),
                "files_uploaded": len(result.get('files_uploaded', [])),
                "error": result.get('message', '') if not result.get('success') else None,
                "expected_behavior": "Should create employee successfully without files"
            }
            
            print(f"✓ Employee created: {test_result['employee_created']}")
            print(f"✓ Files uploaded: {test_result['files_uploaded']}")
            print(f"✓ Overall success: {test_result['success']}")
            
            return test_result
            
        except Exception as e:
            test_result = {
                "scenario": "No Documents Uploaded",
                "success": False,
                "employee_created": False,
                "files_uploaded": 0,
                "error": str(e),
                "expected_behavior": "Should create employee successfully without files"
            }
            print(f"✗ Test failed: {e}")
            return test_result
        finally:
            # Restore original method
            self.integration.get_teamtailor_uploads = original_get_uploads
    
    def test_scenario_2_document_upload_failures(self):
        """Test scenario: Employee created but document uploads fail"""
        print("\n=== Test Scenario 2: Document Upload Failures ===")
        
        # Use the actual payload from the file
        with open('src/payload_for_test.json', 'r') as f:
            payloads = json.load(f)
            payload = payloads[0]
        
        try:
            result = self.integration.process_webhook_payload(payload)
            
            test_result = {
                "scenario": "Document Upload Failures",
                "success": result.get('success', False),
                "employee_created": result.get('success', False),
                "files_uploaded": len(result.get('files_uploaded', [])),
                "total_files_attempted": 10,  # Based on the actual run
                "upload_success_rate": f"{len(result.get('files_uploaded', []))}/10",
                "error": result.get('message', '') if not result.get('success') else None,
                "expected_behavior": "Should create employee even if file uploads fail"
            }
            
            print(f"✓ Employee created: {test_result['employee_created']}")
            print(f"✓ Files uploaded: {test_result['files_uploaded']}/10")
            print(f"✓ Overall success: {test_result['success']}")
            
            return test_result
            
        except Exception as e:
            test_result = {
                "scenario": "Document Upload Failures",
                "success": False,
                "employee_created": False,
                "files_uploaded": 0,
                "total_files_attempted": 10,
                "upload_success_rate": "0/10",
                "error": str(e),
                "expected_behavior": "Should create employee even if file uploads fail"
            }
            print(f"✗ Test failed: {e}")
            return test_result
    
    def test_scenario_3_invalid_payload(self):
        """Test scenario: Invalid webhook payload"""
        print("\n=== Test Scenario 3: Invalid Payload ===")
        
        # Create invalid payload
        payload = {
            "body": {
                "event_name": "candidate.create",  # Wrong event
                "stage_name": "Applied",  # Wrong stage
                "candidate": {
                    "id": 999999,
                    "first_name": "Test",
                    "last_name": "Invalid"
                }
            }
        }
        
        try:
            result = self.integration.process_webhook_payload(payload)
            
            test_result = {
                "scenario": "Invalid Payload",
                "success": result.get('success', False),
                "employee_created": False,
                "files_uploaded": 0,
                "error": result.get('message', ''),
                "expected_behavior": "Should reject invalid payloads gracefully"
            }
            
            print(f"✓ Payload rejected: {not test_result['success']}")
            print(f"✓ Error message: {test_result['error']}")
            
            return test_result
            
        except Exception as e:
            test_result = {
                "scenario": "Invalid Payload",
                "success": False,
                "employee_created": False,
                "files_uploaded": 0,
                "error": str(e),
                "expected_behavior": "Should reject invalid payloads gracefully"
            }
            print(f"✗ Test failed: {e}")
            return test_result
    
    def test_scenario_4_missing_required_fields(self):
        """Test scenario: Missing required fields in payload"""
        print("\n=== Test Scenario 4: Missing Required Fields ===")
        
        # Create payload with missing fields
        payload = {
            "body": {
                "event_name": "job_application.update",
                "stage_name": "Hired",
                "candidate": {
                    "id": 999999,
                    # Missing first_name and last_name
                },
                "job_id": 6065241,
                # Missing job_title
            }
        }
        
        try:
            result = self.integration.process_webhook_payload(payload)
            
            test_result = {
                "scenario": "Missing Required Fields",
                "success": result.get('success', False),
                "employee_created": result.get('success', False),
                "files_uploaded": len(result.get('files_uploaded', [])),
                "error": result.get('message', '') if not result.get('success') else None,
                "expected_behavior": "Should handle missing fields gracefully"
            }
            
            print(f"✓ Employee created: {test_result['employee_created']}")
            print(f"✓ Error handling: {test_result['error']}")
            
            return test_result
            
        except Exception as e:
            test_result = {
                "scenario": "Missing Required Fields",
                "success": False,
                "employee_created": False,
                "files_uploaded": 0,
                "error": str(e),
                "expected_behavior": "Should handle missing fields gracefully"
            }
            print(f"✗ Test failed: {e}")
            return test_result
    
    def test_scenario_5_network_failures(self):
        """Test scenario: Network failures during API calls"""
        print("\n=== Test Scenario 5: Network Failures ===")
        
        # Mock network failures
        original_requests_get = self.integration.teamtailor_session.get
        original_requests_post = self.integration.bamboohr_session.post
        
        def mock_failed_get(*args, **kwargs):
            class MockResponse:
                status_code = 500
                text = "Internal Server Error"
            return MockResponse()
        
        def mock_failed_post(*args, **kwargs):
            class MockResponse:
                status_code = 503
                text = "Service Unavailable"
            return MockResponse()
        
        self.integration.teamtailor_session.get = mock_failed_get
        self.integration.bamboohr_session.post = mock_failed_post
        
        # Use the actual payload
        with open('src/payload_for_test.json', 'r') as f:
            payloads = json.load(f)
            payload = payloads[0]
        
        try:
            result = self.integration.process_webhook_payload(payload)
            
            test_result = {
                "scenario": "Network Failures",
                "success": result.get('success', False),
                "employee_created": result.get('success', False),
                "files_uploaded": len(result.get('files_uploaded', [])),
                "error": result.get('message', '') if not result.get('success') else None,
                "expected_behavior": "Should handle network failures gracefully"
            }
            
            print(f"✓ Error handling: {test_result['error']}")
            print(f"✓ Graceful failure: {not test_result['success']}")
            
            return test_result
            
        except Exception as e:
            test_result = {
                "scenario": "Network Failures",
                "success": False,
                "employee_created": False,
                "files_uploaded": 0,
                "error": str(e),
                "expected_behavior": "Should handle network failures gracefully"
            }
            print(f"✗ Test failed: {e}")
            return test_result
        finally:
            # Restore original methods
            self.integration.teamtailor_session.get = original_requests_get
            self.integration.bamboohr_session.post = original_requests_post
    
    def run_all_tests(self):
        """Run all test scenarios"""
        print("🚀 Starting Integration Test Suite")
        print("=" * 50)
        
        if not self.setup():
            print("❌ Failed to initialize integration")
            return
        
        # Run all test scenarios
        scenarios = [
            self.test_scenario_1_no_documents,
            self.test_scenario_2_document_upload_failures,
            self.test_scenario_3_invalid_payload,
            self.test_scenario_4_missing_required_fields,
            self.test_scenario_5_network_failures
        ]
        
        for scenario in scenarios:
            try:
                result = scenario()
                self.test_results.append(result)
            except Exception as e:
                print(f"❌ Scenario failed with exception: {e}")
                self.test_results.append({
                    "scenario": scenario.__name__,
                    "success": False,
                    "error": str(e)
                })
        
        print("\n" + "=" * 50)
        print("📊 Test Results Summary")
        print("=" * 50)
        
        for result in self.test_results:
            status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
            print(f"{status} - {result.get('scenario', 'Unknown')}")
            if result.get('error'):
                print(f"   Error: {result['error']}")
        
        return self.test_results

def main():
    """Main test runner"""
    test_suite = IntegrationTestSuite()
    results = test_suite.run_all_tests()
    
    # Save results to file
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Test results saved to test_results.json")

if __name__ == "__main__":
    main() 