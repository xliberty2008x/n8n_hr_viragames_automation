# Workflow Setup Guide
==================================================

This guide explains how to configure the sanitized n8n workflows with your actual credentials and settings.

## 🔧 Required Replacements

### 1. Webhook Configuration
Replace `WEBHOOK_ID_XX_PLACEHOLDER` with your actual webhook IDs:
- Generate new webhook IDs in n8n when importing workflows
- Update any external services pointing to these webhooks

### 2. Notion Configuration
Replace `NOTION_DATABASE_ID_XX_PLACEHOLDER` with your Notion database IDs:
- Get database IDs from your Notion database URLs
- Format: The 32-character hash in your database URL

### 3. Credentials Setup
Replace `CREDENTIAL_ID_XX_PLACEHOLDER` with your n8n credential IDs:
- **TeamTailor API**: Create credential with your TeamTailor API token
- **BambooHR API**: Create credential with your BambooHR API key
- **Notion API**: Create credential with your Notion integration token
- **Slack API**: Create credential with your Slack webhook URL
- **OpenAI API**: Create credential with your OpenAI API key

### 4. Company-Specific URLs
Replace placeholder URLs with your actual endpoints:
- `https://YOUR_COMPANY.bamboohr.com` → `https://yourcompany.bamboohr.com`
- `https://www.notion.so/YOUR_WORKSPACE` → Your actual Notion workspace
- `#your-channel-name` → Your actual Slack channel
- `your.email@yourcompany.com` → Actual email addresses

## 📊 Sanitization Summary

**notion_to_csv_native_nodes.json**: 17 replacements
  - Webhook Id: 10
  - Notion Database Id: 4
  - Credential Id: 3

**opening_new_requisition_current_version.json**: 85 replacements
  - Webhook Id: 58
  - Notion Database Id: 7
  - Credential Id: 18
  - Email Addresses: 2

**tt_bamboohr_webhook_parallel_optimized.json**: 45 replacements
  - Webhook Id: 33
  - Notion Database Id: 2
  - Credential Id: 9
  - Api Keys: 1

**notion_to_ai_summary_pipeline.json**: 19 replacements
  - Webhook Id: 12
  - Notion Database Id: 4
  - Credential Id: 3

**notion_database_to_csv_webhook.json**: 0 replacements

**notion_to_csv_native_webhook.json**: 2 replacements
  - Credential Id: 2

**bamboo_change_pay_rate_enhanced.json**: 15 replacements
  - Webhook Id: 9
  - Notion Database Id: 2
  - Credential Id: 2
  - Api Urls: 2

**Total replacements made**: 183

## 🚀 Import Instructions

1. **Import workflows** into your n8n instance
2. **Update all placeholders** with your actual values
3. **Test each workflow** individually before deploying
4. **Configure webhooks** in your external services
5. **Verify integrations** end-to-end

## ⚠️ Security Notes

- Never commit files with real credentials to version control
- Use environment variables for sensitive configuration
- Regularly rotate API keys and tokens
- Monitor webhook endpoints for unauthorized access
- Keep backup copies of your configured workflows locally