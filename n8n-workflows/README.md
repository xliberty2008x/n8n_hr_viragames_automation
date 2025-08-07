# BambooHR Pay Rate Change Notification Workflows

This directory contains n8n workflows for automatically notifying Slack when pay rate changes occur in BambooHR.

## Overview

Two workflows are provided:
1. **Webhook-based workflow** (`bamboohr-pay-rate-change.json`) - Receives real-time updates via BambooHR webhooks
2. **Polling workflow** (`bamboohr-polling-workflow.json`) - Checks for changes every 30 minutes (fallback solution)

## Setup Instructions

### Prerequisites
- n8n instance running and accessible
- BambooHR API credentials
- Slack workspace with bot configured
- Appropriate permissions in BambooHR to access employee data

### 1. Import Workflows to n8n

1. Open your n8n instance
2. Go to Workflows → Import
3. Import both JSON files from this directory

### 2. Configure Credentials

#### BambooHR API Credentials
1. In n8n, go to Credentials → Create New
2. Select "HTTP Request" → "Basic Auth"
3. Name it "BambooHR API"
4. Enter:
   - Username: Your BambooHR API Key
   - Password: Leave empty or enter 'x'
5. Save

#### Slack API Credentials
1. In n8n, go to Credentials → Create New
2. Select "Slack"
3. Name it "Slack API"
4. Follow the OAuth2 setup process or use Bot Token
5. Ensure the bot has permissions to post to the `hr-legal` channel

### 3. Configure BambooHR Webhook (for webhook workflow)

1. Log into BambooHR as an admin
2. Go to Settings → Webhooks
3. Create a new webhook with:
   - URL: `https://your-n8n-instance.com/webhook/bamboohr-pay-rate-webhook`
   - Events: Select "Employee Updated" with focus on compensation fields
   - Fields to monitor: `compensation`, `payRate`, `rate`

### 4. Customize Slack Channel

Both workflows are configured to send to `hr-legal` channel. To change:
1. Open the workflow in n8n
2. Click on "Send to Slack" node
3. Change the channel parameter
4. Save the workflow

## Workflow Details

### Webhook Workflow
- Triggers: Real-time when BambooHR sends webhook
- Processing: Transforms BambooHR data and sends to Slack
- Message format: "Зміна заробітньої плати з [pay rate] для [employee name] [profile link]"

### Polling Workflow
- Triggers: Every 30 minutes
- Processing:
  1. Fetches changes from BambooHR API
  2. Filters for pay rate changes
  3. Gets detailed employee information
  4. Sends formatted message to Slack
  5. Tracks processed employees to avoid duplicates

## Troubleshooting

### Webhooks Not Working

If BambooHR webhooks aren't sending events:

1. **Verify webhook configuration in BambooHR:**
   - Check that the webhook URL is correct
   - Ensure the webhook is enabled
   - Verify event types are correctly selected

2. **Test webhook connectivity:**
   - Use BambooHR's webhook test feature
   - Check n8n execution logs for incoming requests
   - Verify your n8n instance is publicly accessible

3. **Use polling workflow as fallback:**
   - Activate the polling workflow while waiting for webhook fix
   - Adjust polling interval if needed (default: 30 minutes)

### Common Issues

#### No notifications being sent
- Check Slack bot permissions
- Verify channel name is correct
- Review n8n execution logs for errors

#### Duplicate notifications
- Ensure only one workflow is active at a time
- Check the deduplication logic in polling workflow

#### Missing employee data
- Verify BambooHR API permissions
- Check that required fields are accessible via API

## Testing

### Manual Testing
1. In n8n, open the workflow
2. Click "Execute Workflow" button
3. For webhook workflow: Send a test payload
4. For polling workflow: It will check for recent changes

### Test Payload for Webhook
```json
{
  "employee": {
    "id": "123",
    "firstName": "Test",
    "lastName": "Employee",
    "displayName": "Test Employee"
  },
  "fields": {
    "compensation": "75000 USD",
    "rate": "75000"
  }
}
```

## Monitoring

- Enable workflow execution logging in n8n
- Set up error notifications in n8n settings
- Monitor Slack channel for successful notifications
- Review BambooHR audit logs for pay rate changes

## Support

For issues with:
- **BambooHR webhooks**: Contact BambooHR support
- **n8n workflows**: Check n8n documentation or community forums
- **Slack integration**: Verify bot permissions and channel settings

## Security Notes

- Store API credentials securely in n8n
- Use HTTPS for webhook endpoints
- Limit API permissions to minimum required
- Regularly audit access and rotate API keys