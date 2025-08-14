# Notion Database to CSV Export - n8n Workflows

## Overview
Multiple n8n workflows for exporting Notion databases to CSV files with full pagination support. Available in both JavaScript-based and native node versions.

## Workflows

### JavaScript-Based Versions (Advanced)

#### 1. Manual Trigger Version (`notion_database_to_csv.json`)
- **Purpose**: Manual execution for on-demand exports
- **Trigger**: Manual trigger node
- **Best for**: One-time exports, testing, scheduled exports
- **Approach**: Custom JavaScript for maximum control

#### 2. Webhook Version (`notion_database_to_csv_webhook.json`)
- **Purpose**: API-driven exports via webhook
- **Trigger**: HTTP POST webhook
- **Best for**: Automation, integration with other systems, bulk exports
- **Approach**: Advanced JavaScript with comprehensive error handling

### Native Node Versions (Recommended)

#### 3. Native Nodes Manual Version (`notion_to_csv_native_nodes.json`)
- **Purpose**: Simple manual exports using built-in n8n nodes
- **Trigger**: Manual trigger node
- **Best for**: Easy maintenance, visual workflow editing
- **Approach**: Uses native Notion, Set, and SpreadsheetFile nodes

#### 4. Native Nodes Webhook Version (`notion_to_csv_native_webhook.json`)
- **Purpose**: Webhook-triggered exports with native nodes
- **Trigger**: HTTP POST webhook
- **Best for**: Production use, better performance, easier debugging
- **Approach**: Combines native nodes with minimal JavaScript for property processing

## Features

### Core Functionality
- ✅ Full database pagination (handles databases of any size)
- ✅ All Notion property types supported
- ✅ UTF-8 encoding with Excel compatibility
- ✅ Automatic column detection
- ✅ Error handling and recovery
- ✅ Progress tracking for large exports
- ✅ Rate limiting protection

### Supported Notion Property Types
- Title
- Rich Text
- Number
- Select / Multi-select
- Date (with ranges)
- Checkbox
- URL
- Email
- Phone Number
- Formula (all types)
- Relation
- Rollup
- People
- Files & Media
- Created/Edited Time
- Created/Edited By
- Status
- Unique ID

## Setup Instructions

### Prerequisites
1. n8n instance (self-hosted or cloud)
2. Notion API integration
3. Database access permissions

### Step 1: Notion API Setup
1. Go to https://www.notion.so/my-integrations
2. Create a new integration
3. Copy the API key
4. Share your database with the integration

### Step 2: Import Workflow
1. Open n8n
2. Go to Workflows
3. Click "Import from File"
4. Select the JSON file
5. Save the workflow

### Step 3: Configure Credentials
1. Open the workflow
2. Click on "Fetch Notion Pages" node
3. Add Notion credentials:
   - Name: `Notion API`
   - API Key: Your integration token

### Step 4: Configure Environment (Webhook Version)
Add to n8n environment variables:
```bash
NOTION_API_KEY=your_notion_api_key_here
```

## Usage

### Manual Version

1. **Open the workflow**
2. **Click "Execute Workflow"**
3. **In the Manual Trigger node, set:**
   ```json
   {
     "databaseInput": "https://www.notion.so/YOUR_DATABASE_ID",
     "csvFileName": "export.csv"
   }
   ```
4. **Run the workflow**
5. **Download CSV from execution results**

### Webhook Version

#### Basic Request
```bash
curl -X POST https://your-n8n-url/webhook/notion-to-csv-export \
  -H "Content-Type: application/json" \
  -d '{
    "databaseUrl": "https://www.notion.so/YOUR_DATABASE_ID"
  }'
```

#### Advanced Request with Filters
```bash
curl -X POST https://your-n8n-url/webhook/notion-to-csv-export \
  -H "Content-Type: application/json" \
  -d '{
    "databaseUrl": "https://www.notion.so/YOUR_DATABASE_ID",
    "fileName": "filtered_export.csv",
    "filters": {
      "property": "Status",
      "select": {
        "equals": "Completed"
      }
    },
    "sorts": [
      {
        "property": "Created",
        "direction": "descending"
      }
    ],
    "includeArchived": false
  }'
```

### Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `databaseUrl` or `databaseId` | string | Yes | Notion database URL or ID |
| `fileName` | string | No | Output CSV filename (default: `notion_export_YYYY-MM-DD.csv`) |
| `filters` | object | No | Notion API filter object |
| `sorts` | array | No | Notion API sort array |
| `includeArchived` | boolean | No | Include archived pages (default: false) |
| `pageSize` | number | No | Items per batch (max 100, default: 100) |

### Response Format

#### Success Response
```json
{
  "success": true,
  "requestId": "req_1234567890",
  "database": {
    "id": "database_id",
    "url": "database_url",
    "filters": "Applied/None",
    "sorts": "Applied/None"
  },
  "export": {
    "fileName": "export.csv",
    "fileSize": "125.45 KB",
    "encoding": "utf-8"
  },
  "statistics": {
    "totalRecords": 1500,
    "exportedRows": 1500,
    "totalColumns": 25,
    "batchesProcessed": 15
  },
  "performance": {
    "processingTime": "8.5 seconds",
    "averageRecordsPerBatch": 100
  },
  "download": {
    "available": true,
    "path": "./output/export.csv",
    "validUntil": "2024-01-02T12:00:00Z"
  }
}
```

#### Error Response
```json
{
  "success": false,
  "requestId": "req_1234567890",
  "error": {
    "message": "Error description",
    "type": "ErrorType",
    "code": "ERROR_CODE"
  },
  "troubleshooting": [
    "Check API key",
    "Verify database access",
    "..."
  ]
}
```

## CSV Output Format

### System Columns (Always Present)
- `_Row`: Row number
- `_ID`: Notion page ID
- `_Created`: Creation timestamp
- `_Modified`: Last edit timestamp
- `_Archived`: Archive status
- `_URL`: Direct link to Notion page

### Property Columns
- Automatically detected from database
- Named after Notion property names
- Special characters cleaned for CSV compatibility

## Performance Considerations

### Large Databases (>10,000 records)
- Workflow handles pagination automatically
- Processing time: ~1 second per 100 records
- Memory efficient - processes in batches
- Rate limiting: 350ms delay between requests

### Optimization Tips
1. Use filters to reduce data volume
2. Schedule exports during off-peak hours
3. For very large databases (>50,000 records), consider:
   - Breaking into multiple filtered exports
   - Using date-based incremental exports
   - Implementing parallel processing

## Error Handling

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "Invalid database" | Wrong ID/URL | Verify database ID and sharing |
| "Rate limited" | Too many requests | Workflow auto-retries with delay |
| "Unauthorized" | Missing permissions | Share database with integration |
| "Timeout" | Large database | Increase n8n timeout settings |
| "Memory error" | Huge database | Use filters or batch processing |

## Advanced Features

### Custom Filters
```javascript
// Filter by multiple conditions
{
  "and": [
    {
      "property": "Status",
      "select": { "equals": "Active" }
    },
    {
      "property": "Priority",
      "number": { "greater_than": 5 }
    }
  ]
}
```

### Custom Sorts
```javascript
// Sort by multiple fields
[
  {
    "property": "Priority",
    "direction": "descending"
  },
  {
    "property": "Created",
    "direction": "ascending"
  }
]
```

### Scheduled Exports
1. Add Schedule Trigger node
2. Set cron expression (e.g., `0 9 * * 1` for Monday 9 AM)
3. Connect to Parse Database Input node
4. Configure auto-email or upload to cloud storage

## Integration Examples

### With Google Drive
```javascript
// Add after "Save CSV File" node
{
  "type": "n8n-nodes-base.googleDrive",
  "operation": "upload",
  "folderId": "YOUR_FOLDER_ID"
}
```

### With Email
```javascript
// Add Email node to send CSV
{
  "type": "n8n-nodes-base.emailSend",
  "attachments": "data",
  "subject": "Notion Export - {{ $json.fileName }}"
}
```

### With Slack
```javascript
// Notify on completion
{
  "type": "n8n-nodes-base.slack",
  "operation": "file:upload",
  "channelId": "YOUR_CHANNEL"
}
```

## Troubleshooting

### Debug Mode
1. Open workflow
2. Click Settings (gear icon)
3. Enable "Save Execution Progress"
4. Run workflow
5. Check each node's output

### Common Fixes
- **Empty CSV**: Check database sharing
- **Missing columns**: Verify property visibility
- **Encoding issues**: Ensure UTF-8 BOM is present
- **Timeout errors**: Reduce page size or add filters

## Support

### Resources
- [Notion API Docs](https://developers.notion.com)
- [n8n Documentation](https://docs.n8n.io)
- [n8n Community](https://community.n8n.io)

### Workflow Updates
Check for updates at: `/src/n8n/`

## Choosing the Right Version

| Version | Best For | Pros | Cons |
|---------|----------|------|------|
| **Native Nodes Manual** | Simple exports, learning | Easy to understand, visual editing | Less customization |
| **Native Nodes Webhook** | Production automation | Maintainable, reliable, uses n8n features | Limited property handling |
| **JavaScript Manual** | Complex transformations | Full control, advanced processing | Harder to maintain |
| **JavaScript Webhook** | Enterprise integrations | Maximum flexibility, detailed reporting | Requires JS knowledge |

### Recommendation
**Start with Native Node versions** - they're easier to maintain and debug. Only use JavaScript versions if you need:
- Complex data transformations
- Custom error handling
- Advanced filtering logic
- Special property processing

## Version History

### v4.0.0 (Current)
- Added native node versions
- Improved batch processing
- Better property type handling
- Simplified workflow structure

### v3.0.0
- Native nodes implementation
- Batch processing with Split In Batches node
- Improved CSV generation

### v2.0.0
- Added webhook version
- Enhanced error handling
- Improved pagination
- Added filters and sorts support
- Performance optimizations

### v1.0.0
- Initial release
- Basic export functionality
- Manual trigger only

## License
MIT - Feel free to modify and distribute

---

**Created by**: AI Assistant  
**Last Updated**: 2024  
**Compatibility**: n8n v1.0+ | Notion API 2022-06-28
