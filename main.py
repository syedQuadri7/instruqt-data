import func


def main():
    # func.check_and_renew_token()

    tagged_vault = func.get_slugs_with_tag("vault")
    tagged_terraform = func.get_slugs_with_tag("terraform")
    tagged_nomad = func.get_slugs_with_tag("nomad")
    tagged_consul = func.get_slugs_with_tag("consul")
    tagged_hvd = func.get_slugs_with_tag("hvd")
    tracks_all = func.get_track_slugs()

    # func.get_invite_stats()
    #
    # i = "xjsnltkjyjrg"
    #
    # func.get_unique_invite_stats(i)

    # Fetch track plays by month for HVD tracks for FY25
    func.get_track_plays_by_month(tagged_hvd, "HVD Track plays by Month - FY25")

    # # Fetch track plays by month for Consul tracks for FY25
    # func.get_track_plays_by_month(tagged_consul, "Consul Track plays by Month - FY25")
    #
    # # Fetch track plays by month for Terraform tracks for FY25
    # func.get_track_plays_by_month(tagged_terraform, "Terraform Track plays by Month - FY25")
    #
    # # Fetch track plays by month for Vault tracks for FY25
    # func.get_track_plays_by_month(tagged_vault, "Vault Track plays by Month - FY25")
    #
    # # Fetch track plays by month for Nomad tracks for FY25
    # func.get_track_plays_by_month(tagged_nomad, "Nomad Track plays by Month - FY25")
    #
    # # Fetch track plays by month for all tracks for FY25
    # func.get_track_plays_by_month(tracks_all, "All Track plays by Month - FY25")
    #
    # # Fetch track completion rate by month for HVD tracks for FY25
    # func.get_tracks_completion_by_month(tagged_hvd, "HVD Track completion rate by Month - FY25")
    #
    # # Fetch track completion rate by month for Consul tracks for FY25
    # func.get_tracks_completion_by_month(tagged_consul, "Consul Track completion rate by Month - FY25")
    #
    # # Fetch track completion rate by month for Terraform tracks for FY25
    # func.get_tracks_completion_by_month(tagged_terraform, "Terraform Track completion rate by Month - FY25")
    #
    # # Fetch track completion rate by month for Vault tracks for FY25
    # func.get_tracks_completion_by_month(tagged_vault, "Vault Track completion rate by Month - FY25")
    #
    # # Fetch track completion rate by month for Nomad tracks for FY25
    # func.get_tracks_completion_by_month(tagged_nomad, "Nomad Track completion rate by Month - FY25")
    #
    # # Fetch track completion rate by month for all tracks for FY25
    # func.get_tracks_completion_by_month(tracks_all, "All Track completion rate by Month - FY25")
    #
    # # Fetch average review scores by month for HVD tracks for FY25
    # func.get_tracks_review_score_by_month(tagged_hvd, "HVD Tracks Average Review by Month - FY25")
    #
    # # Fetch average review scores by month for Consul tracks for FY25
    # func.get_tracks_review_score_by_month(tagged_consul, "Consul Tracks Average Review by Month - FY25")
    #
    # # Fetch average review scores by month for Terraform tracks for FY25
    # func.get_tracks_review_score_by_month(tagged_terraform, "Terraform Tracks Average Review by Month - FY25")
    #
    # # Fetch average review scores by month for Vault tracks for FY25
    # func.get_tracks_review_score_by_month(tagged_vault, "Vault Tracks Average Review by Month - FY25")
    #
    # # Fetch average review scores by month for Nomad tracks for FY25
    # func.get_tracks_review_score_by_month(tagged_nomad, "Nomad Tracks Average Review by Month - FY25")
    #
    # # Fetch average review scores by month for all tracks for FY25
    # func.get_tracks_review_score_by_month(tracks_all, "All Tracks Average Review by Month - FY25")

    print("Everything is done")


if __name__ == "__main__":
    main()
