# Email Verification System

This project provides tools for verifying email addresses without sending actual verification emails. It includes two main components:

1. **Single Email Verification** - A web interface for checking individual email addresses
2. **Bulk CSV Email Verification** - A tool for processing lists of email addresses from CSV files

## Features

- **Syntax validation** - Checks if the email follows proper format
- **Domain validation** - Verifies if the domain exists
- **MX record validation** - Checks if the domain has mail exchange servers
- **SMTP server validation** - Tests if the mail server accepts the email address
- **Disposable email detection** - Identifies temporary/disposable email domains
- **Role-based email detection** - Flags generic addresses like info@, support@, etc.
- **Catch-all domain detection** - Identifies domains that accept all emails

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

### Single Email Verification

1. Run the single email verification app:

```
python app.py
```

2. Open your browser and go to: `http://localhost:5000`
3. Enter an email address and click "Verify Email"
4. View the detailed verification results

### Bulk CSV Email Verification

1. Run the CSV verification app:

```
python verify-app.py
```

2. Open your browser and go to: `http://localhost:5000`
3. Upload a CSV file containing an "email" column
4. The system will process each email and show real-time progress
5. Once complete, you can download:
   - All results
   - Valid emails only
   - Risky emails only
   - Risky and invalid emails

## CSV File Format

Your CSV file should include a column named "email" (case-insensitive). Example:

```
name,email,company
John Doe,john@example.com,Acme Inc
Jane Smith,jane@example.com,XYZ Corp
```

## Verification Results

Emails are classified into three categories:

- **Valid** - Passed all verification checks
- **Risky** - Passed some checks but has potential issues
- **Invalid** - Failed critical verification checks

Each result includes a specific reason code explaining the verification outcome.

## Important Notes

- Email verification without sending confirmation emails is inherently heuristic
- Some mail servers may block SMTP verification attempts
- The only 100% reliable method is to send a confirmation email and get a response
- This tool provides a best-effort verification based on available information

## License

This project is for educational and personal use only.

## Credits

Created with ❤️ for efficient email list management.