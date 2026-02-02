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

    iocs = soc.get("ioc_list", [])
    triage = soc.get("triage_summary", "")
    ml_explanation = ml.get("explanation", "")
    anomaly_score = ml.get("anomaly_score", 0)

    # Alignment: SOC IOCs + ML anomaly
    if key["attacker_ip"] in iocs and anomaly_score < -0.1:
        score += 40
    else:
        feedback.append("SOC findings and ML anomaly detection do not clearly align.")

    # Full-chain triage summary
    if all(x in triage for x in [key["compromised_user"], key["sensitive_bucket"], key["attacker_bucket"]]):
        score += 30
    else:
        feedback.append("Triage summary does not clearly describe the full attack chain.")

    # Combined reasoning quality
    if len(triage.strip()) > 60 and len(ml_explanation.strip()) > 60:
        score += 30
    else:
        feedback.append("Combined SOC + ML reasoning lacks depth or completeness.")

    return {"combined_score": score, "combined_feedback": feedback}


if __name__ == "__main__":
    print(json.dumps(
        evaluate_combined(sys.argv[1], sys.argv[2], sys.argv[3]),
        indent=4
    ))
