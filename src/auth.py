# src/auth.py
import os
from google.oauth2.credentials import Credentials

def get_credentials() -> Credentials:
    """
    Retrieves OAuth 2.0 credentials from Windows Environment Variables.
    Constructs and returns a google.oauth2.credentials.Credentials object.
    """
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    refresh_token = os.environ.get('GOOGLE_REFRESH_TOKEN')

    missing_vars = []
    if not client_id:
        missing_vars.append('GOOGLE_CLIENT_ID')
    if not client_secret:
        missing_vars.append('GOOGLE_CLIENT_SECRET')
    if not refresh_token:
        missing_vars.append('GOOGLE_REFRESH_TOKEN')

    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}. "
            "Please ensure they are set in your Windows User Environment."
        )

    # Standard Google OAuth2 token endpoint
    token_uri = "https://oauth2.googleapis.com/token"

    return Credentials(
        token=None,  # The access token is dynamically generated via the refresh_token
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri=token_uri
    )
