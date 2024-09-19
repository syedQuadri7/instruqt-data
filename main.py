import func
import time


def main():
    # Start time
    start_time = time.time()

    print("Starting...")

    func.check_and_renew_token()

    # tagged_vault = func.get_slugs_with_tag("vault")
    # tagged_terraform = func.get_slugs_with_tag("terraform")
    # tagged_nomad = func.get_slugs_with_tag("nomad")
    # tagged_consul = func.get_slugs_with_tag("consul")
    # tagged_hvd = func.get_slugs_with_tag("hvd")
    # tracks_all = func.get_track_slugs()

    test = ['database-secrets-engine']
    func.get_track_plays_by_month(test, "test")

    # func.get_invite_stats()
    #
    # func.get_track_plays_by_month(tracks_all, "All Track plays by Month - FY25")
    # func.get_track_plays_by_month(tagged_hvd, "HVD Track plays by Month - FY25")
    #
    # func.get_tracks_review_score_by_month(tracks_all, "All Track Completion Rate by Month - FY25")
    # func.get_tracks_review_score_by_month(tagged_hvd, "HVD Track Completion Rate by Month - FY25")
    #
    # func.get_tracks_review_score_by_month(tracks_all, "All Tracks Average Happiness Score by Month - FY25")
    # func.get_tracks_review_score_by_month(tagged_hvd, "HVD Tracks Average Happiness Score by Month - FY25")


    print("...Ending")

    # End time
    end_time = time.time()

    # Calculate the runtime
    runtime = end_time - start_time

    # Convert runtime to seconds
    minutes, seconds = divmod(runtime, 60)

    # Output the result
    print(f"Runtime: {int(minutes)} minutes and {seconds:.2f} seconds")


if __name__ == "__main__":
    main()
