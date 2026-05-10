# Calendar Availability Consolidator

A local command-line interface (CLI) utility designed to calculate consolidated availability across multiple Google Calendars within a user-defined window.

## Prerequisites

- Python 3.10+
- A Google Cloud Project with the Calendar API enabled
- OAuth 2.0 Credentials (Client ID, Client Secret, Refresh Token)

## Installation

1. Clone the repository and navigate to the root directory.
2. Create a virtual environment and install dependencies:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure your target calendars in `config.yaml`.

## Environment Setup (Windows)

Set your Google OAuth credentials in your Windows User Environment. Open PowerShell and execute:

```powershell
[System.Environment]::SetEnvironmentVariable('GOOGLE_CLIENT_ID', 'your_id_here', 'User')
[System.Environment]::SetEnvironmentVariable('GOOGLE_CLIENT_SECRET', 'your_secret_here', 'User')
[System.Environment]::SetEnvironmentVariable('GOOGLE_REFRESH_TOKEN', 'your_token_here', 'User')
```

*Note: Restart your terminal after setting these variables.*

## Usage

Run the module from the project root:

```bash
python src/main.py --start "2026-05-07 09:00" --end "2026-05-07 18:00"
```

## Running Tests

To execute the unit test suite, ensure your virtual environment is active and run:

```bash
python -m unittest discover -s src/tests -p "test_*.py"
```
