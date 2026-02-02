import json
import sys


def evaluate_ml(student_path, key_path):
    with open(student_path) as f:
        student = json.load(f)

    score = 0
    feedback = []

    anomaly_score = student.get("anomaly_score", 0)
    model_used = student.get("model_used", "")
    features = student.get("features", [])
    explanation = student.get("explanation", "")

    # Anomaly detection
    if anomaly_score < -0.1:
        score += 40
    else:
        feedback.append("Model did not clearly flag anomalous behavior (anomaly_score too high).")

    # Model type
    if model_used:
        score += 10
    else:
        feedback.append("Model type not specified.")

    # Features
    if len(features) >= 3:
        score += 20
    else:
        feedback.append("Too few features used for modeling.")

    # Explanation
    if len(explanation.strip()) > 40:
        score += 30
    else:
        feedback.append("ML explanation too short or lacking depth.")

    return {"ml_score": score, "ml_feedback": feedback}


if __name__ == "__main__":
    print(json.dumps(
        evaluate_ml(sys.argv[1], sys.argv[2]),
        indent=4
    ))
