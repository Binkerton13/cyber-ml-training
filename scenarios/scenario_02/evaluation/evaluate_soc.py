import json
import sys

def evaluate_soc(student_path, key_path):
    with open(student_path) as f:
        student = json.load(f)

    with open(key_path) as f:
        key = json.load(f)

    score = 0
    feedback = []

    if key["attacker_ip"] in student.get("ioc_list", []):
        score += 30
    else:
        feedback.append("Missing attacker IP.")

    if key["malicious_process"] in student.get("ioc_list", []):
        score += 30
    else:
        feedback.append("Missing malicious process.")

    if all(t in student.get("mitre_mapping", []) for t in key["expected_mitre"]):
        score += 40
    else:
        feedback.append("MITRE mapping incomplete.")

    return {"soc_score": score, "soc_feedback": feedback}

if __name__ == "__main__":
    print(json.dumps(
        evaluate_soc(sys.argv[1], sys.argv[2]),
        indent=4
    ))
