# 🧠 **Cyber‑ML Training Platform — Developer Onboarding Guide**  
### *How to Build New Scenarios, Use AI Assistance, and Maintain Platform Quality*

---

# 1. Overview

Welcome to the Cyber‑ML Training Platform engineering team.  
This guide explains:

- How scenarios are structured  
- How to create new scenarios  
- How to use AI (Groq or any LLM) to assist in scenario generation  
- How to maintain consistency across all training content  
- How to produce both the main notebook and the help notebook  
- How to integrate logs, grading, and ML scaffolding  

This document assumes no prior context — it is a complete onboarding package.

---

# 2. Scenario Architecture

Each scenario lives in:

```
scenarios/
   scenario_XX/
      notebook.ipynb
      help.ipynb
      logs/
         auth.csv
         process.csv
         network.csv
         ...
      student_output/   (created at runtime)
      metadata.json
```

### **Every scenario must include:**

| Component | Purpose |
|----------|---------|
| `notebook.ipynb` | Main student-facing investigation notebook |
| `help.ipynb` | Optional incremental hint notebook |
| `logs/` | Synthetic or real-world-inspired event data |
| `metadata.json` | Scenario metadata (difficulty, tags, description) |
| `student_output/` | Auto-created folder for grading outputs |

### **Notebook Requirements**

All notebooks must:

- Load logs from GitHub using the `repo_root` pattern  
- Use Markdown for conceptual guidance  
- Use moderate scaffolding in code cells  
- Avoid push‑play behavior  
- Require students to produce:
  - `ioc_list`
  - `mitre_mapping`
  - `triage_summary`
  - `anomaly_score`
- Save outputs to:
  - `student_output/soc_output.json`
  - `student_output/ml_output.json`

### **Help Notebook Requirements**

`help.ipynb` must:

- Provide incremental hints  
- Include conceptual hints → concrete hints → optional reveal  
- Never provide full solutions  
- Mirror the structure of the main notebook  

---

# 3. Scenario Creation Workflow

This is the official workflow for creating a new scenario.

---

## **Step 1 — Choose a Scenario Type**

There are three supported scenario types (see Section 5):

1. **SOC Investigation Scenario**  
2. **ML‑Focused Scenario**  
3. **Hybrid Scenario (SOC + ML)**  

Pick one based on training goals.

---

## **Step 2 — Generate Logs**

Logs must be:

- Realistic  
- Internally consistent  
- Timestamped  
- Cross‑referenced across sources  

Minimum required logs:

- `auth.csv`
- `process.csv`
- `network.csv`

Optional logs:

- `cloud_iam.csv`
- `dns.csv`
- `proxy.csv`
- `endpoint.csv`

---

## **Step 3 — Write Scenario Metadata**

`metadata.json` example:

```json
{
  "id": "scenario_04",
  "title": "Suspicious Cloud IAM Activity",
  "difficulty": "Intermediate",
  "tags": ["cloud", "iam", "ml", "soc"],
  "description": "Investigate unusual IAM role escalations and API calls."
}
```

---

## **Step 4 — Build the Main Notebook**

Follow the **Scenario 02 baseline**:

- Markdown explains concepts  
- Code cells contain TODOs + commented examples  
- No auto‑solutions  
- Logs loaded via:

```python
repo_root = "https://raw.githubusercontent.com/<org>/<repo>/main"
scenario_path = "scenarios/scenario_XX"
log_base = f"{repo_root}/{scenario_path}/logs/"
```

- ML section must:
  - Provide model options  
  - Provide feature engineering hints  
  - Require student justification  

---

## **Step 5 — Build the Help Notebook**

Structure:

```
1. Understanding the logs
2. Timestamp normalization
3. Initial SOC sweep
4. IOC extraction
5. MITRE mapping
6. Feature engineering
7. Model selection
8. Model training
9. Scoring suspicious events
10. Triage summary
```

Each section includes:

- First hint (conceptual)  
- Second hint (concrete)  
- Optional reveal cell  

---

## **Step 6 — Test the Scenario**

Checklist:

- [ ] All logs load correctly  
- [ ] All timestamps parse  
- [ ] No code cell auto‑solves the scenario  
- [ ] Student must write meaningful content  
- [ ] Output JSON files are created  
- [ ] Help notebook does not leak answers  

---

## **Step 7 — Commit and Document**

Add to:

- README scenario list  
- `/docs/scenario_XX_guide.md` (optional)  

---

# 4. Using AI to Generate New Scenarios

Your teammate can use **any AI model** (Groq, OpenAI, Anthropic, etc.) to generate scenarios, as long as they follow the prompt template below.

---

## **Scenario Generation Prompt Template**

This is the official prompt for generating new scenarios:

```
You are generating a cybersecurity training scenario for the Cyber‑ML Training Platform.

Requirements:
- Produce a realistic multi‑log incident narrative.
- Include auth, process, and network events.
- Include a clear attack chain.
- Include at least one ML‑detectable anomaly.
- Include IOCs, MITRE techniques, and investigative clues.
- Make logs internally consistent.
- Provide a short scenario description.
- Provide a list of log types required.
- Provide a list of features students should consider for ML.
- Provide a list of suspicious events students should discover.

Do NOT generate code.
Do NOT generate notebook content.
Only generate scenario narrative + log schema.
```

This ensures:

- Logs are consistent  
- Attack chain is coherent  
- ML section has meaningful signals  

---

## **Help Notebook Prompt Template**

```
Generate incremental hints for a cybersecurity training scenario.

For each step:
- Provide a conceptual hint
- Provide a more concrete hint
- Provide an optional reveal cell (text only, no code)

Steps:
1. Understanding the logs
2. Timestamp normalization
3. Initial SOC sweep
4. IOC extraction
5. MITRE mapping
6. Feature engineering
7. Model selection
8. Model training
9. Scoring suspicious events
10. Triage summary
```

---

# 5. Scenario Types (with TODO Lists)

Here are the three official scenario types.

---

## **Type 1 — SOC Investigation Scenario**  
### *Focus: Log analysis, IOCs, MITRE mapping*

### TODO List
- [ ] Create auth/process/network logs  
- [ ] Include at least one clear attack chain  
- [ ] Include 3–5 suspicious events  
- [ ] Include 3–10 IOCs  
- [ ] Include 2–4 MITRE techniques  
- [ ] Build notebook with SOC‑only tasks  
- [ ] Build help notebook  

---

## **Type 2 — ML‑Focused Scenario**  
### *Focus: Feature engineering + anomaly detection*

### TODO List
- [ ] Create logs with subtle anomalies  
- [ ] Include numeric features suitable for ML  
- [ ] Include at least one anomaly cluster  
- [ ] Provide multiple model options  
- [ ] Require student justification  
- [ ] Build notebook with ML‑heavy tasks  
- [ ] Build help notebook  

---

## **Type 3 — Hybrid Scenario (SOC + ML)**  
### *Baseline: Scenario 02*

### TODO List
- [ ] Create multi‑source logs  
- [ ] Include both SOC clues and ML‑detectable anomalies  
- [ ] Require IOCs + MITRE + ML scoring  
- [ ] Provide model options  
- [ ] Provide feature engineering hints  
- [ ] Build notebook with both SOC + ML tasks  
- [ ] Build help notebook  

---

# 6. Quality Standards

All scenarios must:

- Use Markdown for conceptual guidance  
- Use moderate scaffolding in code cells  
- Avoid push‑play behavior  
- Require student reasoning  
- Include a help notebook  
- Produce structured JSON outputs  
- Load logs from GitHub  
- Use the `repo_root` pattern  
- Follow Scenario 02’s structure  

---

# 7. Final Notes for the Developer

- You are not expected to write logs manually — use AI to generate them.  
- You are not expected to write notebooks manually — use Scenario 02 as a template.  
- You are not expected to write hints manually — use the help prompt template.  
- You *are* expected to ensure:
  - Logs are consistent  
  - Notebooks do not leak answers  
  - ML tasks are solvable  
  - Output JSON files are correct  

---
