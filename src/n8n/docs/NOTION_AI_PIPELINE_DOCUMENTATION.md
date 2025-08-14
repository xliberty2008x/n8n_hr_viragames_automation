# Notion Database to AI Summary Pipeline

## Overview
This n8n workflow fetches tasks from your Notion database ([Manager's Home](https://www.notion.so/viragames/1d99748bc8c28057a458f3e2bc3fcdda?v=1d99748bc8c281dfb9f6000c1aa9f0fb)), retrieves page content blocks, and uses AI (GPT-4) to generate structured summaries of what was achieved for each task.

## Workflow Components

### 1. **Manual Trigger**
- Starts the workflow manually
- Can be replaced with a Schedule Trigger for automation

### 2. **Get Notion Database**
- Fetches all pages from your Notion database
- URL: `https://www.notion.so/viragames/1d99748bc8c28057a458f3e2bc3fcdda?v=1d99748bc8c281dfb9f6000c1aa9f0fb`
- Returns all task pages with properties

### 3. **Split Pages (Process Each)**
- Processes each page individually
- Batch size: 1 (for sequential processing)
- Ensures proper handling of blocks for each page

### 4. **Get Page Blocks**
- Fetches all content blocks for each page
- Retrieves the actual content (body) of the task
- Includes all block types: text, lists, headings, etc.

### 5. **Assemble Page Data**
- Combines page properties with content blocks
- Extracts key properties:
  - Status, Assignee, Responsible, Priority
  - Dates (start, due, end)
  - Team, Type, Estimates
  - Parent/Sub tasks, Key Results
- Processes block content into readable text

### 6. **AI Agent - Analyze Task**
- Uses GPT-4 to analyze the task
- Generates structured JSON output with:
  - Task name and status
  - Achievement summary
  - Key points
  - Completion percentage
  - Next steps

### 7. **Process AI Response**
- Parses AI-generated JSON
- Combines with original task data
- Handles errors gracefully

### 8. **Collect All Summaries**
- Aggregates all processed tasks
- Prepares data for export

### 9. **Export to CSV**
- Converts summaries to CSV format
- Includes all properties and AI analysis

### 10. **Generate Final Report**
- Creates comprehensive report with:
  - Status breakdown
  - Priority distribution
  - Completion overview
  - Task summaries

## AI Output Format

The AI agent generates the following JSON structure for each task:

```json
{
  "task_name": "Task name from Notion",
  "status": "Current status (e.g., Complete, In Progress)",
  "assignee": "alexander.zimenkov@vira.games",
  "responsible": "Person responsible",
  "priority": "High/Normal/Low",
  "team": "Team name or ID",
  "dates": {
    "start": "2025-08-07",
    "due": "2025-08-14",
    "end": "2025-08-07"
  },
  "achievement_summary": "Concise 2-3 sentence summary of achievements",
  "key_points": [
    "Key point 1",
    "Key point 2",
    "Key point 3"
  ],
  "completion_status": 75,
  "next_steps": "What needs to be done next"
}
```

## Example Output

Based on your sample data, here's what the AI would generate:

### Task: "Успішне отримання кредитів AWS Activate"
```json
{
  "task_name": "Успішне отримання кредитів AWS Activate",
  "status": "Complete",
  "assignee": "kirill.dubovyk@vira.games",
  "responsible": "kirill.dubovyk@vira.games",
  "priority": "Normal",
  "achievement_summary": "Successfully obtained AWS Activate credits for the startup. Completed registration on AWS Activate portal and secured cloud infrastructure credits.",
  "key_points": [
    "Registered startup on AWS Activate portal",
    "Obtained AWS credits",
    "Cloud infrastructure funding secured"
  ],
  "completion_status": 100,
  "next_steps": "None - task completed"
}
```

### Task: "Автоматические сообщения в канал #release-aso"
```json
{
  "task_name": "Автоматические сообщения в канал #release-aso",
  "status": "In Review",
  "assignee": "alexander.zimenkov@vira.games",
  "achievement_summary": "Implemented automatic Slack notifications for release reviews. System now sends messages to #release-aso channel when status changes to review.",
  "key_points": [
    "Automated Slack notifications configured",
    "Triggers on status change to review",
    "Workflow link available for monitoring"
  ],
  "completion_status": 90,
  "next_steps": "Final review and approval needed"
}
```

## Setup Instructions

### 1. Prerequisites
- n8n instance with access to:
  - Notion API credentials
  - OpenAI API credentials
- Access to the Notion database

### 2. Configuration
1. Import the workflow JSON into n8n
2. Update credentials:
   - **Notion API**: Use your "Manager's Home" credentials
   - **OpenAI API**: Use your GPT-4 API key
3. Update the database URL if needed

### 3. Running the Workflow
1. Click "Execute Workflow" to run manually
2. Monitor progress in the execution view
3. Check outputs:
   - CSV file with all summaries
   - Final report JSON

## Performance Considerations

- **Processing Time**: ~2-3 seconds per task
- **API Limits**:
  - Notion: 3 requests/second
  - OpenAI: Based on your tier
- **Batch Processing**: Tasks processed one at a time to ensure accuracy

## Customization Options

### Modify AI Prompt
Edit the system message in the AI Agent node to change analysis focus:
- Add specific metrics to track
- Change summary length
- Focus on different aspects

### Add Filters
Add filters to the Notion database query:
```javascript
"filters": {
  "property": "status",
  "select": {
    "equals": "Complete"
  }
}
```

### Change Export Format
- Modify the CSV columns in "Export to CSV" node
- Add JSON export option
- Send results to Slack/Email

## Troubleshooting

### Common Issues

1. **"Invalid database ID"**
   - Verify the Notion database URL
   - Check API permissions

2. **"Rate limited"**
   - Add delays between API calls
   - Reduce batch size

3. **"AI response parsing error"**
   - Check OpenAI API key
   - Verify JSON schema in output parser

4. **"No blocks found"**
   - Ensure pages have content
   - Check block permissions

## Output Files

### 1. CSV Export
- Filename: `notion_task_summaries_YYYY-MM-DD_HHmmss.csv`
- Contains all task summaries with AI analysis
- Columns include all properties and AI-generated fields

### 2. Final Report
- JSON format with statistics
- Status and priority breakdowns
- Overall completion metrics

## Best Practices

1. **Run during off-peak hours** to avoid rate limits
2. **Test with small batches** before processing entire database
3. **Review AI summaries** for accuracy
4. **Archive outputs** for historical tracking
5. **Monitor API usage** to stay within limits

## Integration Ideas

- **Slack Integration**: Send daily summaries to team channel
- **Email Reports**: Weekly progress emails to stakeholders
- **Dashboard**: Connect to visualization tools
- **Jira Sync**: Update external project management tools

## Version History

- **v1.0.0**: Initial release with core functionality
  - Notion database fetching
  - Block content extraction
  - AI summarization
  - CSV export

## Support

For issues or questions:
1. Check n8n execution logs
2. Verify API credentials
3. Review Notion database permissions
4. Test with individual pages first
