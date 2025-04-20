# ⚖️ CYNAPTICS INDUCTION - AGENTS OF JUSTICE

Welcome to my submission for the **Cynaptics Hackathon**!  
This project simulates a courtroom environment using LLM agents, and also explores how AI can predict legal verdicts using case data.

---

## 🔧 Initial Problem Statement

The task was to **simulate a courtroom environment** using AI agents that represent real courtroom roles such as:
- Judge 👨‍⚖️
- Plaintiff 👤
- Defendant 🙋
- Prosecutor ⚔️
- Defense Lawyer 🛡️
- Witness 🧍

The goal was to build a believable, multi-agent legal proceeding using LLMs to mimic real-world behavior and reasoning in trials.

---

## 🤖 Agents of Justice — Courtroom Simulation

The courtroom simulation follows a structured, realistic flow:
1. 👨‍⚖️ **Judge** introduces the case.
2. ⚔️ **Prosecution** makes an opening statement.
3. 🛡️ **Defense Lawyer** responds.
4. 🧍 **Witness** is interrogated and cross-examined.
5. 🧑‍⚖️ **Closing statements** from both sides.
6. 👨‍⚖️ **Judge** delivers a final verdict.

Each agent uses role-specific prompts and interacts with the case data independently.

---

## 🧪 Kaggle Attempt 1 – Basic Verdict Prediction

Once the courtroom logic was working, I explored **verdict prediction** as a separate experiment on Kaggle.

- I initially ignored the 5-agent requirement to get a baseline working model.
- Tested multiple APIs:
  - ❌ `langchain-openai`: Frequent rate limits (`429` errors).
  - ⚠️ `HuggingFace`: Limited to inputs <8192 tokens, but real cases were >25k characters.
  - ✅ **Google Gemini API**: Successfully handled long cases using `gemini-1.5-flash` and `gemini-2.0-flash`.

### Strategy:
- Single-agent simulation (Judge only).
- Batched input cases in groups of 3–4 to avoid rate limits.
- Verdict generated based on single-agent judgment.

---

## 🧪 Kaggle Attempt 2 – Multi-Agent Verdict Voting

To meet the original requirement of **5 agents**, I evolved the architecture:

### Improvements:
- Added agents:
  - 👨‍⚖️ Judge
  - 👤 Plaintiff
  - ⚔️ Prosecutor
  - 🙋 Defendant
  - 🛡️ Defense Lawyer

### Method:
- Each agent individually reviews the case.
- Final verdict is determined by **majority voting**.

### Limitations:
- Not a dynamic simulation; agents do not interact with each other.
- No memory or conversational history used.
- Future improvement would involve building a **turn-based system with message passing** between agents.

---

## 🧠 Technologies Used

- [Google Generative AI (Gemini)](https://ai.google.dev/)
- Python 🐍
- Pandas 🐼
- CSV, Prompt Engineering

---

## 🚀 How to Run

### 1. Clone this repo
```bash
git clone https://github.com/your-username/agents-of-justice.git
cd agents-of-justice
```
### 2. Setup environment
```bash
pip install -r requirements.txt
```
### 3. Generate Gemini API Key
Go to: https://makersuite.google.com/app/apikey

## 🗂️ Data Usage

### 📌 For Initial Problem Statement (Courtroom Simulation)
- The `cases.csv` file should be placed in the **same directory** as the Python script.
### 📊 For Kaggle Attempts (Verdict Prediction)
- Import the same `cases.csv` file, placed in the working directory.
- Manually **create a blank `submissions.csv` file** in the same directory before running the script:
