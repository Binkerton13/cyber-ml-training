import json
import sys

def evaluate_ml(path):
    with open(path, "r") as f:
        data = json.load(f)

    score = 0
    feedback = []

    # Anomaly score check
    anomaly = data.get("anomaly_score", 0)

    # IsolationForest anomaly threshold
    if anomaly < -0.1:  
        score += 50
    else:
        feedback.append("Model did not classify the login as anomalous.")

    # Model used check
    if data.get("model_used") == "IsolationForest":
        score += 25
    else:
        feedback.append("Unexpected model type.")

    # Explanation check
    if len(data.get("explanation", "")) > 10:
        score += 25
    else:
        feedback.append("Explanation too short.")

    return {
        "ml_score": score,
        "ml_feedback": feedback
    }

if __name__ == "__main__":
    result = evaluate_ml(sys.argv[1])
    print(json.dumps(result, indent=4))
