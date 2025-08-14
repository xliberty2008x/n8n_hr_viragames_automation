# 🚀 Quick Setup Guide - Pay Rate Change Notifications

## Prerequisites
- n8n instance with Slack and HTTP Request nodes
- BambooHR API key
- Slack bot with channel access

## Step-by-Step Implementation

### 1️⃣ Import the Workflow
Import `bamboo_change_pay_rate_enhanced.json` into n8n

### 2️⃣ Configure Credentials

#### BambooHR:
- Type: Basic Auth
- Username: `[Your API Key]`
- Password: `x`

#### Slack:
- Type: OAuth2
- Add bot to channel: `hr_legal_finance`

### 3️⃣ Update the Code Node
Copy the content from `pay_rate_change_code.js` into the Code node

### 4️⃣ Test with Sample Data
Use the pinned data in the workflow to test:
- Employee ID: 319
- Old Rate: 3000.00 USD
- New Rate: 3500.00 USD

### 5️⃣ Configure BambooHR Webhook
1. Go to BambooHR → Settings → Webhooks
2. Add webhook URL: `https://[your-n8n-domain]/webhook/390dd887-582c-4ef5-8898-0aa91485a6dc`
3. Select events: "Employee Updated"
4. Add field filter: "Compensation - Pay Rate"

## 📝 Message Examples

### When Pay Rate Changes:
```
🔔 Зміна заробітної плати
Зміна заробітної плати з 3000.00 USD на 3500.00 USD для Іван Петренко
[Переглянути профіль працівника]
```

### When New Pay Rate Set:
```
🔔 Встановлення заробітної плати  
Встановлена заробітна плата 3500.00 USD для Марія Коваленко
[Переглянути профіль працівника]
```

## ⚠️ Important Notes

1. **Test First**: Always test with the Python script before deploying
2. **Check History**: Ensure compensation history exists in BambooHR
3. **Slack Permissions**: Bot must have `chat:write` scope
4. **Error Handling**: Workflow includes error notification node

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| No previous rate found | Check if employee has compensation history |
| Slack message not sent | Verify bot is in channel and has permissions |
| Webhook not triggering | Check webhook configuration in BambooHR |
| Wrong message format | Review Code node for parsing errors |

## 📞 Support
- Test Script: `src/test_pay_rate_change.py`
- Full Documentation: `docs/PAY_RATE_CHANGE_IMPLEMENTATION.md`
- Test Payload: `src/n8n/bamboo_change_pay_rate_test_payload.json`

---
Ready to deploy! 🎉
