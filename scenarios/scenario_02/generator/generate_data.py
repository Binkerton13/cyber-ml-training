import json
import random
import pandas as pd
from datetime import datetime, timedelta
import os

# -----------------------------
# Path-safe directory handling
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
EVAL_DIR = os.path.join(BASE_DIR, "..", "evaluation")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(EVAL_DIR, exist_ok=True)

# -----------------------------
# Scenario configuration
# -----------------------------
USERS = ["j.smith", "a.lee", "m.garcia", "t.jones"]
HOSTS = ["workstation-01", "workstation-02", "workstation-03", "fileserver-01"]

def generate_auth_logs(comp_user, attacker_ip):
    rows = []
    base = datetime.now()

    # Normal logins
    for i in range(50):
        rows.append({
            "timestamp": (base + timedelta(minutes=i)).isoformat() + "Z",
            "username": random.choice(USERS),
            "source_ip": "10.0.1." + str(random.randint(10, 50)),
            "destination_host": random.choice(HOSTS),
            "result": "success"
        })

    # Malicious login
    rows.append({
        "timestamp": (base + timedelta(minutes=55)).isoformat() + "Z",
        "username": comp_user,
        "source_ip": attacker_ip,
        "destination_host": "workstation-02",
        "result": "success"
    })

    return pd.DataFrame(rows)

def generate_process_logs(comp_user):
    rows = []
    base = datetime.now()

    # Normal processes
    for i in range(100):
        rows.append({
            "timestamp": (base + timedelta(seconds=i)).isoformat() + "Z",
            "host": random.choice(HOSTS),
            "username": random.choice(USERS),
            "process": random.choice(["chrome.exe", "explorer.exe", "outlook.exe"])
        })

    # Malicious process
    rows.append({
        "timestamp": (base + timedelta(seconds=200)).isoformat() + "Z",
        "host": "workstation-02",
        "username": comp_user,
        "process": "mimikatz.exe"
    })

    return pd.DataFrame(rows)

def generate_network_logs(attacker_ip):
    rows = []
    base = datetime.now()

    # Normal traffic
    for i in range(80):
        rows.append({
            "timestamp": (base + timedelta(seconds=i)).isoformat() + "Z",
            "src_ip": "10.0.1." + str(random.randint(10, 50)),
            "dst_ip": "10.0.2." + str(random.randint(10, 50)),
            "bytes_sent": random.randint(200, 2000)
        })

    # Exfil attempt
    rows.append({
        "timestamp": (base + timedelta(seconds=300)).isoformat() + "Z",
        "src_ip": attacker_ip,
        "dst_ip": "185.199.110." + str(random.randint(1, 254)),
        "bytes_sent": random.randint(50000, 200000)
    })

    return pd.DataFrame(rows)

def main():
    comp_user = random.choice(USERS)
    attacker_ip = "185.199.110." + str(random.randint(1, 254))

    auth = generate_auth_logs(comp_user, attacker_ip)
    proc = generate_process_logs(comp_user)
    net = generate_network_logs(attacker_ip)

    auth.to_csv(os.path.join(LOG_DIR, "auth.csv"), index=False)
    proc.to_csv(os.path.join(LOG_DIR, "process.csv"), index=False)
    net.to_csv(os.path.join(LOG_DIR, "network.csv"), index=False)

    answer_key = {
        "compromised_user": comp_user,
        "attacker_ip": attacker_ip,
        "malicious_process": "mimikatz.exe",
        "exfil_ip": "185.199.110.*",
        "expected_mitre": ["T1078", "T1003", "T1021", "T1041"]
    }

    with open(os.path.join(EVAL_DIR, "answer_key.json"), "w") as f:
        json.dump(answer_key, f, indent=4)

    print("Scenario 02 data generated successfully.")

if __name__ == "__main__":
    main()
