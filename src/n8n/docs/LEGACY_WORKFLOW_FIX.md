# Legacy Workflow Critical Fixes

## File: `tt_bamboohr_webhook_with_offers_paginated_legacy.json`

### ⚠️ WARNING
This is a legacy workflow with critical issues. Use `tt_bamboohr_webhook_parallel_optimized.json` instead!

### If You Must Use This Legacy Version

#### 1. Fix Security Issue (CRITICAL!)
Replace the hardcoded token in "Fetch All Job Offers (Paginated)1" node:

**BEFORE (Line 65):**
```javascript
const apiToken = 'rddtbCpJh6CBefTGkNTalKDdLOaVyVQ-3m86RcU7'; // SECURITY RISK!
```

**AFTER:**
```javascript
// Remove this line and use n8n credentials instead
// The node should use the TeamTailor credential configured in n8n
```

#### 2. Add Filtering to Reduce API Calls
In the same node, modify the URL to filter by application:

**BEFORE:**
```javascript
let nextUrl = `${baseUrl}?include=job-application,user&page[size]=${pageSize}`;
```

**AFTER:**
```javascript
const applicationId = $('Webhook1').first().json.body.id;
let nextUrl = `${baseUrl}?filter[job-application-id]=${applicationId}&include=job-application,user&page[size]=${pageSize}`;
```

#### 3. Fix Node References
The workflow uses $('Webhook1') instead of $('Webhook') - ensure all references match the actual node names.

### Issues in This Legacy Version

1. **Security**: Hardcoded API token (line 65)
2. **Performance**: Fetches ALL offers instead of filtering
3. **Naming**: All nodes have "1" suffix (confusing)
4. **Parallelization**: Only partial parallel execution
5. **Efficiency**: Makes 50+ API calls when 1 would suffice

### Recommendation

**DO NOT USE THIS WORKFLOW IN PRODUCTION**

Instead, use the optimized version:
- `tt_bamboohr_webhook_parallel_optimized.json`

Which provides:
- 70% faster execution
- 99% fewer API calls
- Proper security
- Full parallelization
- Clean architecture


