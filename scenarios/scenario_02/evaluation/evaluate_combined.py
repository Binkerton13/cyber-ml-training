import json
import sys

def evaluate_combined(soc_path, ml_path, key_path):
    with open(soc_path) as f:
        soc = json.load(f)

    with open(ml_path) as f:
        ml = json.load(f)

    with open(key_path) as f:
        key = json.load(f)

    score = 0
    feedback = []

    if key["attacker_ip"] in soc.get("ioc_list", []) and ml.get("anomaly_score", 0) < -0.1:
        score += 50
    else:
        feedback.append("SOC and ML findings do not align.")

    if len(soc.get("triage_summary", "")) > 20:
        score += 25

    if len(ml.get("explanation", "")) > 20:
        score += 25

    return {"combined_score": score, "combined_feedback": feedback}

if __name__ == "__main__":
    print(json.dumps(
        evaluate_combined(sys.argv[1], sys.argv[2], sys.argv[3]),
        indent=4
    ))
