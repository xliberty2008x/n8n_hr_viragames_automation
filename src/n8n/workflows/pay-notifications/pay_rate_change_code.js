/**
 * n8n Code Node Script for BambooHR Pay Rate Change Processing
 * 
 * This script processes BambooHR webhook data for pay rate changes,
 * fetches compensation history, and formats Slack notifications in Ukrainian.
 * 
 * Input: 
 * - Webhook data from BambooHR with employee pay rate change
 * - Compensation history API response from BambooHR
 * 
 * Output:
 * - Formatted Slack message with blocks
 * - Employee metadata for logging
 */

// Get webhook data and compensation history
const webhookData = $input.first().json;
const employee = webhookData.body.employees[0];
const compensationResponse = $json;

// Extract employee information
const employeeId = employee.id;
const employeeName = employee.fields['First name Last name'];
const newPayRate = employee.fields['Compensation - Pay Rate'];
const effectiveDate = employee.fields['Compensation - Effective Date'];
const changeReason = employee.fields['Compensation - Change Reason'] || 'Не вказано';
const comment = employee.fields['Compensation - Comment'] || '';
const department = employee.fields['Job Information - Department'] || '';
const jobTitle = employee.fields['Job Information - Job Title'] || '';

// Function to parse XML response from BambooHR
function parseCompensationHistory(response) {
  let previousPayRate = null;
  
  try {
    // If response is already parsed JSON
    if (response && response.table) {
      const rows = response.table.row || [];
      const rowsArray = Array.isArray(rows) ? rows : [rows];
      
      // Convert rows to a more manageable format
      const compensationRecords = rowsArray
        .filter(row => row.field)
        .map(row => {
          const fields = {};
          const fieldArray = Array.isArray(row.field) ? row.field : [row.field];
          
          fieldArray.forEach(field => {
            // Handle different field structures
            if (field['@id'] && field['#text']) {
              fields[field['@id']] = field['#text'];
            } else if (field['@id']) {
              fields[field['@id']] = field['$'] || field;
            }
          });
          
          return {
            date: fields.date || fields.effectiveDate || fields['customEffectiveDate'],
            rate: fields.rate || fields.payRate || fields['customRate'],
            currency: fields.currency || fields['customCurrency'] || 'USD',
            payPer: fields.payPer || fields['customPayPer'] || 'Month'
          };
        })
        .filter(record => record.date && record.rate) // Filter out incomplete records
        .sort((a, b) => new Date(a.date) - new Date(b.date));
      
      // Find the rate just before the effective date
      for (let i = compensationRecords.length - 1; i >= 0; i--) {
        const recordDate = new Date(compensationRecords[i].date);
        const changeDate = new Date(effectiveDate);
        
        if (recordDate < changeDate) {
          const rate = compensationRecords[i].rate;
          const currency = compensationRecords[i].currency;
          previousPayRate = `${rate} ${currency}`;
          break;
        }
      }
      
      // If no previous rate found but records exist, take the most recent one
      if (!previousPayRate && compensationRecords.length > 0) {
        const lastRecord = compensationRecords[compensationRecords.length - 1];
        if (lastRecord.date !== effectiveDate) {
          previousPayRate = `${lastRecord.rate} ${lastRecord.currency}`;
        }
      }
    }
  } catch (error) {
    console.error('Error parsing compensation history:', error);
    // For testing purposes, use a fallback value
    previousPayRate = null;
  }
  
  return previousPayRate;
}

// Parse compensation history
const previousPayRate = parseCompensationHistory(compensationResponse);

// Create employee profile link
const employeeLink = `https://viragames.bamboohr.com/employees/employee.php?id=${employeeId}`;

// Determine the type of change and format message accordingly
let messageText;
let messageType;
let emoji;

if (previousPayRate && previousPayRate !== newPayRate) {
  // Pay rate changed
  emoji = '🔔';
  messageType = 'Зміна заробітної плати';
  messageText = `${emoji} ${messageType}\n` +
    `Зміна заробітної плати з *${previousPayRate}* на *${newPayRate}* ` +
    `для *${employeeName}*\n` +
    `<${employeeLink}|Переглянути профіль працівника>`;
} else if (previousPayRate === newPayRate) {
  // Pay rate unchanged (might be other compensation details changed)
  emoji = 'ℹ️';
  messageType = 'Оновлення компенсації';
  messageText = `${emoji} ${messageType}\n` +
    `Компенсація залишилася без змін: *${newPayRate}* ` +
    `для *${employeeName}*\n` +
    `<${employeeLink}|Переглянути профіль працівника>`;
} else {
  // New pay rate (no previous history found)
  emoji = '🔔';
  messageType = 'Встановлення заробітної плати';
  messageText = `${emoji} ${messageType}\n` +
    `Встановлена заробітна плата *${newPayRate}* ` +
    `для *${employeeName}*\n` +
    `<${employeeLink}|Переглянути профіль працівника>`;
}

// Create main message block
const slackBlocks = [
  {
    type: "section",
    text: {
      type: "mrkdwn",
      text: messageText
    }
  }
];

// Add context information
const contextElements = [
  {
    type: "mrkdwn",
    text: `📅 *Дата набуття чинності:* ${effectiveDate}`
  },
  {
    type: "mrkdwn",
    text: `📝 *Причина:* ${changeReason}`
  }
];

// Add department and job title if available
if (department || jobTitle) {
  let jobInfo = [];
  if (department) jobInfo.push(department);
  if (jobTitle) jobInfo.push(jobTitle);
  
  contextElements.push({
    type: "mrkdwn",
    text: `💼 *Посада:* ${jobInfo.join(' - ')}`
  });
}

slackBlocks.push({
  type: "context",
  elements: contextElements
});

// Add comment if exists
if (comment) {
  slackBlocks.push({
    type: "section",
    text: {
      type: "mrkdwn",
      text: `💬 *Коментар:* ${comment}`
    }
  });
}

// Add divider
slackBlocks.push({
  type: "divider"
});

// Add debug/tracking information
slackBlocks.push({
  type: "context",
  elements: [
    {
      type: "mrkdwn",
      text: `🔍 ID: ${employeeId} | Попередня: ${previousPayRate || 'Не знайдено'} | Час: ${new Date().toLocaleString('uk-UA')}`
    }
  ]
});

// Return formatted data for Slack
return {
  // Main text (fallback for notifications)
  text: messageText.replace(/\*/g, ''), // Remove markdown for plain text
  
  // Rich formatted blocks
  blocks: slackBlocks,
  
  // Metadata for logging/debugging
  metadata: {
    employeeId: employeeId,
    employeeName: employeeName,
    previousRate: previousPayRate,
    newRate: newPayRate,
    effectiveDate: effectiveDate,
    changeReason: changeReason,
    department: department,
    jobTitle: jobTitle,
    messageType: messageType,
    timestamp: new Date().toISOString()
  }
};
