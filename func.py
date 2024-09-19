import csv
import json
import os
import subprocess
import time
from datetime import datetime, timedelta
import gspread
import pandas as pd
import requests
from gspread.exceptions import WorksheetNotFound
from gspread.worksheet import CellFormat
from gspread_formatting import CellFormat, TextFormat, format_cell_range
import config
import utilities
import pytz


def get_request(q):
    # Sends a POST request to the API endpoint with the provided query 'q'

    # The endpoint URL and access token are retrieved from the config object
    # Authorization header is set using the Bearer token
    response = requests.post(
        config.ENDPOINT,  # API endpoint from config
        headers={"Authorization": "Bearer " + config.ACCESS_TOKEN},  # Authorization header with Bearer token
        json={"query": q}  # The query is passed in the request body as JSON
    )

    # The response is returned in JSON format
    return response.json()


def get_track_plays_by_month(track_slugs, sheet):
    # Generate a dictionary of start and end dates for each month based on the config.YEAR
    dates = utilities.month_map(config.YEAR)

    # Initialize an empty list to store data for each track slug
    slug_data = []

    # Iterate over each track slug in the input list
    for track_slug in track_slugs:
        # Initialize an empty list for the current track slug's row data
        row = []

        # Iterate over each month (key = start date, value = end date) from the dates dictionary
        for k, v in dates.items():
            # Create a query to fetch statistics for the current track slug for the specified month
            query = f"""
                query {{
                    statistics(trackSlug: "{track_slug}", organizationSlug: "{config.ORG_SLUG}", filterDevelopers: {config.FILTER_DEVELOPERS}, start: "{k}", end: "{v}") {{
                        track {{
                            title
                            started_total
                        }}
                    }}
                }}
            """

            # Send the query using the get_request function and store the response
            track = get_request(query)

            # Extract the track title and the number of started_total plays from the response
            title = track["data"]["statistics"]["track"]["title"]
            started_total = track["data"]["statistics"]["track"]["started_total"]
            started_total = None if started_total == 0 else int(started_total)

            # If the track title is not already in the row, append it (to avoid duplication)
            if title not in row:
                row.append(title)

            # Append the started_total plays for the current month to the row
            row.append(started_total)

        # After processing all months, append the row data for this track slug to the slug_data list
        slug_data.append(row)

    # Create and return a table (or similar structure) using the collected slug_data
    return create_table(slug_data, sheet)


def write_to_sheets(path, sheet):
    if sheet is not None:
        # gc = gspread.service_account(filename='service_account.json')
        gc = gspread.service_account()

        spreadsheet = gc.open('Instruqt Metrics')

        # Try to open the worksheet by title, or create it if it doesn't exist
        try:
            worksheet = spreadsheet.worksheet(sheet)
        except WorksheetNotFound:
            # If the sheet doesn't exist, create a new one
            worksheet = spreadsheet.add_worksheet(title=sheet, rows=100, cols=50)

        # Read the CSV file
        with open(f'{path}', newline='') as csvfile:
            reader = list(csv.reader(csvfile))

        # Clear the contents of the worksheet before updating it
        worksheet.clear()

        # Update the worksheet with the CSV data
        worksheet.update('A1', reader)

        # Apply bold formatting to the first row (headers)
        header_range = f'A1:{chr(64 + len(reader[0]))}1'  # Dynamically calculate the range based on the number of columns
        bold_format = CellFormat(textFormat=TextFormat(bold=True))
        format_cell_range(worksheet, header_range, bold_format)

        # Delete the CSV file after writing to the sheet
        os.remove(path)


def get_track_slugs():
    # Build the GraphQL query to retrieve the slugs of all tracks for the specified organization
    query = f"""query {{
           tracks(organizationSlug: "{config.ORG_SLUG}") {{
             slug
             title
           }}
       }}"""

    # Send the query to the API and store the response
    output = get_request(query)

    # Extract the 'slug' field from each track in the response
    slugs = [track['slug'] for track in output['data']['tracks']]

    # Return the list of slugs
    return slugs


def create_table(data, sheet):
    # Get the current time in EST
    current_time_utc = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    current_time_est = convert_to_eastern_us(current_time_utc)

    # Define the months as the column headers for the table (from February to January)
    months = ['February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
              'December', 'January']

    # Append the current time in EST to the "Track Titles" header
    track_title_header = f"Track Titles (run {current_time_est} EST)"
    headers = [track_title_header] + months

    # Extract the topics (track titles) from the first element of each sublist in data
    topics = [item[0] for item in data]

    # Extract the values (started_total plays per month) from the rest of each sublist in data
    values = [item[1:] for item in data]

    # Combine track titles and monthly values into a list of lists
    combined_data = [[topics[i]] + values[i] for i in range(len(topics))]

    # Create a pandas DataFrame with the values, using headers as the column labels
    df = pd.DataFrame(combined_data, columns=headers)

    # Define the file path where the CSV file will be saved
    file_path = 'outputs/data.csv'

    # Save the DataFrame to a CSV file
    df.to_csv(file_path, index=False)  # Use index=False to avoid adding an extra index column

    return write_to_sheets(file_path, sheet)


def get_tracks_completion_by_month(track_slugs, sheet):
    # Generate a dictionary of start and end dates for each month based on the config.YEAR
    dates = utilities.month_map(config.YEAR)

    # Initialize an empty list to store data for each track slug
    slug_data = []

    # Iterate over each track slug in the input list
    for track_slug in track_slugs:
        # Initialize a list for the current track slug's row data, starting with the track title
        row = None

        # Iterate over each month (key = start date, value = end date) from the dates dictionary
        for k, v in dates.items():
            # Construct the query once, with variables that can be reused
            query = f"""
                query {{
                    statistics(trackSlug: "{track_slug}", organizationSlug: "{config.ORG_SLUG}", filterDevelopers: {config.FILTER_DEVELOPERS}, start: "{k}", end: "{v}") {{
                        track {{
                            title
                            started_total
                            completed_total
                        }}
                    }}
                }}
            """

            # Send the query using the get_request function and store the response
            track = get_request(query)

            # Extract the track details
            track_data = track.get("data", {}).get("statistics", {}).get("track", {})
            title = track_data.get("title")
            started_total = track_data.get("started_total", 0)
            completed_total = track_data.get("completed_total", 0)

            # If this is the first iteration for this track, initialize the row with the title
            if row is None:
                row = [title]

            # Calculate the completion percentage
            percent_completed = round((completed_total / started_total) * 100) if started_total > 0 else None

            # Append the percentage with a "%" sign if it is not None
            percent_completed_str = f"{percent_completed}%" if percent_completed is not None else None

            # Append the completion percentage for the current month to the row
            row.append(percent_completed_str)

        # If row is initialized, append it to the slug_data list
        if row:
            slug_data.append(row)

    # Create and return a table (or similar structure) using the collected slug_data
    return create_table(slug_data, sheet)


def get_tracks_review_score_by_month(track_slugs, sheet):
    # Generate a dictionary of start and end dates for each month based on the config.YEAR
    dates = utilities.month_map(config.YEAR)

    # Initialize an empty list to store data for each track slug
    slug_data = []

    # Iterate over each track slug in the input list
    for track_slug in track_slugs:
        row = None  # Initialize the row variable

        # Iterate over each month (key = start date, value = end date) from the dates dictionary
        for k, v in dates.items():
            # Create a query to fetch statistics for the current track slug for the specified month
            query = f"""
                query {{
                    statistics(trackSlug: "{track_slug}", organizationSlug: "{config.ORG_SLUG}", filterDevelopers: {config.FILTER_DEVELOPERS}, start: "{k}", end: "{v}") {{
                        track {{
                            title
                            average_review_score
                        }}
                    }}
                }}
            """

            # Send the query using the get_request function and store the response
            track = get_request(query)

            # Extract the track data
            track_data = track.get("data", {}).get("statistics", {}).get("track", {})
            title = track_data.get("title")
            average_review_score = track_data.get("average_review_score")

            # Convert the review score to a percentage out of 100 (multiply by 20)
            average_review_score_str = f"{round(average_review_score * 20, 2)}%" if average_review_score is not None else None

            # Initialize the row with the title on the first iteration
            if row is None:
                row = [title]

            # Append the review score (converted to a percentage) to the row
            row.append(average_review_score_str)

        # If row has been initialized, append it to the slug_data list
        if row:
            slug_data.append(row)

    # Create and return a table (or similar structure) using the collected slug_data
    return create_table(slug_data, sheet)


def get_slugs_with_tag(tag_val):
    # Build the GraphQL query to retrieve track slugs, titles, and their associated tags
    query = f"""query {{
               tracks(organizationSlug: "{config.ORG_SLUG}") {{
                slug
                title
                 trackTags {{
                    value
                 }}
               }}
           }}"""

    # Send the query to the API and store the response data
    data = get_request(query)

    # Initialize empty lists to store the slugs of tracks that match the tag
    tagged_slugs = []

    # Iterate over each track in the response
    for track in data.get('data', {}).get('tracks', []):
        # Check each tag associated with the track
        for tag in track.get('trackTags', []):
            # If the tag value matches the provided tag_val, add the slug and title to the respective lists
            if tag.get('value') == tag_val:
                tagged_slugs.append(track.get('slug'))  # Add the slug of the track
                break  # Stop checking other tags for this track once a match is found

    # Return the list of slugs for tracks that have the matching tag
    return tagged_slugs


def get_unique_invite_stats(i):
    query = f"""
                query {{
                trackInvite(inviteID: "{i}") {{
                    publicTitle
                    claimCount
                    plays {{
                        total_challenges
                        completed_challenges
                        }}
                    }}
                }}
            """

    data = get_request(query)

    # Extract the invite data directly since trackInvite is not a list
    invite = data['data']['trackInvite']
    public_title = invite['publicTitle']
    claim_count = invite['claimCount']

    # List to store rows of extracted data
    rows = []

    # Count the number of plays
    number_of_plays = len(invite['plays'])

    # Aggregate challenges if there are plays
    if number_of_plays > 0:
        total_challenges_sum = 0
        completed_challenges_sum = 0

        for play in invite['plays']:
            total_challenges_sum += play['total_challenges']
            completed_challenges_sum += play['completed_challenges']

        # Calculate the aggregated completion percentage
        completion_percent = round((completed_challenges_sum / total_challenges_sum) * 100,
                                   2) if total_challenges_sum > 0 else 0

        # Append aggregated data
        rows.append([public_title, claim_count, number_of_plays, total_challenges_sum, completed_challenges_sum,
                     completion_percent])
    else:
        # No plays, just add title and claimCount
        rows.append([public_title, claim_count, number_of_plays, None, None, None])

    # Convert the rows to a pandas DataFrame
    df = pd.DataFrame(rows,
                      columns=['PublicTitle', 'ClaimCount', 'NumberOfPlays', 'TotalChallenges', 'CompletedChallenges',
                               'CompletionPercent'])

    # Define the file path where the DataFrame will be saved as a CSV
    file_path = f'outputs/{i}_invite_stats.csv'

    # Write the DataFrame to a CSV file without including the index column
    df.to_csv(file_path, index=False)

    write_to_sheets(file_path, f'Invite Stats for {public_title}')


# Function to convert UTC time to Eastern US time
def convert_to_eastern_us(created_at):
    # Parse the UTC datetime string
    utc_time = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")

    # Define the UTC timezone
    utc_zone = pytz.timezone('UTC')

    # Define the Eastern US timezone
    eastern_zone = pytz.timezone('US/Eastern')

    # Localize the UTC datetime and convert to Eastern US time
    utc_time = utc_zone.localize(utc_time)
    eastern_time = utc_time.astimezone(eastern_zone).strftime("%Y-%m-%d %I:%M %p")

    return eastern_time


# Helper function to check if the invite has expired and was created more than 30 days ago
def is_expired_and_old(expires_at, created_at, current_time):
    if not expires_at or not created_at:
        return False
    expires_at_dt = datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%SZ")
    created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    # Check if invite has expired and was created more than 30 days ago
    return expires_at_dt < current_time and (current_time - created_at_dt) > timedelta(days=30)


# Helper function to extract emails from a section
def extract_emails(entries):
    return "\n".join(
        entry.get('user', {}).get('profile', {}).get('email', '')
        for entry in entries
        if entry.get('user', {}).get('profile', {}).get('email')
    )


def get_invite_stats():
    query = f"""
        query {{
            trackInvites(teamSlug: "{config.ORG_SLUG}") {{
                publicTitle
                claimCount
                expiresAt
                created
                plays {{
                    total_challenges
                    completed_challenges
                }}
                trackEdges {{
                    node {{
                        title
                    }}
                }}
                claims {{
                    user {{
                        profile {{
                            email
                        }}
                    }}
                }}
                authors {{
                    user {{
                        profile {{
                            email
                        }}
                    }}
                }}
            }}
        }}
    """

    # Execute the query
    data = get_request(query)

    # Get current date and time in UTC and convert it to Eastern Time
    current_time_utc = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    current_time_est = convert_to_eastern_us(current_time_utc)

    # List to store rows of extracted data
    rows = []

    # Iterate over the trackInvites in the JSON data
    for invite in data.get('data', {}).get('trackInvites', []):
        expires_at = invite.get('expiresAt')
        created_at_utc = invite.get('created')

        # Skip if invite has expired and was created more than 30 days ago
        if is_expired_and_old(expires_at, created_at_utc, datetime.utcnow()):
            continue

        invite_title = invite.get('publicTitle', 'Unknown Title')
        claim_count = invite.get('claimCount', 0)

        # Extract titles and emails only if they exist
        titles_str = "\n".join(title for edge in invite.get('trackEdges', []) if (title := edge['node'].get('title')))
        emails_str = extract_emails(invite.get('claims', []))
        author_str = extract_emails(invite.get('authors', []))

        # Convert the 'created' time from UTC to Eastern US time
        created_at = convert_to_eastern_us(created_at_utc) if created_at_utc else 'Unknown'

        # Count the number of plays
        plays = invite.get('plays', [])
        number_of_plays = len(plays)

        if number_of_plays > 0:
            # Aggregate challenges and ensure they are integers
            total_challenges_sum = sum(play.get('total_challenges', 0) for play in plays)
            completed_challenges_sum = sum(play.get('completed_challenges', 0) for play in plays)

            # Calculate the aggregated completion percentage
            completion_percent = round((completed_challenges_sum / total_challenges_sum) * 100,
                                       2) if total_challenges_sum > 0 else 0

            # Append aggregated data
            rows.append([
                invite_title, claim_count, number_of_plays, total_challenges_sum,
                completed_challenges_sum, completion_percent, titles_str, emails_str, created_at, author_str
            ])

        else:
            # No plays, just add title, claimCount, and emails
            rows.append([invite_title, claim_count, number_of_plays, None, None, None, titles_str, emails_str])

    # Update the column headers, adding the current EST time to "Invite Title"
    column_headers = [
        f"Invite Title (run {current_time_est})", 'Claim Count', 'Plays', 'Total Challenges', 'Completed Challenges',
        'Completion Percent', 'Tracks in Invite', 'Users who Claimed', 'Invite Creation Date (EST)', 'Invite Author',
    ]

    # Convert the rows to a pandas DataFrame
    df = pd.DataFrame(rows, columns=column_headers)

    # Define the file path where the DataFrame will be saved as a CSV
    file_path = 'outputs/invite_stats.csv'

    # Write the DataFrame to a CSV file without including the index column
    df.to_csv(file_path, index=False)

    write_to_sheets(file_path, 'Invite Stats')


def is_token_valid():
    try:
        # Read the credentials file
        with open(config.credentials_file, 'r') as f:
            credentials = json.load(f)

        # Get the expiration time from the credentials (epoch time)
        expires_at = credentials.get('expires')

        if expires_at is None:
            print("Expiration time not found in credentials.")
            return False

        # Get the current time (epoch time)
        current_time = int(time.time())

        # Check if the token is still valid
        if current_time < expires_at:
            return True
        else:
            return False

    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading credentials file: {e}")
        return False


def renew_token():
    try:
        # Use Popen to send '1' automatically when prompted
        process = subprocess.Popen("instruqt auth login", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)

        # Automatically send '1' when prompted
        stdout, stderr = process.communicate(input='1\n')

        # Check if the command executed successfully
        if process.returncode != 0:
            print(f"Error: {stderr}")
            return

        # Retrieve the updated token from the credentials file using jq
        config.ACCESS_TOKEN = subprocess.check_output(
            "jq -r .access_token ~/.config/instruqt/credentials", shell=True, text=True
        ).strip()

        print("Token renewed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to renew token: {e}")


def check_and_renew_token():
    # Check if the current token is valid using the is_token_valid function
    if is_token_valid():
        # If the token is still valid, print a confirmation message
        print("Token is valid.")
    else:
        # If the token has expired or is invalid, print a message and renew the token
        print("Token has expired or is invalid. Renewing token...")
        # Call the renew_token function to refresh the token
        renew_token()
