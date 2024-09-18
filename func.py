import csv
import json
import os
import subprocess
import time
import pandas as pd
import requests
from gspread import WorksheetNotFound

import config
import utilities
from datetime import datetime
import gspread


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
        gc = gspread.service_account(filename='service_account.json')

        spreadsheet = gc.open('Instruqt Metrics')

        # Try to open the worksheet by title, or create it if it doesn't exist
        try:
            worksheet = spreadsheet.worksheet(sheet)
        except WorksheetNotFound:
            # If the sheet doesn't exist, create a new one
            worksheet = spreadsheet.add_worksheet(title=sheet, rows=300, cols=100)
        # Read the CSV file
        with open(f'{path}', newline='') as csvfile:
            reader = list(csv.reader(csvfile))

        # Resize the worksheet to fit the CSV data
        worksheet.resize(rows=len(reader), cols=len(reader[0]))

        # Update the worksheet with the CSV data
        worksheet.update('A1', reader)

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
    # Define the months as the column headers for the table (from Feb to Jan)
    months = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']

    # Extract the topics (track titles) from the first element of each sublist in data
    topics = [item[0] for item in data]

    # Extract the values (started_total plays per month) from the rest of each sublist in data
    values = [item[1:] for item in data]

    # Create a pandas DataFrame with the values, using the topics as the index (row labels) and months as the columns
    df = pd.DataFrame(values, index=topics, columns=months)

    # Define the file path where the CSV file will be saved
    file_path = 'outputs/data.csv'

    # Save the DataFrame to a CSV file
    df.to_csv(file_path)

    return write_to_sheets(file_path, sheet)


def get_tracks_completion_by_month(track_slugs, sheet):
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
                            completed_total
                        }}
                    }}
                }}
            """

            # Send the query using the get_request function and store the response
            track = get_request(query)

            # Extract the track title, started_total, and completed_total from the response
            title = track["data"]["statistics"]["track"]["title"]
            started_total = track["data"]["statistics"]["track"]["started_total"]
            completed_total = track["data"]["statistics"]["track"]["completed_total"]

            # Calculate the percentage of completed courses, rounded to 2 decimal places
            # If no courses were started, set percent_completed to 0.00
            percent_completed = round((completed_total / started_total * 100), 2) if started_total > 0 else 0.00

            # If the track title is not already in the row, append it (to avoid duplication)
            if title not in row:
                row.append(title)

            # Append the completion percentage for the current month to the row
            row.append(percent_completed)

        # After processing all months, append the row data for this track slug to the slug_data list
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
                            average_review_score
                        }}
                    }}
                }}
            """

            # Send the query using the get_request function and store the response
            track = get_request(query)

            # Extract the track title and average review score from the response
            title = track["data"]["statistics"]["track"]["title"]
            average_review_score = track["data"]["statistics"]["track"]["average_review_score"]

            # Round the average review score to 2 decimal places, if it exists (not None)
            if average_review_score is not None:
                average_review_score = round(average_review_score, 2)
            else:
                average_review_score = 0.00  # Handle None case

            # If the track title is not already in the row, append it (to avoid duplication)
            if title not in row:
                row.append(title)

            # Append the average review score for the current month to the row
            row.append(average_review_score)

        # After processing all months, append the row data for this track slug to the slug_data list
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


def get_invite_stats():
    query = f"""
            query {{
            trackInvites(teamSlug: "{config.ORG_SLUG}") {{
                publicTitle
                claimCount
                expiresAt
                plays {{
                    total_challenges
                    completed_challenges
                    }}
                }}
            }}
        """

    data = get_request(query)

    # Get current date and time
    current_time = datetime.utcnow()

    # List to store rows of extracted data
    rows = []

    # Iterate over the trackInvites in the JSON data
    for invite in data['data']['trackInvites']:
        public_title = invite['publicTitle']
        claim_count = invite['claimCount']
        expires_at = invite.get('expiresAt')

        # Check if the invite has expired
        if expires_at:
            expires_at_dt = datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%SZ")
            if expires_at_dt < current_time:
                continue

        # Count the number of plays
        number_of_plays = len(invite['plays'])

        # Aggregate challenges if there are plays
        if invite['plays']:
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
    file_path = 'outputs/invite_stats.csv'

    # Write the DataFrame to a CSV file without including the index column
    df.to_csv(file_path, index=False)


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
        # Run the instruqt auth login command to renew the token
        subprocess.run("instruqt auth login", shell=True, check=True)

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
