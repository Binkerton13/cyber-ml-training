import json
import random
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

def generate_normal_logins(num=50):
    rows = []
    base_time = datetime.now(timezone.utc)

    for i in range(num):
        rows.append({
            "timestamp": (base_time + timedelta(minutes=i)).isoformat() + "Z",
            "username": "j.smith",
            "source_ip": "10.0.1.15",
            "destination_host": "workstation-22",
            "event_type": "login",
            "details": "success"
        })
    return rows

def generate_attack_event():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "username": "j.smith",
        "source_ip": "185.199.110." + str(random.randint(1, 254)),
        "destination_host": "server-" + str(random.randint(1, 20)),
        "event_type": "login",
        "details": "success"
    }

def main():
    os.makedirs("../logs", exist_ok=True)
    os.makedirs("../evaluation", exist_ok=True)

    normal = generate_normal_logins()
    attack = generate_attack_event()

    df = pd.DataFrame(normal + [attack])
    df.to_csv("../logs/generated_logs.csv", index=False)

    answer_key = {
        "malicious_ip": attack["source_ip"],
        "malicious_host": attack["destination_host"],
        "expected_mitre": ["T1078", "T1021"]
    }

    with open("../evaluation/answer_key.json", "w") as f:
        json.dump(answer_key, f, indent=4)

    print("Generated logs and answer key.")

if __name__ == "__main__":
    main()
