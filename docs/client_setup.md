# Client Setup Guide

## Overview

This guide explains how to set up a new client for the automatic email application. Each client requires a dedicated directory with configuration files, contact data, and marketing copy.

## Creating a Client Directory

Create a new directory under `clients/` with your business name:
```bash
mkdir clients/YourBusinessName
```

## Required Files Structure

Each client directory must contain:
1. `config.yaml` - Client configuration settings
2. `data.csv` or `data.xlsx` - Contact list data
3. `copy/default.txt` - Marketing template copy

## Configuration File (`config.yaml`)

The configuration file defines how the application should handle this specific client's emails.

### Example Configuration:
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

### Configuration Parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `client_name` | Name of the client/business | "Acme Corporation" |
| `active` | Enable/disable this client | true/false |
| `frequency` | How often to send emails | "daily", "weekly", "monthly" |
| `subject_template` | Jinja2 template for email subject | "Hello {{first_name}}!" |
| `from_email` | Sender email address | "sales@yourbusiness.com" |
| `mailjet_api_key` | Mailjet API key (use ${VAR} to reference env vars) | "${MAILJET_API_KEY}" |
| `mailjet_secret` | Mailjet API secret (use ${VAR} to reference env vars) | "${MAILJET_SECRET}" |
| `retry_attempts` | Number of retry attempts for failed emails | 5 |
| `chunk_size` | Number of emails to send in each batch | 200 |

## Contact Data Files

### CSV Format (`data.csv`)
```csv
email,first_name,last_name
customer1@business.com,John,Doe
customer2@business.com,Jane,Smith
```

### Excel Format (`data.xlsx`)
The application supports Excel files with the same column structure:
- Column 1: email
- Column 2: first_name  
- Column 3: last_name

Additional columns can be included but will not be used unless referenced in templates.

## Marketing Copy Templates

Create a `copy/` directory and add your marketing text file:
```bash
mkdir clients/YourBusinessName/copy
```

### Example Template (`copy/default.txt`)
```
Hi {{first_name}},

This is a personalized message for {{first_name}} {{last_name}} from YourBusiness.

Best regards,
The Team
```

### Template Variables

The following variables are automatically available:
- `{{email}}` - Email address
- `{{first_name}}` - First name
- `{{last_name}}` - Last name

Additional columns from your data file can also be referenced in templates.

## Complete Example Setup

Here's a complete example for a client named "Acme Corporation":

```bash
# Create directory structure
mkdir clients/AcmeCorp
mkdir clients/AcmeCorp/copy

# Create config.yaml
cat > clients/AcmeCorp/config.yaml << EOF
client_name: "Acme Corporation"
active: true
frequency: "weekly"
subject_template: "Weekly Update for {{first_name}}"
from_email: "marketing@acmecorp.com"
mailjet_api_key: "${MAILJET_API_KEY}"
mailjet_secret: "${MAILJET_SECRET}"
retry_attempts: 5
chunk_size: 200
EOF

# Create data.csv
cat > clients/AcmeCorp/data.csv << EOF
email,first_name,last_name
john@acmecorp.com,John,Doe
jane@acmecorp.com,Jane,Smith
EOF

# Create marketing copy
cat > clients/AcmeCorp/copy/default.txt << EOF
Dear {{first_name}} {{last_name}},

We're excited to share our weekly update with you!

Best regards,
The Acme Corp Team
EOF
```

## Testing Your Setup

After creating your client files, test the setup:
1. Run `python scripts/run_all.py` to process all active clients
2. Check the logs in `clients/AcmeCorp/logs/` for any errors
3. Verify that emails are being sent correctly

## Troubleshooting Common Issues

1. **File not found errors**: Ensure all files exist in correct locations
2. **Mailjet API errors**: Verify MAILJET_API_KEY and MAILJET_SECRET environment variables
3. **Template parsing errors**: Check for invalid Jinja2 syntax in your copy files
4. **Permission errors**: Make sure files have appropriate read permissions

## Best Practices

1. Start with a small test dataset before full campaigns
2. Use descriptive client names that match your business
3. Keep marketing copy relevant and personalized
4. Regularly update contact data to maintain accuracy
5. Monitor email deliverability rates and adjust accordingly