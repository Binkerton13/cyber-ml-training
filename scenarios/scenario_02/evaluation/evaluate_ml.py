import json
import sys

def evaluate_ml(student_path, key_path):
    with open(student_path) as f:
        student = json.load(f)

    score = 0
    feedback = []

    if student.get("anomaly_score", 0) < -0.1:
        score += 50
    else:
        feedback.append("Model did not detect anomaly.")

    if student.get("model_used") == "IsolationForest":
        score += 25

    if len(student.get("explanation", "")) > 20:
        score += 25
    else:
        feedback.append("Explanation too short.")

    return {"ml_score": score, "ml_feedback": feedback}

if __name__ == "__main__":
    print(json.dumps(
        evaluate_ml(sys.argv[1], sys.argv[2]),
        indent=4
    ))
