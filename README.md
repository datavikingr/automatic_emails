# Automatic Email Application

An automated email marketing solution for local businesses that sends personalized emails using Mailjet API.

## Features

- **Multi-client support**: Manage multiple local businesses with separate configurations
- **Excel/CSV import**: Easily import contact lists with email addresses, first names, and last names
- **Template-based marketing**: Use text files for marketing copy with Jinja2 templating
- **Mailjet integration**: Reliable email delivery through Mailjet API
- **Flexible scheduling**: Configure send frequency per client
- **Error handling**: Robust retry logic with logging

## Project Structure

```
automatic-emails/
├── clients/                # Client directories with configs and data
│   ├── ClientA/
│   │   ├── config.yaml     # Client settings
│   │   ├── data.csv        # Contact list (email, first_name, last_name)
│   │   └── copy/
│   │       └── default.txt # Marketing template
├── src/                    # Source code
│   ├── main.py             # Main application logic
│   ├── mailer.py           # Mailjet integration
│   ├── parser.py           # Data file parsing
│   ├── template.py         # Template rendering
│   └── config.py           # Configuration handling
├── scripts/                # Utility scripts
│   └── run_all.py          # Batch runner for all clients
└── README.md               # This file
```

## Getting Started

### Prerequisites

- Python 3.8+
- Mailjet API credentials
- Required packages: `pip install -r requirements.txt`

### Setup

1. **Create a client directory**:
   ```bash
   mkdir clients/YourBusinessName
   ```

2. **Configure client settings** (`clients/YourBusinessName/config.yaml`):
   ```yaml
   client_name: "YourBusinessName"
   active: true
   frequency: "weekly"  # daily, weekly, monthly
   subject_template: "Hello {{first_name}} from YourBusiness!"
   from_email: "sales@yourbusiness.com"
   mailjet_api_key: "${MAILJET_API_KEY}"
   mailjet_secret: "${MAILJET_SECRET}"
   retry_attempts: 5
   chunk_size: 200
   ```

3. **Add contact data** (`clients/YourBusinessName/data.csv`):
   ```csv
   email,first_name,last_name
   customer1@business.com,John,Doe
   customer2@business.com,Jane,Smith
   ```

4. **Create marketing copy** (`clients/YourBusinessName/copy/default.txt`):
   ```
   Hi {{first_name}},
   
   This is a personalized message for {{first_name}} {{last_name}} from YourBusiness.
   
   Best regards,
   The Team
   ```

### Usage

#### Run for all active clients:
```bash
python scripts/run_all.py
```

#### Send emails via command line:
```bash
python -m src.main run --client YourBusinessName
```

## Configuration Options

- `client_name`: Name of the client/business
- `active`: Enable/disable this client (true/false)
- `frequency`: How often to send emails (daily, weekly, monthly)
- `subject_template`: Jinja2 template for email subject line
- `from_email`: Sender email address
- `mailjet_api_key`: Mailjet API key (use ${MAILJET_API_KEY} to reference environment variable)
- `mailjet_secret`: Mailjet API secret (use ${MAILJET_SECRET} to reference environment variable)
- `retry_attempts`: Number of retry attempts for failed emails
- `chunk_size`: Number of emails to send in each batch

## Environment Variables

Set your Mailjet credentials as environment variables:
```bash
export MAILJET_API_KEY="your_api_key_here"
export MAILJET_SECRET="your_secret_here"
```

## Deployment

### For Local Businesses

1. Install dependencies: `pip install -r requirements.txt`
2. Set up client configurations
3. Schedule with cron or task scheduler:
   ```bash
   # Run daily at 9 AM
   0 9 * * * /path/to/automatic-emails/scripts/run_all.py
   ```

## Development

### Adding New Clients

Create a new directory in the `clients` folder with:
1. `config.yaml` - client configuration
2. `data.csv` or `data.xlsx` - contact data
3. `copy/default.txt` - marketing template

### Extending Functionality

The application is designed to be extensible:
- Add new template variables in the CSV/Excel files
- Modify copy templates with additional Jinja2 syntax
- Extend configuration options in `config.yaml`

## License

This project is licensed under the MIT License.