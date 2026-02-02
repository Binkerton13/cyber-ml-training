import os
import json
import random
from datetime import datetime, timedelta

import pandas as pd
import numpy as np

# -----------------------------
# Path-safe directory handling
# -----------------------------
GEN_DIR = os.path.dirname(os.path.abspath(__file__))          # /scenario_03/generator
BASE_DIR = os.path.abspath(os.path.join(GEN_DIR, ".."))       # /scenario_03

LOG_DIR = os.path.join(BASE_DIR, "logs")
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")

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
            "event_name": "ConsoleLogin",
            "source_ip": random_internal_ip(),
            "region": random.choice(REGIONS_NORMAL),
            "result": "Success"
        })

    # Suspicious login
    rows.append({
        "timestamp": (base_time + timedelta(minutes=45)).isoformat() + "Z",
        "user": comp_user,
        "event_name": "ConsoleLogin",
        "source_ip": attacker_ip,
        "region": attacker_region,
        "result": "Success"
    })

    # Privilege escalation
    rows.append({
        "timestamp": (base_time + timedelta(minutes=47)).isoformat() + "Z",
        "user": comp_user,
        "event_name": "CreateAccessKey",
        "source_ip": attacker_ip,
        "region": attacker_region,
        "result": "Success"
    })
    rows.append({
        "timestamp": (base_time + timedelta(minutes=49)).isoformat() + "Z",
        "user": comp_user,
        "event_name": "AttachRolePolicy",
        "source_ip": attacker_ip,
        "region": attacker_region,
        "result": "Success"
    })
    rows.append({
        "timestamp": (base_time + timedelta(minutes=51)).isoformat() + "Z",
        "user": comp_user,
        "event_name": "AssumeRole",
        "source_ip": attacker_ip,
        "region": attacker_region,
        "result": "Success"
    })

    return pd.DataFrame(rows)


# -----------------------------
# CloudTrail API log generation
# -----------------------------
def generate_api_logs(comp_user, attacker_ip, attacker_region, base_time):
    rows = []

    # Normal API calls
    for i in range(60):
        rows.append({
            "timestamp": (base_time + timedelta(minutes=i)).isoformat() + "Z",
            "user": random.choice(USERS),
            "event_name": random.choice(["DescribeInstances", "ListBuckets", "GetParameter"]),
            "resource": random.choice(BUCKETS_NORMAL),
            "region": random.choice(REGIONS_NORMAL),
            "latency_ms": random.randint(20, 200),
            "status": "200"
        })

    # Discovery phase
    rows.append({
        "timestamp": (base_time + timedelta(minutes=55)).isoformat() + "Z",
        "user": comp_user,
        "event_name": "ListBuckets",
        "resource": "*",
        "region": attacker_region,
        "latency_ms": random.randint(30, 150),
        "status": "200"
    })
    rows.append({
        "timestamp": (base_time + timedelta(minutes=56)).isoformat() + "Z",
        "user": comp_user,
        "event_name": "ListObjects",
        "resource": BUCKET_SENSITIVE,
        "region": attacker_region,
        "latency_ms": random.randint(30, 150),
        "status": "200"
    })

    # Collection phase
    for i, obj in enumerate(SENSITIVE_OBJECTS):
        rows.append({
            "timestamp": (base_time + timedelta(minutes=57, seconds=30 * i)).isoformat() + "Z",
            "user": comp_user,
            "event_name": "GetObject",
            "resource": f"{BUCKET_SENSITIVE}/{obj}",
            "region": attacker_region,
            "latency_ms": random.randint(40, 250),
            "status": "200"
        })

    # Exfiltration
    rows.append({
        "timestamp": (base_time + timedelta(minutes=60)).isoformat() + "Z",
        "user": comp_user,
        "event_name": "PutObject",
        "resource": BUCKET_ATTACKER,
        "region": attacker_region,
        "latency_ms": random.randint(50, 300),
        "status": "200"
    })

    return pd.DataFrame(rows)


# -----------------------------
# S3 access logs (optional for SOC)
# -----------------------------
def generate_storage_logs(comp_user, attacker_ip, base_time):
    rows = []

    # Normal access
    for i in range(50):
        rows.append({
            "timestamp": (base_time + timedelta(minutes=i)).isoformat() + "Z",
            "user": random.choice(USERS),
            "bucket": random.choice(BUCKETS_NORMAL),
            "object": f"logs/app_{random.randint(1, 100)}.log",
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

    # Exfiltration
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


# -----------------------------
# ML Feature Dataset Generation
# -----------------------------
def generate_api_feature_table(api_df):
    """
    Produces ML‑friendly behavioral features for Scenario 03C.
    """
    df = api_df.copy()

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"].str.replace("Z", ""), utc=True)
    df["hour"] = df["timestamp"].dt.hour

    # Group by user for behavioral aggregation
    grouped = df.groupby("user")

    feature_table = pd.DataFrame({
        "user": grouped.size().index,
        "api_count_total": grouped.size().values,
        "unique_api_calls": grouped["event_name"].nunique().values,
        "unique_resources": grouped["resource"].nunique().values,
        "avg_latency": grouped["latency_ms"].mean().values,
        "error_rate": (grouped["status"].apply(lambda x: (x != "200").mean())).values,
        "region_entropy": grouped["region"].apply(lambda x: x.value_counts(normalize=True).mul(np.log2(x.value_counts(normalize=True))).sum() * -1).values,
        "hour_mean": grouped["hour"].mean().values,
        "hour_std": grouped["hour"].std().fillna(0).values
    })

    return feature_table


# -----------------------------
# Main
# -----------------------------
def main():
    base_time = datetime.now()
    compromised_user = random.choice(USERS)
    attacker_ip = random_external_ip()
    attacker_region = random.choice(REGIONS_SUSPICIOUS)

    iam_df = generate_iam_logs(compromised_user, attacker_ip, attacker_region, base_time)
    api_df = generate_api_logs(compromised_user, attacker_ip, attacker_region, base_time)
    storage_df = generate_storage_logs(compromised_user, attacker_ip, base_time)

    # ML feature dataset
    feature_df = generate_api_feature_table(api_df)

    # -----------------------------
    # Save logs with new naming
    # -----------------------------
    iam_path = os.path.join(LOG_DIR, "cloud_iam.csv")
    api_path = os.path.join(LOG_DIR, "cloud_api.csv")
    storage_path = os.path.join(LOG_DIR, "storage_access.csv")
    feature_path = os.path.join(LOG_DIR, "cloud_api_features.csv")

    iam_df.to_csv(iam_path, index=False)
    api_df.to_csv(api_path, index=False)
    storage_df.to_csv(storage_path, index=False)
    feature_df.to_csv(feature_path, index=False)

    # -----------------------------
    # Save answer key
    # -----------------------------
    answer_key = {
        "compromised_user": compromised_user,
        "attacker_ip": attacker_ip,
        "attacker_region": attacker_region,
        "sensitive_bucket": BUCKET_SENSITIVE,
        "attacker_bucket": BUCKET_ATTACKER,
        "sensitive_objects": SENSITIVE_OBJECTS,
        "expected_mitre": [
            "T1078",
            "T1098",
            "T1087",
            "T1530",
            "T1567"
        ]
    }

    with open(os.path.join(EVAL_DIR, "answer_key.json"), "w") as f:
        json.dump(answer_key, f, indent=4)

    print("Scenario 03 data generated successfully.")
    print(f"IAM logs: {iam_path}")
    print(f"API logs: {api_path}")
    print(f"Storage logs: {storage_path}")
    print(f"ML feature table: {feature_path}")


if __name__ == "__main__":
    main()
