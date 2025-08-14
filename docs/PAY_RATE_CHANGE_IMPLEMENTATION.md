# BambooHR Pay Rate Change Notification System

## 📋 Overview

This system automatically detects pay rate changes in BambooHR and sends formatted notifications to a Slack channel in Ukrainian. The implementation includes Python testing scripts and n8n workflow configurations.

## 🎯 Business Requirements

### Original Request
> "Запит - прилітати у канал hr&Legal та писало. Хочу аби у систему прилітало наступне: 'Зміна заробітньої плати з [Актуальне число зміни зп] для [Прізвище Імʼя працівника системи] [Посилання на працівника]'"

### Translation
The system should send notifications to the HR & Legal Slack channel with the format:
- "Salary change from [old amount] to [new amount] for [Employee Name] [Link to employee]"

## 🏗️ Architecture

### Components

1. **BambooHR Webhook** - Triggers on compensation changes
2. **n8n Workflow** - Processes webhook data and orchestrates the flow
3. **BambooHR API** - Fetches compensation history
4. **Slack Integration** - Sends formatted notifications
5. **Python Test Script** - Validates logic before deployment

### Data Flow

```mermaid
graph LR
    A[BambooHR Webhook] --> B[n8n Workflow]
    B --> C[Check Pay Rate Change]
    C --> D[Fetch Compensation History]
    D --> E[Compare Old vs New Rate]
    E --> F[Format Slack Message]
    F --> G[Send to Slack Channel]
```

## 🚀 Implementation

### 1. Python Test Script (`src/test_pay_rate_change.py`)

**Purpose**: Test the pay rate change logic before implementing in n8n

**Key Features**:
- Simulates webhook processing
- Fetches compensation history (mocked for testing)
- Formats Slack messages in Ukrainian
- Generates test output for validation

**Usage**:
```bash
cd src
python test_pay_rate_change.py
```

**Output Example**:
```
🔔 Зміна заробітної плати
Зміна заробітної плати з 3000.00 USD на 3500.00 USD для test-Iryna-test11 test-Munchak
<https://viragames.bamboohr.com/employees/employee.php?id=319|Переглянути профіль працівника>
```

### 2. n8n Workflow Files

#### Enhanced Workflow (`bamboo_change_pay_rate_enhanced.json`)

**Nodes**:
1. **Webhook Node** - Receives BambooHR events
2. **IF Node** - Checks if pay rate changed
3. **HTTP Request Node** - Fetches compensation history
4. **Code Node** - Processes data and formats message
5. **Slack Node** - Sends notification

#### JavaScript Code (`pay_rate_change_code.js`)

**Functions**:
- `parseCompensationHistory()` - Parses BambooHR XML response
- Message formatting logic with three scenarios:
  - Pay rate increased/decreased
  - Pay rate unchanged
  - New pay rate (no history)

### 3. Test Payload (`bamboo_change_pay_rate_test_payload.json`)

Contains sample webhook data for testing the workflow

## 📝 Message Formats

### 1. Pay Rate Change
```
🔔 Зміна заробітної плати
Зміна заробітної плати з 3000.00 USD на 3500.00 USD для John Doe
[Переглянути профіль працівника]
📅 Дата набуття чинності: 2025-08-11
📝 Причина: Annual changes
```

### 2. New Pay Rate (No History)
```
🔔 Встановлення заробітної плати
Встановлена заробітна плата 3500.00 USD для John Doe
[Переглянути профіль працівника]
📅 Дата набуття чинності: 2025-08-11
```

### 3. Compensation Update (No Rate Change)
```
ℹ️ Оновлення компенсації
Компенсація залишилася без змін: 3500.00 USD для John Doe
[Переглянути профіль працівника]
```

## 🔧 Configuration

### Required Environment Variables

Create `config/config.env`:
```env
BAMBOOHR_API_KEY=your-api-key
BAMBOOHR_COMPANY_DOMAIN=viragames
```

### n8n Credentials

1. **BambooHR Basic Auth**
   - Username: API Key
   - Password: x (literal 'x')

2. **Slack API**
   - OAuth token with `chat:write` scope
   - Channel ID: `C06K20PG800` (hr_legal_finance)

## 🔄 Deployment Steps

### Step 1: Test with Python Script
```bash
# Run test script
cd src
python test_pay_rate_change.py

# Review output in formatted_slack_message.json
```

### Step 2: Import n8n Workflow
1. Open n8n interface
2. Import `bamboo_change_pay_rate_enhanced.json`
3. Configure credentials
4. Test with pinned data

### Step 3: Configure BambooHR Webhook
1. Go to BambooHR Settings > Webhooks
2. Add webhook URL from n8n
3. Select "Employee Updated" event
4. Filter for compensation changes

### Step 4: Test End-to-End
1. Make a test pay rate change in BambooHR
2. Verify webhook triggers
3. Check Slack notification

## 🐛 Troubleshooting

### Common Issues

1. **No Previous Pay Rate Found**
   - Check if compensation history exists
   - Verify API permissions
   - Review date comparison logic

2. **XML Parsing Errors**
   - Ensure BambooHR API returns valid XML
   - Check field mappings in code

3. **Slack Message Not Sending**
   - Verify channel ID
   - Check bot permissions
   - Ensure OAuth token is valid

### Debug Mode

The workflow includes debug information in each Slack message:
```
🔍 ID: 319 | Попередня: 3000.00 USD | Час: 11/08/2025, 20:30:45
```

## 📊 API Endpoints Used

### BambooHR API

1. **Get Compensation History**
   ```
   GET /api/v1/employees/{id}/tables/compensation
   ```
   Returns historical compensation records

2. **Employee Profile Link**
   ```
   https://{domain}.bamboohr.com/employees/employee.php?id={id}
   ```

## 🔐 Security Considerations

1. **API Keys** - Store securely in environment variables
2. **Webhook Security** - Validate webhook signatures
3. **Data Privacy** - Ensure only authorized personnel have access to Slack channel
4. **Rate Limiting** - Implement retry logic for API calls

## 📈 Future Enhancements

1. **Multi-language Support** - Add English/Ukrainian toggle
2. **Batch Processing** - Handle multiple employee changes
3. **Audit Trail** - Log all notifications to database
4. **Analytics Dashboard** - Track compensation trends
5. **Approval Workflow** - Add manager approval step

## 📚 References

- [BambooHR API Documentation](https://documentation.bamboohr.com/reference)
- [n8n Documentation](https://docs.n8n.io/)
- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)

## 👥 Support

For issues or questions:
1. Check troubleshooting section
2. Review test script output
3. Examine n8n execution logs
4. Contact HR Tech team

---

**Last Updated**: August 2025
**Version**: 1.0.0
**Author**: HR Integration Team
