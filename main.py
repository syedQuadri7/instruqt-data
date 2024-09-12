import json

import config
import func
from func import get_request, compile_message, get_hotpool_violations, get_track_slugs, get_tracks_scores



def main():
    # func.check_and_renew_token()

    get_hotpool_violations()

    tracks_tagged = func.get_slugs_with_tag("terraform")
    #
    # tracks_all = func.get_track_slugs()
    #
    # func.get_track_plays_by_month(tracks_tagged)

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

    # query = f"""query {{
    #            tracks(organizationSlug: "{config.ORG_SLUG}") {{
    #              slug
    #              statistics {{
    #                 title
    #                 started_total
    #                 completed_total
    #                 average_review_score
    #                 }}
    #            }}
    #        }}"""
    #
    # print(get_request(query))
    #
    #
    # get_tracks_scores("scores")




if __name__ == "__main__":
    main()
