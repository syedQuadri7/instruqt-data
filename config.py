import json
import os
import subprocess

# Suppress the output by redirecting it to DEVNULL
# ACCESS_TOKEN = subprocess.check_output(
#     "jq -r .access_token ~/.config/instruqt/credentials",
#     shell=True,
#     text=True,
#     stderr=subprocess.DEVNULL  # Suppress any error messages
# ).strip() if subprocess.run(
#     "jq -r .access_token ~/.config/instruqt/credentials",
#     shell=True,
#     stdout=subprocess.DEVNULL,  # Suppress standard output
#     stderr=subprocess.DEVNULL  # Suppress error output
# ).returncode == 0 else None

# Retrieve the JSON content from the environment variable (the secret)
instruqt_creds = os.getenv("INSTRUQT_CREDS")

if instruqt_creds:
    # Parse the JSON content of the secret
    creds_data = json.loads(instruqt_creds)
    # Extract the access token
    ACCESS_TOKEN = creds_data.get('access_token')
else:
    ACCESS_TOKEN = None

ENDPOINT = "https://play.instruqt.com/graphql"
HTTP_HEADERS = {"Authorization": "Bearer %s" % ACCESS_TOKEN}
ORG_SLUG = "hashicorp"
FILTER_DEVELOPERS = "true"
YEAR = "2024"
credentials_file = os.path.expanduser('~/.config/instruqt/credentials')
SPREADSHEET = "1MRjoESUT0O6OGao9qO52DmfBPCwHfAc5oMl3YMK-4VE"
