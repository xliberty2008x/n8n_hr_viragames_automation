# Quick Setup Guide for BambooHR Pay Rate Notifications

## Step 1: Import Workflows

```bash
# If you have n8n CLI installed
n8n import:workflow bamboohr-pay-rate-change.json
n8n import:workflow bamboohr-polling-workflow.json
```

Or manually import via n8n UI.

## Step 2: Required Environment Variables

Add these to your n8n environment:

```env
# BambooHR Configuration
BAMBOOHR_SUBDOMAIN=viragames
BAMBOOHR_API_KEY=your_api_key_here

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_CHANNEL=hr-legal
```

## Step 3: Webhook URL for BambooHR

Your webhook endpoint will be:
```
https://[your-n8n-domain]/webhook/bamboohr-pay-rate-webhook
```

## Step 4: Testing the Integration

### Test with cURL (webhook):
```bash
curl -X POST https://[your-n8n-domain]/webhook/bamboohr-pay-rate-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "employee": {
      "id": "123",
      "displayName": "Тестовий Працівник"
    },
    "fields": {
      "compensation": "50000 UAH"
    }
  }'
```

### Test BambooHR API connection:
```bash
curl -u YOUR_API_KEY:x \
  https://api.bamboohr.com/api/gateway.php/viragames/v1/employees/directory
```

## Step 5: Slack Message Format

The notification will appear in Slack as:
```
Зміна заробітньої плати з 50000 UAH для Іван Петренко https://viragames.bamboohr.com/employees/employee.php?id=123
```

## Step 6: Activate Workflow

Choose ONE workflow to activate:
- **Webhook workflow**: If BambooHR webhooks are working
- **Polling workflow**: As a fallback or if webhooks aren't available

## Troubleshooting Checklist

- [ ] n8n instance is publicly accessible (for webhooks)
- [ ] BambooHR API key has read permissions for employee data
- [ ] Slack bot is invited to the target channel
- [ ] Webhook URL is correctly configured in BambooHR
- [ ] Only one workflow is active at a time

## Contact Support

- **BambooHR Webhook Issues**: support@bamboohr.com
- **n8n Issues**: https://community.n8n.io
- **Slack Bot Issues**: Check bot permissions at api.slack.com/apps