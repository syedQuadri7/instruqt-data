import json

import func
import config


# Usage Instructions:
# This script is designed to interact with an API, retrieve data for various tracks, and process the data.
# Ensure the following:
# 1. The `config.py` file must contain proper configurations, such as ENDPOINT, ACCESS_TOKEN, ORG_SLUG, etc.
# 2. `utilities.py` should have a `month_map` function that maps months to start and end dates.
# 3. Ensure valid credentials and use the token renewal function to maintain access.

def main():
    func.check_and_renew_token()

    # tracks_tagged = func.get_slugs_with_tag("terraform")
    #
    # tracks_all = func.get_track_slugs()
    #
    # func.get_track_plays_by_month(tracks_tagged)
    #
    # func.get_tracks_scores(tracks_all)
    # func.get_invite_stats()

    i = "xjsnltkjyjrg"
    func.get_unique_invite_stats(i)

    hvd_tracks = ["health-assessments-and-run-tasks",
                  "terraform-modules-testing-and-lifecycle",
                  "vcdl-888-sentinel-module-development",
                  "sentinel-pac-lifecycle-management",
                  "terraform-agents",
                  "terraform-git-flow",
                  "terraform-cloud-consumer-workflow",
                  "terraform-cloud-variables",
                  "dynamic-credentials-terraform-cloud",
                  "terraform-control-workspaces",
                  "terraform-landing-zone-provisioning-workflow",
                  "terraform-modules",
                  "terraform-packer",
                  "policy-as-code-introduction-terraform",
                  "tfc-private-module-registry",
                  "tfc-proj-wkspc-conf",
                  "autopilot-configuration-and-operations",
                  "database-secrets-engine",
                  "deployment-and-backup-basics",
                  "vault-dr-recovery-operations",
                  "enterprise-cluster-audit-logs",
                  "hvd-enterprise-cluster-configuration-policy--governance-exercise",
                  "using-vault-basic-concepts",
                  "mfa-with-vault-enterprise",
                  "vault-agent-templating-and-pki-workflow-hvd",
                  "vault-agent-templating-and-pki",
                  "vault-authentication-basics",
                  "vault-dynamic-secrets-with-cloud-engines-hvd",
                  "vault-static-secret-basics",
                  "consul-enterprise-business-continuity-and-upgrade",
                  "enterprise-cluster-configuration",
                  "enterprise-cluster-dns-configuration"]

    print("Everything is done")


if __name__ == "__main__":
    main()
