import os
import json
import random
from datetime import datetime, timedelta

import pandas as pd

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
USERS = ["cloud_eng_1", "cloud_eng_2", "devops_1", "analyst_1"]
REGIONS_NORMAL = ["us-east-1", "us-west-2"]
REGIONS_SUSPICIOUS = ["ap-southeast-1", "eu-central-1"]
INTERNAL_IP_RANGE = "10.0.{}.{}"
EXTERNAL_IP_RANGE = "185.199.110.{}"

BUCKETS_NORMAL = ["logs-bucket", "backups-bucket", "public-assets"]
BUCKET_SENSITIVE = "sensitive-data"
BUCKET_ATTACKER = "external-exfil-bucket"

SENSITIVE_OBJECTS = [
    "hr/payroll_2024.xlsx",
    "finance/q4_results.pdf",
    "engineering/roadmap_2025.docx"
]


def random_internal_ip():
    return INTERNAL_IP_RANGE.format(random.randint(1, 5), random.randint(10, 250))


def random_external_ip():
    return EXTERNAL_IP_RANGE.format(random.randint(1, 254))


# -----------------------------
# IAM log generation
# -----------------------------
def generate_iam_logs(comp_user, attacker_ip, attacker_region, base_time):
    rows = []

    # Normal logins
    for i in range(40):
        rows.append({
            "timestamp": (base_time + timedelta(minutes=i)).isoformat() + "Z",
            "user": random.choice(USERS),
            "action": "ConsoleLogin",
            "source_ip": random_internal_ip(),
            "region": random.choice(REGIONS_NORMAL),
            "result": "Success"
        })

    # Suspicious login from unusual region
    rows.append({
        "timestamp": (base_time + timedelta(minutes=45)).isoformat() + "Z",
        "user": comp_user,
        "action": "ConsoleLogin",
        "source_ip": attacker_ip,
        "region": attacker_region,
        "result": "Success"
    })

    # Privilege escalation sequence
    rows.append({
        "timestamp": (base_time + timedelta(minutes=47)).isoformat() + "Z",
        "user": comp_user,
        "action": "CreateAccessKey",
        "source_ip": attacker_ip,
        "region": attacker_region,
        "result": "Success"
    })
    rows.append({
        "timestamp": (base_time + timedelta(minutes=49)).isoformat() + "Z",
        "user": comp_user,
        "action": "AttachRolePolicy",
        "source_ip": attacker_ip,
        "region": attacker_region,
        "result": "Success"
    })
    rows.append({
        "timestamp": (base_time + timedelta(minutes=51)).isoformat() + "Z",
        "user": comp_user,
        "action": "AssumeRole",
        "source_ip": attacker_ip,
        "region": attacker_region,
        "result": "Success"
    })

    return pd.DataFrame(rows)


# -----------------------------
# API call log generation
# -----------------------------
def generate_api_logs(comp_user, attacker_ip, attacker_region, base_time):
    rows = []

    # Normal API calls
    for i in range(60):
        rows.append({
            "timestamp": (base_time + timedelta(minutes=i)).isoformat() + "Z",
            "user": random.choice(USERS),
            "api_call": random.choice(["DescribeInstances", "ListBuckets", "GetParameter"]),
            "resource": random.choice(BUCKETS_NORMAL),
            "latency_ms": random.randint(20, 200),
            "status": "200"
        })

    # Discovery phase
    rows.append({
        "timestamp": (base_time + timedelta(minutes=55)).isoformat() + "Z",
        "user": comp_user,
        "api_call": "ListBuckets",
        "resource": "*",
        "latency_ms": random.randint(30, 150),
        "status": "200"
    })
    rows.append({
        "timestamp": (base_time + timedelta(minutes=56)).isoformat() + "Z",
        "user": comp_user,
        "api_call": "ListObjects",
        "resource": BUCKET_SENSITIVE,
        "latency_ms": random.randint(30, 150),
        "status": "200"
    })

    # Collection phase
    for i, obj in enumerate(SENSITIVE_OBJECTS):
        rows.append({
            "timestamp": (base_time + timedelta(minutes=57, seconds=30 * i)).isoformat() + "Z",
            "user": comp_user,
            "api_call": "GetObject",
            "resource": f"{BUCKET_SENSITIVE}/{obj}",
            "latency_ms": random.randint(40, 250),
            "status": "200"
        })

    # Exfiltration phase (modeled as PutObject to external bucket)
    rows.append({
        "timestamp": (base_time + timedelta(minutes=60)).isoformat() + "Z",
        "user": comp_user,
        "api_call": "PutObject",
        "resource": BUCKET_ATTACKER,
        "latency_ms": random.randint(50, 300),
        "status": "200"
    })

    return pd.DataFrame(rows)


# -----------------------------
# S3 access log generation
# -----------------------------
def generate_storage_logs(comp_user, attacker_ip, base_time):
    rows = []

    # Normal access
    for i in range(50):
        rows.append({
            "timestamp": (base_time + timedelta(minutes=i)).isoformat() + "Z",
            "user": random.choice(USERS),
            "bucket": random.choice(BUCKETS_NORMAL),
            "object": "logs/app_{}.log".format(random.randint(1, 100)),
            "bytes_read": random.randint(1000, 50000),
            "bytes_written": random.randint(0, 2000),
            "source_ip": random_internal_ip()
        })

    # Sensitive reads
    for i, obj in enumerate(SENSITIVE_OBJECTS):
        rows.append({
            "timestamp": (base_time + timedelta(minutes=57, seconds=30 * i)).isoformat() + "Z",
            "user": comp_user,
            "bucket": BUCKET_SENSITIVE,
            "object": obj,
            "bytes_read": random.randint(50000, 200000),
            "bytes_written": 0,
            "source_ip": attacker_ip
        })

    # Exfiltration write (modeled as large write to external bucket)
    rows.append({
        "timestamp": (base_time + timedelta(minutes=60)).isoformat() + "Z",
        "user": comp_user,
        "bucket": BUCKET_ATTACKER,
        "object": "exfiltrated_archive.zip",
        "bytes_read": 0,
        "bytes_written": random.randint(50000000, 200000000),
        "source_ip": attacker_ip
    })

    return pd.DataFrame(rows)


def main():
    base_time = datetime.now()
    compromised_user = random.choice(USERS)
    attacker_ip = random_external_ip()
    attacker_region = random.choice(REGIONS_SUSPICIOUS)

    iam_df = generate_iam_logs(compromised_user, attacker_ip, attacker_region, base_time)
    api_df = generate_api_logs(compromised_user, attacker_ip, attacker_region, base_time)
    storage_df = generate_storage_logs(compromised_user, attacker_ip, base_time)

    iam_path = os.path.join(LOG_DIR, "iam.csv")
    api_path = os.path.join(LOG_DIR, "api_calls.csv")
    storage_path = os.path.join(LOG_DIR, "storage_access.csv")

    iam_df.to_csv(iam_path, index=False)
    api_df.to_csv(api_path, index=False)
    storage_df.to_csv(storage_path, index=False)

    answer_key = {
        "compromised_user": compromised_user,
        "attacker_ip": attacker_ip,
        "attacker_region": attacker_region,
        "sensitive_bucket": BUCKET_SENSITIVE,
        "attacker_bucket": BUCKET_ATTACKER,
        "sensitive_objects": SENSITIVE_OBJECTS,
        "expected_mitre": [
            "T1078",  # Valid Accounts
            "T1098",  # Account Manipulation
            "T1087",  # Account Discovery
            "T1530",  # Data from Cloud Storage
            "T1567"   # Exfiltration to Cloud Storage
        ]
    }

    with open(os.path.join(EVAL_DIR, "answer_key.json"), "w") as f:
        json.dump(answer_key, f, indent=4)

    print("Scenario 03 data generated successfully.")
    print(f"IAM logs: {iam_path}")
    print(f"API logs: {api_path}")
    print(f"Storage logs: {storage_path}")


if __name__ == "__main__":
    main()
