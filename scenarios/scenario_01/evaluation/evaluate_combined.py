import json
import sys

def evaluate_combined(soc_path, ml_path):
    with open(soc_path, "r") as f:
        soc = json.load(f)

    with open(ml_path, "r") as f:
        ml = json.load(f)

    combined_score = 0
    feedback = []

    # Did SOC and ML agree?
    if "185.199.110.153" in soc.get("ioc_list", []) and ml.get("anomaly_score", 0) < -0.1:
        combined_score += 50
    else:
        feedback.append("SOC and ML findings do not align.")

    # Did student produce a triage summary?
    if len(soc.get("triage_summary", "")) > 20:
        combined_score += 25
    else:
        feedback.append("Triage summary too short.")

    # Did student explain ML results?
    if len(ml.get("explanation", "")) > 20:
        combined_score += 25
    else:
        feedback.append("ML explanation too short.")

    return {
        "combined_score": combined_score,
        "combined_feedback": feedback
    }

if __name__ == "__main__":
    result = evaluate_combined(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=4))
