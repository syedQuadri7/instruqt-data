import func


def main():
    func.check_and_renew_token()

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

    func.get_track_plays_by_month(tagged_nomad, "Nomad Tracks by Month - FY25")

    # func.get_tracks_completion_by_month(tagged_terraform, "Terraform Tracks Completion Rate - FY25")
    #
    # func.get_tracks_review_score_by_month(tagged_vault, "Vault Tracks Average Review - FY25")

    print("Everything is done")


if __name__ == "__main__":
    main()
