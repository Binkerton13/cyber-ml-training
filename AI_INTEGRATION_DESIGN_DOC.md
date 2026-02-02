# 🧠 **AI Integration Design Document (Groq‑Only)**  
### *Cyber‑ML Training Platform — Unified AI Helper Module*

---

## 🎯 Purpose

This document defines the architecture for integrating **Groq‑powered AI feedback** into the Cyber‑ML Training Platform. The goal is to:

- Evaluate student model choices  
- Score their justifications  
- Provide structured feedback  
- Keep notebooks secure (no API keys)  
- Maintain a clean, pluggable architecture for future model providers  

---

# 🏗️ Architecture Overview

```
/ai/
   ai_provider.py        ← Unified interface
   ai_groq.py            ← Groq implementation
   ai_stub.py            ← Placeholder for future providers
/backend/
   endpoints/
       evaluate_model_choice.py
```

The notebooks **never** call Groq directly.  
They only write JSON outputs.

The backend reads those outputs and calls the AI provider.

---

# ⚙️ AI Provider Modes

```
AI_MODE = groq | stub
```

### **groq**
Use Groq’s cloud API (primary, default)

### **stub**
Return placeholder responses (offline mode)

---

# 🔑 Groq Setup (for the developer)

1. Create a Groq account  
   https://console.groq.com

2. Generate an API key

3. Add to environment:

```
export GROQ_API_KEY="your_key_here"
export AI_MODE="groq"
```

4. Install SDK:

```
pip install groq
```

---

# 🧩 Responsibilities of the AI Helper

### ✔ Evaluate student model choice  
Input:

```json
{
  "model": "IsolationForest",
  "justification": "I chose this because..."
}
```

Output:

```json
{
  "score": 0.82,
  "feedback": "Good reasoning. IsolationForest is appropriate because..."
}
```

### ✔ JSON‑only responses  
No free‑form text.

### ✔ Graceful fallback  
If AI is offline:

```json
{
  "score": null,
  "feedback": "AI helper unavailable."
}
```

---

# 🔌 Unified Provider Interface

`ai_provider.py` exposes:

```python
def ask_ai(prompt: str) -> dict:
    ...
```

This is the only function the backend calls.

---

# 🧱 Provider Implementations

## **Groq Provider**  
`ai_groq.py`

- Uses `llama-3.3-70b-versatile` by default  
- Returns structured JSON  
- Handles API errors gracefully  

## **Stub Provider**  
`ai_stub.py`

Used when:

- AI_MODE=stub  
- Groq is unavailable  
- Running offline  

Returns:

```json
{"score": None, "feedback": "AI disabled."}
```

---

# 🔄 Future‑Proofing

To add a new provider:

1. Create `ai_newprovider.py`
2. Implement:

```python
def ask_newprovider(prompt: str) -> dict:
    ...
```

3. Add routing in `ai_provider.py`

No other changes required.

---

# 🧪 Prompt Template

Backend sends:

```
You are evaluating a student's choice of anomaly detection model.
Score their justification from 0.0 to 1.0 based on correctness, clarity, and reasoning.

Return ONLY valid JSON:
{
  "score": <float>,
  "feedback": "<short explanation>"
}
```

---

# 📡 Backend Endpoint

`POST /evaluate-model-choice`

Input:

```json
{
  "model": "IsolationForest",
  "justification": "I chose this because..."
}
```

Output:

```json
{
  "score": 0.82,
  "feedback": "Good reasoning..."
}
```

---

# 📝 TODO List for the AI Engineer

### **Phase 1 — Environment Setup**
- [ ] Create Groq account  
- [ ] Generate API key  
- [ ] Add `GROQ_API_KEY` to environment  
- [ ] Install Groq SDK  
- [ ] Verify connectivity  

### **Phase 2 — Implement Providers**
- [ ] Implement `ai_groq.py`  
- [ ] Implement `ai_stub.py`  
- [ ] Implement routing in `ai_provider.py`  

### **Phase 3 — Backend Integration**
- [ ] Create `/evaluate-model-choice` endpoint  
- [ ] Add prompt template  
- [ ] Parse JSON safely  
- [ ] Add error handling  

### **Phase 4 — Connect to Scenario Outputs**
- [ ] Read `ml_output.json`  
- [ ] Send model + justification to AI  
- [ ] Write AI feedback back into JSON  

### **Phase 5 — Documentation**
- [ ] Update README  
- [ ] Add provider instructions  
- [ ] Add troubleshooting guide  

---

# 📁 **Template Files**

Below are the exact contents you can drop into the repo.

---

## 📄 `ai/ai_provider.py`

```python
import os
from .ai_groq import ask_groq
from .ai_stub import ask_stub

AI_MODE = os.getenv("AI_MODE", "groq").lower()

def ask_ai(prompt: str) -> dict:
    """
    Unified AI provider interface.
    Returns a dict with keys: score, feedback.
    """
    if AI_MODE == "groq":
        return ask_groq(prompt)
    else:
        return ask_stub(prompt)
```

---

## 📄 `ai/ai_groq.py`

```python
import os
import json
from groq import Groq

def ask_groq(prompt: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"score": None, "feedback": "Missing GROQ_API_KEY."}

    client = Groq(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        content = response.choices[0].message["content"]
        return json.loads(content)

    except Exception as e:
        return {"score": None, "feedback": f"Groq error: {e}"}
```

---

## 📄 `ai/ai_stub.py`

```python
def ask_stub(prompt: str) -> dict:
    return {
        "score": None,
        "feedback": "AI helper disabled (stub mode)."
    }
```

---

## 📄 `backend/endpoints/evaluate_model_choice.py`

```python
from fastapi import APIRouter
from ai.ai_provider import ask_ai

router = APIRouter()

@router.post("/evaluate-model-choice")
def evaluate_model_choice(payload: dict):
    model = payload.get("model")
    justification = payload.get("justification")

    prompt = f"""
    You are evaluating a student's choice of anomaly detection model.
    Model chosen: {model}
    Justification: {justification}

    Score their justification from 0.0 to 1.0 based on correctness, clarity, and reasoning.

    Return ONLY valid JSON:
    {{
      "score": <float>,
      "feedback": "<short explanation>"
    }}
    """

    return ask_ai(prompt)
```

---
