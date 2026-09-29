# Automatic Email Application

## Overview

The Automatic Email Application is a Python-based solution designed to help local businesses send personalized email marketing campaigns. It uses Mailjet API for reliable email delivery and supports multiple clients with individual configurations.

## Key Features

1. **Multi-Client Support**: Each business client has their own configuration directory
2. **Flexible Data Import**: Accepts CSV or Excel files with email addresses, first names, and last names
3. **Template-Based Marketing**: Uses text files with Jinja2 templating for marketing copy
4. **Mailjet Integration**: Leverages Mailjet API for robust email delivery
5. **Batch Processing**: Efficiently sends emails in batches to avoid rate limiting
6. **Error Handling**: Includes retry logic and comprehensive logging

## Architecture

### Core Components

1. **Configuration Management** (`config.py`):
   - Reads YAML configuration files per client
   - Handles environment variable substitution
   - Validates configuration settings

2. **Data Parsing** (`parser.py`):
   - Supports CSV and Excel file formats
   - Parses contact data into structured format
   - Handles different column structures

3. **Template Rendering** (`template.py`):
   - Uses Jinja2 for template processing
   - Substitutes placeholders with actual values
   - Supports complex templating logic

4. **Email Sending** (`mailer.py`):
   - Integrates with Mailjet API
   - Implements batch sending
   - Includes retry mechanisms
   - Handles errors gracefully

5. **Main Application Logic** (`main.py`):
   - Command-line interface
   - Client management
   - Campaign execution

6. **Batch Runner** (`scripts/run_all.py`):
   - Processes all active clients
   - Schedules campaign execution
   - Centralized logging

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables for Mailjet API keys:
   ```bash
   export MAILJET_API_KEY="your_api_key_here"
   export MAILJET_SECRET="your_secret_here"
   ```

## Client Setup

Each client requires a dedicated directory under `/clients/` with the following structure:

```
clients/
└── YourBusinessName/
    ├── config.yaml
    ├── data.csv
    └── copy/
        └── default.txt
```

### Configuration File (`config.yaml`)
```yaml
client_name: "YourBusinessName"
active: true
frequency: "weekly"
subject_template: "Hello {{first_name}} from YourBusiness!"
from_email: "sales@yourbusiness.com"
mailjet_api_key: "${MAILJET_API_KEY}"
mailjet_secret: "${MAILJET_SECRET}"
retry_attempts: 5
chunk_size: 200
```

### Data File (`data.csv`)
```csv
email,first_name,last_name
customer1@business.com,John,Doe
customer2@business.com,Jane,Smith
```

### Marketing Template (`copy/default.txt`)
```
Hi {{first_name}},

This is a personalized message for {{first_name}} {{last_name}} from YourBusiness.

Best regards,
The Team
```

## Usage

### Command Line Interface
```bash
# Run all active clients
python scripts/run_all.py

# Run specific client
python -m src.main run --client YourBusinessName
```

### Scheduling
The application is designed to be scheduled using cron or task schedulers:
```bash
# Run daily at 9 AM
0 9 * * * /path/to/automatic-emails/scripts/run_all.py

# Run weekly on Mondays at 8 AM
0 8 * * 1 /path/to/automatic-emails/scripts/run_all.py
```

## Error Handling and Logging

The application includes robust error handling:
- Retry logic for failed email deliveries
- Comprehensive logging to both file and console
- Detailed error messages for debugging
- Per-client logging for monitoring

## Security Considerations

1. **API Key Management**: API keys are stored in environment variables, not in code
2. **File Permissions**: Ensure proper permissions on configuration files
3. **Data Privacy**: All data is processed locally; no external data transmission except to Mailjet

## Extensibility

The application can be extended:
- Add new template variables by extending the data parsing
- Modify email sending logic in mailer.py
- Add new command-line options in main.py
- Create custom batch processing logic

## Best Practices

1. Test with small datasets before full campaigns
2. Monitor email deliverability rates
3. Regularly update contact information
4. Use meaningful subject lines for better engagement
5. Follow email marketing best practices and regulations