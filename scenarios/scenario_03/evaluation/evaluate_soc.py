import json
import sys


def evaluate_soc(student_path, key_path):
    with open(student_path) as f:
        student = json.load(f)

    with open(key_path) as f:
        key = json.load(f)

    score = 0
    feedback = []

    iocs = student.get("ioc_list", [])
    mitre = student.get("mitre_mapping", [])
    triage = student.get("triage_summary", "")
    detection_rule = student.get("detection_rule", "")

    # Compromised user
    if key["compromised_user"] in iocs:
        score += 20
    else:
        feedback.append("Compromised user not clearly identified in IOCs.")

    # Attacker IP
    if key["attacker_ip"] in iocs:
        score += 20
    else:
        feedback.append("Attacker IP missing from IOCs.")

    # Sensitive bucket
    if key["sensitive_bucket"] in iocs:
        score += 15
    else:
        feedback.append("Sensitive bucket not identified as an IOC.")

    # Exfil bucket
    if key["attacker_bucket"] in iocs:
        score += 15
    else:
        feedback.append("Exfiltration bucket not identified as an IOC.")

    # MITRE mapping
    if all(t in mitre for t in key["expected_mitre"]):
        score += 20
    else:
        feedback.append("MITRE ATT&CK mapping incomplete or incorrect.")

    # Triage summary
    if len(triage.strip()) > 40:
        score += 5
    else:
        feedback.append("Triage summary too short or lacking detail.")

    # Detection rule
    if any(x in detection_rule for x in [key["attacker_ip"], key["sensitive_bucket"], key["attacker_bucket"]]):
        score += 5
    else:
        feedback.append("Detection rule does not clearly target attacker behavior.")

    return {"soc_score": score, "soc_feedback": feedback}


if __name__ == "__main__":
    print(json.dumps(
        evaluate_soc(sys.argv[1], sys.argv[2]),
        indent=4
    ))
