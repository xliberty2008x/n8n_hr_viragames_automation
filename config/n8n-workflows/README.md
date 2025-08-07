# n8n Workflow Templates

This directory contains the n8n workflow JSON files for the HR automation system.

## Available Workflows

### 1. Department Synchronization (`department-sync.json`)
- Syncs organizational structure between Notion and TeamTailor
- Schedule: Weekly
- Execution time: 1-2 minutes

### 2. Job Requisition Creation (`job-requisition.json`)
- Creates requisitions in TeamTailor from Notion data
- Trigger: Manual/Webhook
- Execution time: 30 seconds

### 3. Employee Onboarding (`employee-onboarding.json`)
- Creates BambooHR profiles for new hires
- Trigger: TeamTailor webhook
- Execution time: 2-3 minutes

## How to Import

1. Open your n8n instance
2. Navigate to Workflows
3. Click "Import from File"
4. Select the desired JSON file
5. Configure credentials as needed
6. Activate the workflow

## Configuration Required

Before importing, ensure you have:
- TeamTailor API credentials
- BambooHR API key
- Notion integration token
- Slack webhook URL (optional)

## Support

For issues or questions, please refer to the [main documentation](https://xliberty2008x.github.io/n8n_hr_viragames_automation/).