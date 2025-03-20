from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import logging

def get_oauth2_token(client_id, client_secret, token_url):
    try:
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(
            token_url=token_url,
            client_id=client_id,
            client_secret=client_secret
        )
        logging.info(f"OAuth2 token retrieved successfully")
        return token['access_token']
    except Exception as e:
        logging.error(f"Failed to retrieve OAuth2 token: {e}")
        return None
