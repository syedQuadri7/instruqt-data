import json
import subprocess
import time
import pandas as pd
import requests
import config
import utilities


def get_request(q):
    """
    Sends a POST request to the API endpoint defined in the config.
    The request contains a query, and the response is returned as JSON.
    """
    return requests.post(config.ENDPOINT, headers={"Authorization": "Bearer " + config.ACCESS_TOKEN},
                         json={"query": q}).json()


def get_track_plays_by_month(track_slugs):
    """
    Queries the API for the track plays by month for each track slug.
    Returns a table of results with track titles and their corresponding plays per month.
    """
    dates = utilities.month_map(config.YEAR)
    slug_data = []
    for track_slug in track_slugs:
        print(track_slug)
        row = []
        for k, v in dates.items():
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

            track = get_request(query)

            title = track["data"]["statistics"]["track"]["title"]
            started_total = track["data"]["statistics"]["track"]["started_total"]
            if title not in row:
                row.append(title)
            row.append(started_total)

        slug_data.append(row)
    return create_table(slug_data)


def get_track_slugs():
    """
        Queries the API for all track slugs associated with the organization.
        Returns a list of track slugs.

        Usage:
        1. Ensure that the 'config.py' file contains the correct organization slug (ORG_SLUG).
        2. This function makes a request to the API and retrieves all available track slugs for the organization.
        3. The function returns a list of slugs, which can be used for other queries like fetching track statistics.

        Example:
            track_slugs = get_track_slugs()

        Output:
        A list of strings where each string is a track slug, for example:
        ['track1', 'track2', 'track3']

        Dependencies:
        - Requires a properly configured 'config.py' file with `ORG_SLUG`.
        - Requires the `get_request` function to handle API communication.

        Note:
        - Ensure you have network access and a valid access token to query the API.
        """
    query = f"""query {{
           tracks(organizationSlug: "{config.ORG_SLUG}") {{
             slug
           }}
       }}"""

    output = get_request(query)
    slugs = [track['slug'] for track in output['data']['tracks']]
    return slugs


def create_table(data):
    """
    Creates a table (DataFrame) from the provided data and exports it to a file.
    """
    # Define the months as the column headers
    months = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']

    # Extract the topics and values from the data
    topics = [item[0] for item in data]
    values = [item[1:] for item in data]

    # Create the DataFrame with topics as the index and months as the columns
    df = pd.DataFrame(values, index=topics, columns=months)

    file_path = f'tracks_by_month.csv'
    df.to_csv(file_path)

    print(f"Data has been saved to {file_path}")


def get_tracks_scores(track_slugs):
    """
    Queries the API for each track's statistics such as title, total started, total completed,
    and average review score. It computes the percentage of completions and saves the data
    to a CSV file.

    Usage:
    1. Provide a list of track slugs as input. For example:
        track_slugs = ['track1', 'track2', 'track3']
    2. Ensure that the 'config.py' file contains proper configurations, such as ORG_SLUG.
    3. The function will create an output file 'track_scores.csv' in the 'outputs' directory,
       containing the statistics for each track.

    Example:
        track_slugs = ['slug1', 'slug2']
        get_tracks_scores(track_slugs)

    Output:
    A CSV file named 'track_scores.csv' with the following columns:
    - Title: The title of the track.
    - Started: The total number of users who started the track.
    - Completed: The total number of users who completed the track.
    - Percent Completed: The percentage of users who completed the track.
    - Average Review Score: The average review score for the track.
    """
    # Initialize an empty list to hold the data for each track
    d = []

    # Iterate over each track slug and make a query for each
    for track_slug in track_slugs:
        # Define the query for the specific track_slug
        query = f"""
            query {{
                statistics(trackSlug: "{track_slug}", organizationSlug: "{config.ORG_SLUG}") {{
                    track {{
                        title
                        started_total
                        completed_total
                        average_review_score
                    }}
                }}
            }}
        """

        # Get data for this specific track
        data = get_request(query)

        # Extract relevant statistics from the response
        track_data = data['data']['statistics']['track']
        title = track_data['title']
        started = track_data['started_total']
        completed = track_data['completed_total']
        average_review_score = track_data['average_review_score']

        # Calculate percent completed and round to 2 decimal places
        percent_completed = round((completed / started * 100), 2) if started > 0 else 0.00

        # Round average_review_score to 2 decimal places, but only if it's not None
        if average_review_score is not None:
            average_review_score = round(average_review_score, 2)

        # Append the row to the data list
        d.append({
            'Title': title,
            'Started': started,
            'Completed': completed,
            'Percent Completed': percent_completed,
            'Average Review Score': average_review_score
        })

    # Create a DataFrame from the data list
    df = pd.DataFrame(d)

    # Write the DataFrame to a CSV file
    file_path = f'track_scores.csv'
    df.to_csv(file_path, index=False)


def get_slugs_with_tag(tag_val):
    """
    Queries the API for tracks based on a specific tag value.
    Writes the track titles associated with that tag to a text file.
    Returns the track slugs that match the tag.
    """
    query = f"""query {{
               tracks(organizationSlug: "{config.ORG_SLUG}") {{
                slug
                title
                 trackTags {{
                    value
                 }}
               }}
           }}"""

    data = (get_request(query))

    tagged_slugs = []
    tagged_titles = []
    for track in data.get('data', {}).get('tracks', []):
        for tag in track.get('trackTags', []):
            if tag.get('value') == tag_val:
                tagged_slugs.append(track.get('slug'))
                tagged_titles.append(track.get('title'))
                break

    write_list_to_file(tagged_titles, tag_val)
    return tagged_slugs


def write_list_to_file(lines, name):
    """
    Writes the provided list of lines to a file under the 'outputs' directory.
    """
    name = f"outputs/{name}_tag_output.txt"
    with open(name, 'w') as f:
        for line in lines:
            f.write(f"{line}\n")


def is_token_valid():
    """
    Checks if the stored token in the credentials file is still valid.
    Returns True if valid, False otherwise.
    """
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
    """
    Renews the API token by running the 'instruqt auth login' command.
    """
    try:
        # Run the instruqt auth login command to renew the token
        subprocess.run("instruqt auth login", shell=True, check=True)
        print("Token renewed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to renew token: {e}")


def check_and_renew_token():
    """
    Checks if the token is valid; if not, renews the token.
    """
    if is_token_valid():
        print("Token is still valid.")
    else:
        print("Token has expired or is invalid. Renewing token...")
        renew_token()
