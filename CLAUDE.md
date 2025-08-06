# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a TeamTailor to BambooHR integration system that automatically creates employee records in BambooHR when candidates are hired in TeamTailor. The integration is triggered by webhook events and handles employee creation along with document uploads.

## Key Components

- **src/teamtailor_bamboohr_integration.py** - Main integration class that orchestrates the entire workflow
- **src/bamboohr_client.py** - Dedicated BambooHR API client for common operations
- **config/config.env** - Configuration file containing API credentials (not tracked in git)

## Development Commands

### Setup and Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Create config file from example
cp config/config.example.env config/config.env
# Then edit config/config.env with your API credentials
```

### Running Tests
```bash
# Test BambooHR connection
python test_connection.py

# Run integration test scenarios
python test_integration_scenarios.py

# Test with actual payload
python example_usage.py
```

### No Linting/Type Checking Tools
This project currently doesn't have configured linting or type checking tools. Consider adding:
- `ruff` or `flake8` for linting
- `mypy` for type checking
- `black` for code formatting

## Architecture Overview

### Integration Flow
1. **Webhook Receipt**: TeamTailor sends webhook when candidate reaches "Hired" stage
2. **Validation**: Integration validates the webhook payload and event type
3. **Data Retrieval**: 
   - Fetches job requisition details from TeamTailor
   - Downloads candidate documents/attachments
4. **Employee Creation**: 
   - Builds employee payload with department mapping
   - Creates employee record in BambooHR
5. **Document Upload**: Uploads all candidate documents to the employee's BambooHR profile

### Key Methods in TeamTailorBambooHRIntegration

- `process_webhook_payload()` - Main entry point that orchestrates the entire flow
- `validate_webhook_payload()` - Ensures webhook is for "Hired" stage
- `check_employee_exists()` - Prevents duplicate employee creation
- `build_employee_payload()` - Maps TeamTailor data to BambooHR format
- `upload_files_to_bamboohr()` - Handles document uploads with retry logic
- `get_supported_filename()` - Converts unsupported file extensions

### Configuration Requirements
The integration requires API credentials in `config/config.env`:
- `BAMBOOHR_COMPANY_DOMAIN` - Your BambooHR subdomain
- `BAMBOOHR_API_KEY` - BambooHR API key
- `TEAMTAILOR_API_TOKEN` - TeamTailor API token

### Recent Improvements (January 2025)
- Removed TEST_ prefix from employee names for production use
- Fixed file upload JSON parsing errors
- Added support for unsupported file extensions (.twbx, .pptx)
- Improved error reporting with partial success indicators
- Added duplicate employee detection and handling