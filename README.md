# Instruqt Track API

## Installation

### Step 1: Clone the repository

1. Git clone this repo

### Step 2: Create a virtual environment

1. python3 -m venv venv 
2. source venv/bin/activate

### Step 3: Install the required dependencies

1. pip install -r requirements.txt

### Step 4: Deactivate the virtual environment (when done)

1. deactivate

This repository provides functions to retrieve, process, and save statistics about learning tracks. The functions interact with an API to fetch track slugs, monthly play statistics, and review scores. Below are detailed usage instructions for each function.

## Functions Overview

### 1. `get_slugs_with_tag(tag_val)`
Fetches all track slugs that have the specified tag.

#### Usage:
```python
tracks_tagged = func.get_slugs_with_tag("terraform")
```
Input: tag_val (string) - The tag value to search for (e.g., "terraform").

Output: List of slugs for tracks that are tagged with the given value.

Side effect: Saves the titles of the tagged tracks to a file `outputs/{tag_val}_tag_output.txt`.

### 2. get_track_slugs()
Retrieves all available track slugs and titles for the specified organization.

#### Usage:
```python
tracks_all = func.get_track_slugs()
```
Input: None.

Output: List of all track slugs.

Side effect: Saves track titles to `outputs/all_tracks_output.txt`.

### 3. get_track_plays_by_month(track_slugs)
Fetches monthly play statistics for the provided list of track slugs.
```python
func.get_track_plays_by_month(tracks_tagged)
```

Input: track_slugs (list) - A list of track slugs.

Output: None.

Side effect: Saves monthly play statistics to `outputs/tracks_by_month.csv`.

### 4. get_tracks_scores(track_slugs)
Retrieves completion statistics and average review scores for the provided track slugs.
```python
func.get_tracks_scores(tracks_all)
```

Input: track_slugs (list) - A list of track slugs.

Output: None.

Side effect: Saves completion and review scores to `outputs/track_scores.csv`.

## Example Workflow


### Get slugs for tracks tagged with "terraform":
```python
tracks_tagged = func.get_slugs_with_tag("terraform")
```

### Get slugs for all tracks:
```python
tracks_all = func.get_track_slugs()
```

### Get monthly play statistics for tagged tracks:
```python
func.get_track_plays_by_month(tracks_tagged)
```

### Get completion and review scores for all tracks:

```python
func.get_tracks_scores(tracks_all)
```