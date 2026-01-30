import json
import sys
import os

EXPECTED_IOCS = ["185.199.110.153"]
EXPECTED_MITRE = ["T1078", "T1021"]

def evaluate_soc(path):
    with open(path, "r") as f:
        data = json.load(f)

    score = 0
    feedback = []

    #IOC Check
    if any(ioc in data.get("ioc_list", []) for ioc in EXPECTED_IOCS):
        score += 40
    else:
        feedback.append("Missing expected IOC(s).")

    # MITRE Check
    if any(m in data.get("mitre_mapping", []) for m in EXPECTED_MITRE):
        score += 40
    else:
        feedback.append("Incorrect MITRE ATT&CK mapping.")

    #Detection rule check
    if "185.199.110.153" in data.get("detection_rules", ""):
        score += 20
    else:
        feedback.append("Detection rule does not match suspicious IP.")
    
    return {
        "soc_score": score,
        "soc_feedback": feedback
    }

if __name__ == "__main__":
    result = evaluate_soc(sys.argv[1])
    print(json.dumps(result, indent=4))