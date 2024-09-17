import os
import subprocess

# Suppress the output by redirecting it to DEVNULL
ACCESS_TOKEN = subprocess.check_output(
    "jq -r .access_token ~/.config/instruqt/credentials",
    shell=True,
    text=True,
    stderr=subprocess.DEVNULL  # Suppress any error messages
).strip() if subprocess.run(
    "jq -r .access_token ~/.config/instruqt/credentials",
    shell=True,
    stdout=subprocess.DEVNULL,  # Suppress standard output
    stderr=subprocess.DEVNULL  # Suppress error output
).returncode == 0 else None

ENDPOINT = "https://play.instruqt.com/graphql"
HTTP_HEADERS = {"Authorization": "Bearer %s" % ACCESS_TOKEN}
ORG_SLUG = "hashicorp"
FILTER_DEVELOPERS = "true"
YEAR = "2024"
credentials_file = os.path.expanduser('~/.config/instruqt/credentials')
SPREADSHEET = "1MRjoESUT0O6OGao9qO52DmfBPCwHfAc5oMl3YMK-4VE"
