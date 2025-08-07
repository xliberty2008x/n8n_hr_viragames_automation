# Quick Start Guide

Get your HR automation system running in 30 minutes!

## Prerequisites Checklist

- [ ] n8n instance (cloud or self-hosted)
- [ ] TeamTailor account with API access
- [ ] BambooHR account with API key
- [ ] Notion workspace with integration
- [ ] Slack workspace (optional)

## Step 1: Obtain API Credentials

### TeamTailor
1. Log in to TeamTailor Admin
2. Navigate to Settings → Integrations → API
3. Generate new API token
4. Copy and save securely

### BambooHR
1. Log in as administrator
2. Click your profile → API Keys
3. Add new API Key
4. Name it "n8n Integration"
5. Copy the key (shown only once!)

### Notion
1. Visit [Notion Integrations](https://www.notion.so/my-integrations)
2. Create new integration
3. Name it "HR Automation"
4. Copy the Internal Integration Token
5. Share databases with the integration

### Slack (Optional)
1. Go to your Slack workspace
2. Apps → Incoming Webhooks
3. Add to channel (e.g., #hr-notifications)
4. Copy webhook URL

## Step 2: Configure n8n

### Install n8n (if not already done)
```bash
# Using npm
npm install n8n -g

# Using Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Add Credentials in n8n
1. Open n8n (http://localhost:5678)
2. Go to Credentials
3. Add new credential for each service:
   - HTTP Request (TeamTailor)
   - HTTP Request (BambooHR)
   - Notion API
   - Webhook (Slack)

## Step 3: Import Workflows

1. Download workflow templates from `config/n8n-workflows/`
2. In n8n, click "Import from File"
3. Import each workflow:
   - Department Sync
   - Job Requisition
   - Employee Onboarding
4. Update credential references in each workflow

## Step 4: Configure Databases in Notion

### Create Department Database
Properties required:
- Name (Title)
- TeamTailor ID (Text)
- Manager (Person)
- Status (Select: Active/Inactive)

### Create Requisitions Database
Properties required:
- Title (Title)
- Department (Relation)
- Location (Select)
- Employment Type (Select)
- Status (Select)

### Create Employees Database
Properties required:
- Name (Title)
- Email (Email)
- Department (Relation)
- Start Date (Date)
- BambooHR ID (Number)

## Step 5: Test the Integration

### Test Department Sync
1. Create test department in Notion
2. Run Department Sync workflow manually
3. Verify department appears in TeamTailor

### Test Employee Onboarding
1. Create test hire in TeamTailor
2. Trigger webhook
3. Check BambooHR for new employee
4. Verify Notion update
5. Check Slack notification

## Step 6: Schedule Workflows

### Department Sync
- Schedule: Weekly (Sunday 2 AM)
- In n8n: Add Cron node
- Expression: `0 2 * * 0`

### Employee Data Refresh
- Schedule: Daily (6 AM)
- Expression: `0 6 * * *`

## Step 7: Monitor & Maintain

### Set Up Monitoring
1. Enable n8n execution logs
2. Configure error notifications
3. Set up Slack alerts for failures

### Regular Maintenance
- Weekly: Check execution logs
- Monthly: Review API usage
- Quarterly: Update credentials

## Troubleshooting Quick Fixes

### "API Token Invalid"
- Regenerate token in source system
- Update in n8n credentials

### "Rate Limit Exceeded"
- Add delay nodes in workflow
- Reduce batch sizes

### "Database Not Found"
- Share Notion database with integration
- Check database ID in workflow

### "Webhook Not Triggering"
- Verify webhook URL in TeamTailor
- Check n8n webhook node is active

## Success Metrics

After setup, you should see:
- ✅ 85% reduction in manual data entry
- ✅ Real-time synchronization working
- ✅ Error rate below 5%
- ✅ Processing time under 5 minutes

## Next Steps

1. Read [Advanced Configuration](advanced-config.md)
2. Set up [Custom Fields](custom-fields.md)
3. Configure [Error Handling](error-handling.md)
4. Implement [Backup Strategy](backup-strategy.md)

## Need Help?

- 📖 [Full Documentation](https://xliberty2008x.github.io/n8n_hr_viragames_automation/)
- 🎥 [Video Tutorial](https://www.loom.com/share/efa273c5ea30401ea4063c91b92a1d67)
- 🐛 [Troubleshooting Guide](https://xliberty2008x.github.io/n8n_hr_viragames_automation/troubleshooting.html)
- 💬 [GitHub Issues](https://github.com/xliberty2008x/n8n_hr_viragames_automation/issues)