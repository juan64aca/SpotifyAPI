import json
import requests
from datetime import datetime


class Token:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = "https://accounts.spotify.com/api/token"
        self.token = None
        self.expiration = None
        self.file = 'token.json'
        self.load_token()

    def load_token(self):
        print("Loading Token.")
        try:
            with open(self.file, 'r') as file:
                data = json.load(file)

            now = datetime.now().timestamp()
            if data['expiration'] > now:
                self.token = data['token']
                self.expiration = data['expiration']

                return True

            else:
                print("Token expired.")
                self.get_token()

        except FileNotFoundError:
            print("Token file not found.")
            self.get_token()
            self.load_token()

    def save_token(self):

        print("Saving token.")
        now = datetime.now().timestamp()

        if not self.token or not self.expiration:
            raise Exception("Missing token.")
        elif self.expiration < now:
            raise Exception("Token expired.")

        data = {
            'token': self.token,
            'expiration': self.expiration
        }

        with open('token.json', 'w') as file:
            json.dump(data, file)

        return True

    def get_token(self):
        print("Requesting Token.")

        auth_response = requests.post(self.url, {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })

        if auth_response.status_code == 200:
            token_info = auth_response.json()

            self.token = token_info['access_token']
            self.expiration = datetime.now().timestamp() + token_info['expires_in']
            self.save_token()

            return True

        else:
            error = auth_response.json()['error_description']
            raise Exception(f'Failed to get token: {auth_response.status_code}. "{error}"')
