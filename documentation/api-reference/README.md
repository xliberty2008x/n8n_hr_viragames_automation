# API Reference Documentation

Complete API documentation for all integrated systems in the HR automation platform.

## 📚 Available Documentation

### TeamTailor API
- [Authentication Guide](teamtailor-auth.md)
- [Endpoints Reference](teamtailor-endpoints.md)
- [Webhook Events](teamtailor-webhooks.md)
- [Custom Fields](teamtailor-custom-fields.md)

### BambooHR API
- [Authentication Setup](bamboohr-auth.md)
- [Employee Management](bamboohr-employees.md)
- [Custom Fields Configuration](bamboohr-custom-fields.md)
- [Reports API](bamboohr-reports.md)

### Notion API
- [Integration Setup](notion-setup.md)
- [Database Operations](notion-databases.md)
- [Property Types](notion-properties.md)
- [Sync Strategies](notion-sync.md)

### Slack Webhooks
- [Webhook Configuration](slack-webhooks.md)
- [Message Formatting](slack-formatting.md)
- [Error Notifications](slack-errors.md)

## 🔑 Authentication Overview

| System | Auth Type | Required Credentials |
|--------|-----------|---------------------|
| TeamTailor | Bearer Token | API Token |
| BambooHR | Basic Auth | API Key + Subdomain |
| Notion | Bearer Token | Integration Token |
| Slack | Webhook URL | Incoming Webhook URL |

## 🔄 Rate Limits

| System | Limit | Window | Notes |
|--------|-------|--------|-------|
| TeamTailor | 300 | 1 minute | Shared across all endpoints |
| BambooHR | 60 | 1 minute | Per API key |
| Notion | 3 | 1 second | Burst allowed |
| Slack | 1 | 1 second | Per webhook |

## 📝 Common Integration Patterns

### 1. Data Synchronization
```javascript
// Example: Sync departments from Notion to TeamTailor
const syncDepartments = async () => {
  const notionDepts = await fetchNotionDepartments();
  const teamTailorDepts = await fetchTeamTailorDepartments();
  
  const toCreate = findNewDepartments(notionDepts, teamTailorDepts);
  const toUpdate = findUpdatedDepartments(notionDepts, teamTailorDepts);
  
  await createDepartments(toCreate);
  await updateDepartments(toUpdate);
};
```

### 2. Webhook Processing
```javascript
// Example: Process TeamTailor hire webhook
const processHireWebhook = async (payload) => {
  const candidate = payload.data;
  
  // Create BambooHR employee
  const employee = await createBambooHREmployee(candidate);
  
  // Update Notion database
  await updateNotionEmployee(employee);
  
  // Send Slack notification
  await sendSlackNotification(employee);
};
```

### 3. Error Handling
```javascript
// Example: Robust API call with retry
const apiCallWithRetry = async (fn, retries = 3) => {
  try {
    return await fn();
  } catch (error) {
    if (retries > 0 && error.status === 429) {
      await sleep(1000);
      return apiCallWithRetry(fn, retries - 1);
    }
    throw error;
  }
};
```

## 🚨 Error Codes Reference

### TeamTailor
- `401` - Invalid API token
- `403` - Insufficient permissions
- `404` - Resource not found
- `429` - Rate limit exceeded

### BambooHR
- `401` - Invalid API key
- `403` - Access denied
- `404` - Employee/resource not found
- `500` - Server error

### Notion
- `400` - Invalid request
- `401` - Invalid integration token
- `404` - Database/page not found
- `429` - Rate limited

## 📊 Testing Endpoints

Each API has test endpoints for development:

- **TeamTailor**: `GET /ping` - Test connection
- **BambooHR**: `GET /meta/users` - List users
- **Notion**: `GET /users/me` - Get bot user
- **Slack**: Send test message to webhook URL

## 🔗 Quick Links

- [TeamTailor API Docs](https://docs.teamtailor.com/)
- [BambooHR API Docs](https://documentation.bamboohr.com/reference)
- [Notion API Docs](https://developers.notion.com/)
- [Slack API Docs](https://api.slack.com/)

## 💡 Best Practices

1. **Always use environment variables** for API credentials
2. **Implement rate limiting** in your n8n workflows
3. **Log all API interactions** for debugging
4. **Use webhook signatures** to verify authenticity
5. **Cache frequently accessed data** to reduce API calls
6. **Implement proper error handling** and retry logic
7. **Monitor API usage** to stay within limits

## 📧 Support

For API-related issues:
- TeamTailor: support@teamtailor.com
- BambooHR: support@bamboohr.com
- Notion: Check their developer community
- Slack: Use their developer support portal