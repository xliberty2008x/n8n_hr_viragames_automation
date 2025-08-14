# HR Integration System

**Production Ready v1.0** - TeamTailor, BambooHR, Notion & Slack integration via n8n

## Impact Metrics
- **Time savings**: 85% (45-60 min → 5-7 min per process)
- **Error reduction**: 80% fewer manual errors
- **Systems integrated**: 4 platforms unified
- **Real-time sync**: Automated data consistency

## System Architecture
- **TeamTailor** → **n8n** ← **Notion**
- **n8n** → **BambooHR** + **Slack**

## Workflows

### HR Integration (`src/n8n/workflows/hr-integration/`)
1. **tt_bamboohr_webhook_parallel_optimized.json** - Main employee onboarding
2. **opening_new_requisition_current_version.json** - Job requisition creation

### Notion Export (`src/n8n/workflows/notion-export/`)
3. **notion_to_ai_summary_pipeline.json** - AI-powered reporting
4. **notion_database_to_csv_webhook.json** - Data exports

### Pay Notifications (`src/n8n/workflows/pay-notifications/`)
5. **bamboo_change_pay_rate_enhanced.json** - Salary change alerts

## Quick Start

1. **Clone repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure**: Copy `config/config.example.env` to `config/config.env`
4. **Import workflows** from `src/n8n/workflows/`
5. **Test**: `python test_integration_scenarios.py`

## Security
- All sensitive data sanitized with placeholders
- Environment variables for credentials
- See [Setup Guide](src/n8n/workflows/SETUP_GUIDE.md) for configuration

## Documentation
- **Live Site**: https://xliberty2008x.github.io/n8n_hr_viragames_automation/
- **Setup Guide**: [src/n8n/workflows/SETUP_GUIDE.md](src/n8n/workflows/SETUP_GUIDE.md)
- **Workflow Docs**: [src/n8n/docs/](src/n8n/docs/)

## Developed by
**AI Automation Department** - Vira Games  
**Author**: Cyril Dubovik
