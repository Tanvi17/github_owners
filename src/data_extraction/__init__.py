import os
from dotenv import load_dotenv
from github import Auth

load_dotenv()

github_auth = Auth.Token(os.getenv('GITHUB_AUTH_TOKEN'))