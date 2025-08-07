#!/bin/bash

# BambooHR Webhook Troubleshooting Script
# This script helps diagnose webhook connectivity issues

echo "========================================"
echo "BambooHR Webhook Troubleshooting Script"
echo "========================================"
echo ""

# Configuration
read -p "Enter your n8n webhook URL: " WEBHOOK_URL
read -p "Enter your BambooHR API key: " -s BAMBOOHR_API_KEY
echo ""
read -p "Enter your BambooHR subdomain (e.g., viragames): " BAMBOOHR_SUBDOMAIN

echo ""
echo "1. Testing n8n webhook endpoint..."
echo "-----------------------------------"

# Test webhook endpoint
WEBHOOK_TEST=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"test": true}')

if [ "$WEBHOOK_TEST" -eq 200 ] || [ "$WEBHOOK_TEST" -eq 201 ] || [ "$WEBHOOK_TEST" -eq 204 ]; then
    echo "✅ Webhook endpoint is accessible (HTTP $WEBHOOK_TEST)"
else
    echo "❌ Webhook endpoint returned HTTP $WEBHOOK_TEST"
    echo "   Please check:"
    echo "   - n8n is running and accessible"
    echo "   - Webhook workflow is active"
    echo "   - URL is correct"
fi

echo ""
echo "2. Testing BambooHR API connection..."
echo "--------------------------------------"

# Test BambooHR API
API_TEST=$(curl -s -o /dev/null -w "%{http_code}" \
  -u "$BAMBOOHR_API_KEY:x" \
  "https://api.bamboohr.com/api/gateway.php/$BAMBOOHR_SUBDOMAIN/v1/employees/directory")

if [ "$API_TEST" -eq 200 ]; then
    echo "✅ BambooHR API connection successful"
else
    echo "❌ BambooHR API returned HTTP $API_TEST"
    echo "   Please check:"
    echo "   - API key is valid"
    echo "   - Subdomain is correct"
    echo "   - API permissions are sufficient"
fi

echo ""
echo "3. Sending test webhook payload..."
echo "-----------------------------------"

# Send test payload
TEST_PAYLOAD='{
  "employee": {
    "id": "test-123",
    "firstName": "Test",
    "lastName": "Employee",
    "displayName": "Test Employee"
  },
  "fields": {
    "compensation": "50000 UAH",
    "rate": "50000"
  },
  "event": "employee.updated",
  "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"
}'

echo "Sending test payload to webhook..."
TEST_RESPONSE=$(curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "$TEST_PAYLOAD")

echo "Response: $TEST_RESPONSE"

echo ""
echo "4. Checking recent BambooHR changes..."
echo "---------------------------------------"

# Check for recent employee changes
SINCE_DATE=$(date -u -d '1 hour ago' +"%Y-%m-%dT%H:%M:%SZ")
CHANGES=$(curl -s -u "$BAMBOOHR_API_KEY:x" \
  "https://api.bamboohr.com/api/gateway.php/$BAMBOOHR_SUBDOMAIN/v1/employees/changed?since=$SINCE_DATE&type=updated" \
  | grep -c "\"id\"")

echo "Found $CHANGES employee changes in the last hour"

echo ""
echo "========================================"
echo "Troubleshooting Summary"
echo "========================================"
echo ""
echo "If webhooks aren't working:"
echo "1. Contact BambooHR support to verify webhook feature is enabled"
echo "2. Check webhook configuration in BambooHR settings"
echo "3. Use the polling workflow as a temporary solution"
echo "4. Monitor n8n execution logs for incoming webhook requests"
echo ""
echo "Polling workflow activation:"
echo "- Import bamboohr-polling-workflow.json to n8n"
echo "- Configure credentials"
echo "- Activate the workflow"
echo "- It will check for changes every 30 minutes"