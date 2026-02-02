# Scenario 03 — AWS Cloud Compromise (Advanced)

## Overview

In this scenario, you will investigate a multi-stage intrusion in an AWS-like cloud environment.

An attacker has:

- Logged in as a cloud engineer from an unusual region
- Escalated privileges by creating access keys and attaching policies
- Enumerated S3 buckets and objects
- Accessed sensitive data
- Exfiltrated data to an external bucket

You will analyze:

- IAM logs (`iam.csv`)
- API call logs (`api_calls.csv`)
- S3 access logs (`storage_access.csv`)

Your goals:

1. Identify the compromised user
2. Identify the attacker IP and region
3. Identify privilege escalation events
4. Identify sensitive data access and exfiltration
5. Map activity to MITRE ATT&CK (cloud techniques)
6. Train an ML model to detect anomalous behavior
7. Generate structured outputs for automated grading

## Logs

- `logs/iam.csv` — IAM/CloudTrail-style events
- `logs/api_calls.csv` — API calls (discovery, collection, exfiltration)
- `logs/storage_access.csv` — S3-style access logs

## Deliverables

Your main notebook **must** generate:

- `student_output/soc_output.json`
- `student_output/ml_output.json`

These are consumed by the evaluation scripts and CI.

## Optional Deep-Dive Notebooks

- `soc_tasks/deep_dive_soc.ipynb` — Advanced SOC investigation
- `ml_tasks/deep_dive_ml.ipynb` — Advanced ML modeling

These are enrichment only and are not required for grading.
