# Instruqt Track API

## Prerequisites

- Ensure Python 3.x is installed on your system. You can download it
  from [python.org](https://www.python.org/downloads/).
- Familiar with Python syntax and running Python code.

## Installation

### Step 1: Clone the repository

1. Git clone this repo

### Step 2: Create a virtual environment

A virtual environment ensures that the dependencies required by this project do not conflict with other Python projects
on your machine.

- On macOS/Linux:
    1. python3 -m venv venv
    2. source venv/bin/activate

### Step 3: Install the required dependencies

Dependencies are external libraries or packages needed to run this project. Use `pip`, the Python package manager, to
install them:

1. pip install -r requirements.txt

This will install all the required packages listed in the `requirements.txt` file.

### Step 4: Deactivate the virtual environment (when done)

To stop using the virtual environment, run:

```
deactivate
```

You will need to reactivate it (Step 2) each time you work on the project.

This repository provides functions to retrieve, process, and save statistics about learning tracks. The functions
interact with an API to fetch track slugs, monthly play statistics, and review scores. Below are detailed usage
instructions for each function.

## Functions Overview

### 1. get_slugs_with_tag(tag_val)

Fetches all track slugs that have the specified tag.

#### Usage:

```
tracks_tagged = func.get_slugs_with_tag("terraform")
```

Input: tag_val (string) - The tag value to search for (e.g., "terraform").

Output: List of slugs for tracks that are tagged with the given value.

Side effect: Saves the titles of the tagged tracks to a file `outputs/{tag_val}_tag_output.txt`.

### 2. get_track_slugs()

Retrieves all available track slugs and titles for the specified organization.

#### Usage:

```
tracks_all = func.get_track_slugs()
```

Input: None.

Output: List of all track slugs.

Side effect: Saves track titles to `outputs/all_tracks_output.txt`.

### 3. get_track_plays_by_month(track_slugs)

Fetches monthly play statistics for the provided list of track slugs.

```
func.get_track_plays_by_month(tracks_tagged)
```

Input: track_slugs (list) - A list of track slugs.

Output: None.

Side effect: Saves monthly play statistics to `outputs/tracks_by_month.csv`.

### 4. get_tracks_scores(track_slugs)

Retrieves completion statistics and average review scores for the provided track slugs.

```
func.get_tracks_scores(tracks_all)
```

Input: track_slugs (list) - A list of track slugs.

Output: None.

Side effect: Saves completion and review scores to `outputs/track_scores.csv`.

### 5. get_unique_invite_stats(i)

Retrieves aggregated completion statistics for a specific invite ID.

```
func.get_unique_invite_stats("inviteID123")
```

Input: i (string) - A unique invite ID (Identifier).

Output: None.

Side effect: Saves completion statistics to `outputs/{inviteID}_invite_stats.csv`.

### 6. get_invite_stats()

Retrieves completion statistics for all invites associated with the organization.

```
func.get_invite_stats()
```

Input: None.

Output: None.

Side effect: Saves completion statistics to `outputs/invite_stats.csv`.

## Example Workflow

The functions below have customizable parameter values. Use the [Functions Overview](#functions-overview-) section as a
reference for what parameters are acceptable.

When you run the script, the code inside `main()` will execute. All the functions must be run from the main function.

> [!IMPORTANT]
> The `func.check_and_renew_token()` function must be the first line in the `main()` function since this will verify
> your
> authentication with instruqt.

### Get slugs for tracks tagged with "terraform":

```
tracks_tagged = func.get_slugs_with_tag("terraform")
```

### Get slugs for all tracks:

```
tracks_all = func.get_track_slugs()
```

### Get monthly play statistics for tracks:

```
func.get_track_plays_by_month(tracks)
```

### Get completion and review scores for all tracks:

```
func.get_tracks_scores(tracks_all)
```

### Get statistics for a specific invite by its ID:

```
invite_id = "inviteID123"
func.get_unique_invite_stats(invite_id)
```

You can get the invite_id by navigating to [Instruqt invites](https://play.instruqt.com/manage/hashicorp/invites,
selecting an invite, and then copying the value of the `Identifier` field.

### Get statistics for all invites associated with the team:

```
func.get_invite_stats()
```