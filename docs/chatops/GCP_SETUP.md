# GCP WIF Setup (TL;DR)
1) Workload Identity Pool+Provider ל-GitHub OIDC (issuer: https://token.actions.githubusercontent.com).
2) attribute.repository == 'edri2or-commits/make-ops-clean'.
3) roles/iam.workloadIdentityUser ל-SA שב-${GCP_SA_EMAIL}.
4) שתפו את ה-Spreadsheet (${SHEET_ID}) עם ה-SA כ-Editor.
