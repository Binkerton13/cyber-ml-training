# Scenario 02 — Lateral Movement in a Windows Domain (Intermediate)

## Overview
In this scenario, you will investigate a multi-stage intrusion involving credential theft and lateral movement across a Windows domain. You will analyze authentication logs, process creation logs, and network connection logs to identify suspicious activity.

You will:
- Identify patient zero
- Trace lateral movement
- Extract Indicators of Compromise (IOCs)
- Map activity to MITRE ATT&CK
- Train an ML model to detect anomalous process or network behavior
- Produce structured SOC + ML outputs for automated grading

## Logs Provided
- `auth.csv` — Authentication events
- `process.csv` — Windows process creation events
- `network.csv` — Network connections between hosts

## Attack Summary
An attacker compromises a workstation, steals credentials, and moves laterally to a file server. They stage data and attempt exfiltration.

Your job is to uncover the full attack chain.

## Deliverables
Your notebook must generate:
- `soc_output.json`
- `ml_output.json`
- `report.md`

These will be automatically evaluated by GitHub Actions.
