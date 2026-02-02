import json
import sys

def evaluate_soc(student_path, key_path):
    with open(student_path) as f:
        student = json.load(f)

    with open(key_path) as f:
        key = json.load(f)

    score = 0
    feedback = []

    # IOC check
    if key["malicious_ip"] in student.get("ioc_list", []):
        score += 40
    else:
        feedback.append("Missing malicious IP.")

    # MITRE check
    if all(t in student.get("mitre_mapping", []) for t in key["expected_mitre"]):
        score += 40
    else:
        feedback.append("Incorrect MITRE mapping.")

    # Detection rule check
    if key["malicious_ip"] in student.get("detection_rule", ""):
        score += 20
    else:
        feedback.append("Detection rule incomplete.")

    return {"soc_score": score, "soc_feedback": feedback}

if __name__ == "__main__":
    print(json.dumps(
        evaluate_soc(sys.argv[1], sys.argv[2]),
        indent=4
    ))
