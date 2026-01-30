# Scenario 01 — Suspicious Login + Lateral Movement (Guided)

## Overview
In this guided scenario, you will investigate a suspicious login event and determine whether it represents malicious activity. You will perform both SOC-style log triage and ML-based anomaly detection.

This scenario teaches:
- How to analyze authentication logs
- How to extract Indicators of Compromise (IOCs)
- How to map activity to MITRE ATT&CK
- How to engineer features for anomaly detection
- How to train a simple ML model to score suspicious events
- How to combine SOC reasoning with ML output

---

## Scenario Narrative
A user account (`j.smith`) has logged in from an unusual IP address. Shortly afterward, the account accessed a server it normally never interacts with. Your job is to determine whether this activity is suspicious.

You will:
1. Review authentication logs
2. Identify anomalies manually (SOC analysis)
3. Train an anomaly detection model on historical login data
4. Compare your SOC findings with the ML model output
5. Produce a final report

---

## Tasks

### **Task 1 — SOC Analysis**
- Load the authentication logs
- Identify unusual login patterns
- Extract IOCs (IP, hostname, timestamps)
- Map activity to MITRE ATT&CK
- Write a detection rule (YAML or JSON)

### **Task 2 — ML Analysis**
- Load the historical login dataset
- Engineer features (hour, geo distance, device change)
- Train an anomaly detection model
- Score the suspicious login
- Explain the model output

### **Task 3 — Final Report**
- Compare SOC vs ML findings
- Explain whether the activity is malicious
- Provide recommendations

---

## Deliverables
Your notebook will automatically generate:

- `soc_output.json`
- `ml_output.json`
- `report.md`

These will be pushed to GitHub for automated evaluation.

---

## Good luck — and have fun learning!
