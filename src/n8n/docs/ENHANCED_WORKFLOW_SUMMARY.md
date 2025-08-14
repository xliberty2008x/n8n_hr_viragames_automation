# Enhanced TeamTailor to BambooHR Integration with Job Offers

## Overview
This enhanced n8n workflow integrates TeamTailor job offers data into the BambooHR employee creation process, providing more accurate salary and start date information.

## Key Enhancements

### 1. **Static Test Trigger**
- Replaced webhook with static test payload from `payload_for_test.json`
- Allows testing without live webhook events
- Contains the exact payload structure from your test case

### 2. **Job Offer Integration**
- New node: "Fetch Job Offers" - retrieves all job offers from TeamTailor
- New node: "Process Job Offers" - finds offer matching the application ID
- Extracts critical data:
  - Salary information
  - Start date
  - Offer status (pending/accepted/declined)
  - Offer ID for tracking

### 3. **Enhanced Employee Payload**
The "Build Employee Payload" node now uses offer data:

```javascript
// Priority for hire date:
1. Offer start date (most accurate)
2. Candidate updated_at
3. Webhook updated_at
4. Current date (fallback)

// Salary extraction:
- Parses salary from offer details
- Handles formats like "1500 USD/monthly"
- Extracts numeric value for BambooHR

// Employment status:
- "Active" if offer status is "accepted"
- "Pending" otherwise
```

### 4. **Improved BambooHR Employee Creation**
Employee payload now includes:
- `payRate`: From offer salary (e.g., 1500)
- `hireDate`: From offer start date (e.g., "2025-08-06")
- `mobilePhone`: From candidate phone
- `customOfferId`: For tracking the offer
- `customOfferStatus`: For workflow visibility

### 5. **Enhanced Slack Notification**
Notification now includes:
- Salary information
- Hire date
- Offer ID and status
- Complete employee details

## Workflow Structure

```
1. Static Test Payload
   ↓
2. Check if Hired
   ↓
3. Parallel Fetch:
   - Job Offers → Process Offers
   - Job Requisition → Department
   ↓
4. Build Enhanced Employee Payload
   ↓
5. BambooHR Meta Fields Processing
   ↓
6. Create Employee with Offer Data
   ↓
7. Send Success Notification
```

## Key Data Points

### From Job Offer:
- **Salary**: `offer.details.salary` or `offer.details.Compensation`
- **Start Date**: `offer.details['Start day']`
- **Status**: `offer.status` (accepted/pending/declined)
- **Offer ID**: `offer.id`

### Example Offer Data:
```json
{
  "offerId": "1f7ac031-24a3-42c0-82cd-5569fb228e78",
  "status": "accepted",
  "details": {
    "Compensation": 1500,
    "Start day": "2025-08-06",
    "salary": "1500 USD/monthly"
  }
}
```

### Final BambooHR Payload:
```json
{
  "firstName": "Iryna",
  "lastName": "Munchak",
  "workEmail": "irynamunchak02@gmail.com",
  "hireDate": "2025-08-06",
  "payRate": 1500,
  "payType": "Salary",
  "payPer": "Year",
  "jobTitle": "Marketing Data Analyst",
  "department": "Marketing",
  "mobilePhone": "18724444058",
  "employmentHistoryStatus": "Active",
  "location": "Remote"
}
```

## Testing Instructions

1. Import the workflow into n8n
2. Configure credentials:
   - TeamTailor API token
   - BambooHR API credentials
   - Slack (optional)
3. Run the workflow manually
4. The static payload will trigger the entire flow
5. Check results in BambooHR

## Benefits

1. **Accurate Hire Date**: Uses actual start date from offer
2. **Correct Salary**: Pulls salary directly from accepted offer
3. **Better Tracking**: Links BambooHR employee to TeamTailor offer
4. **Validation**: Only creates employee if offer is accepted
5. **Testing**: Easy to test with static payload

## Notes

- The workflow handles cases where no offer exists (uses fallback values)
- Salary parsing handles various formats (numeric and string)
- All original functionality is preserved and enhanced
- Compatible with existing BambooHR field mappings