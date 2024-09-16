import func

# Usage Instructions:
# This script is designed to interact with an API, retrieve data for various tracks, and process the data.
# Ensure the following:
# 1. The `config.py` file must contain proper configurations, such as ENDPOINT, ACCESS_TOKEN, ORG_SLUG, etc.
# 2. `utilities.py` should have a `month_map` function that maps months to start and end dates.
# 3. Ensure valid credentials and use the token renewal function to maintain access.

def main():
    func.check_and_renew_token()

    tracks_tagged = func.get_slugs_with_tag("vault")

    # tracks_all = func.get_track_slugs()
    #
    # func.get_track_plays_by_month(tracks_tagged)
    #
    # func.get_tracks_scores(tracks_all)
    #
    # func.get_invite_stats()
    #
    # i = "xjsnltkjyjrg"
    #
    # func.get_unique_invite_stats(i)

    print("Everything is done")


if __name__ == "__main__":
    main()
