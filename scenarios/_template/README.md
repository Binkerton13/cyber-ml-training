# Scenario Template — Create Your Own SOC + ML Training Scenario

This folder provides a complete template for building new training scenarios.

## How to Use This Template

1. Copy this folder and rename it:

    scenarios/scenario_XX/

2. Update:
- `README.md` with your scenario narrative
- `generator/generate_data.py` to produce randomized logs + answer key
- `notebook_template.ipynb` with your guided or challenge flow
- `evaluation/*.py` with scenario-specific scoring logic

3. Run the generator to produce:
- `logs/*.csv` (student-facing data)
- `evaluation/answer_key.json` (hidden truth for grading)

4. Push your scenario to GitHub.  
The CI workflows will automatically detect and evaluate student submissions.

---

## Required Components

### 1. Narrative
Explain:
- What happened?
- What logs are provided?
- What is the student expected to do?

### 2. Data
Provide:
- Realistic logs
- Randomized anomalies
- A hidden answer key

### 3. Notebook
Must include:
- SOC analysis section
- ML analysis section
- Output generation section

### 4. Evaluation Scripts
Must:
- Load student outputs
- Load answer key
- Score SOC, ML, and combined reasoning

---

## Deliverables Students Must Produce

- `soc_output.json`
- `ml_output.json`
- `report.md`

These are automatically graded by GitHub Actions.

---

## Notes for Scenario Authors

- Keep logs small but realistic.
- Use the generator to produce randomized-but-gradable data.
- Ensure evaluation scripts reference `answer_key.json`.
- Avoid hardcoding values in the notebook — use variables.
- Test your scenario by running the notebook end-to-end.

Happy building!
