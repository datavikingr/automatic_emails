# Usage Guide for Automatic Email Application

## Overview

This guide explains how to use the automatic email application to send personalized marketing emails to local business clients.

## Prerequisites

- Python 3.8+
- Mailjet API credentials
- Required packages: `pip install -r requirements.txt`

## Setting Up a New Client

### Step 1: Create Client Directory
```bash
mkdir clients/YourBusinessName
```

### Step 2: Configure Client Settings
Create `clients/YourBusinessName/config.yaml`:
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

### Step 3: Add Contact Data
Create `clients/YourBusinessName/data.csv`:
```csv
email,first_name,last_name
customer1@business.com,John,Doe
customer2@business.com,Jane,Smith
```

### Step 4: Create Marketing Copy
Create `clients/YourBusinessName/copy/default.txt`:
```
Hi {{first_name}},

This is a personalized message for {{first_name}} {{last_name}} from YourBusiness.

Best regards,
The Team
```

## Running the Application

### Option 1: Run All Active Clients
```bash
python scripts/run_all.py
```

### Option 2: Run Specific Client
```bash
python -m src.main run --client YourBusinessName
```

## Scheduling Emails

### Using Cron (Linux/Mac)
Add to crontab:
```bash
# Run daily at 9 AM
0 9 * * * /path/to/automatic-emails/scripts/run_all.py

# Run weekly on Mondays at 8 AM
0 8 * * 1 /path/to/automatic-emails/scripts/run_all.py
```

### Using Windows Task Scheduler
Create a batch file that runs:
```batch
python C:\path\to\automatic-emails\scripts\run_all.py
```

## Advanced Features

### Template Variables
The following variables are available in your text templates:
- `{{email}}` - Email address
- `{{first_name}}` - First name
- `{{last_name}}` - Last name
- Any additional columns from your CSV/Excel file

### Customizing Subject Lines
Use the `subject_template` in config.yaml:
```yaml
subject_template: "Monthly Update for {{first_name}} {{last_name}}"
```

## Troubleshooting

### Common Issues

1. **Mailjet API Errors**: Check that MAILJET_API_KEY and MAILJET_SECRET are set correctly.
2. **File Not Found Errors**: Ensure all files (CSV, XLSX, TXT) exist in the correct locations.
3. **Permission Denied**: Make sure all files have appropriate read permissions.

### Logging
The application logs to:
- `automatic_emails.log` - Global application log
- `clients/ClientName/logs/ClientName.log` - Per-client logs

## Best Practices

1. Always test with a small dataset first
2. Monitor email deliverability rates
3. Respect email sending limits and rates
4. Keep marketing copy relevant and personalized
5. Regularly update contact data