import pandas as pd
import google.generativeai as genai
import csv
import time

# model choice
genai.configure(api_key="gemini-api-key") 
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# load data
df = pd.read_csv(r"C:\Users\ESHWAR\OneDrive\Desktop\Programs\python\cynaptics hackathon\cases.csv")  
df['id'] = df['id'].astype(str)  # convert 'id' to string

# AGENTS

class Judge:
    def evaluate(self, case_text):
        prompt = f"""
You are a judge in a virtual courtroom. Based on the following case description, determine the final verdict.
Consider the merits of the case, fairness, and the law.

Respond in this exact format:
VERDICT: GRANTED or VERDICT: DENIED

Case:
\"\"\"
{case_text}
\"\"\"
"""
        return self.ask_model(prompt)

    def ask_model(self, prompt):
        try:
            response = model.generate_content(prompt)
            reply = response.text.strip().upper()
            if "GRANTED" in reply:
                return 1
            elif "DENIED" in reply:
                return 0
            else:
                return -1  # Unknown/invalid
        except Exception as e:
            print(f"Error: {e}")
            return -1

class Defendant:
    def evaluate(self, case_text):
        prompt = f"""
You are the defendant in a virtual courtroom. Based on the following case description, determine if the case is favorable to you.
Consider the allegations, the evidence against you, and your right to a fair trial.

Respond in this exact format:
VERDICT: GRANTED or VERDICT: DENIED

Case:
\"\"\"
{case_text}
\"\"\"
"""
        return self.ask_model(prompt)

    def ask_model(self, prompt):
        try:
            response = model.generate_content(prompt)
            reply = response.text.strip().upper()
            if "GRANTED" in reply:
                return 1
            elif "DENIED" in reply:
                return 0
            else:
                return -1  # Unknown/invalid
        except Exception as e:
            print(f"Error: {e}")
            return -1

class DefenseLawyer:
    def evaluate(self, case_text):
        prompt = f"""
You are the defense lawyer in a virtual courtroom. Based on the following case description, argue that the case should be granted.
Consider the defendant's rights, evidence, and any possible mitigating circumstances.

Respond in this exact format:
VERDICT: GRANTED or VERDICT: DENIED

Case:
\"\"\"
{case_text}
\"\"\"
"""
        return self.ask_model(prompt)

    def ask_model(self, prompt):
        try:
            response = model.generate_content(prompt)
            reply = response.text.strip().upper()
            if "GRANTED" in reply:
                return 1
            elif "DENIED" in reply:
                return 0
            else:
                return -1  # Unknown/invalid
        except Exception as e:
            print(f"Error: {e}")
            return -1

class Prosecutor:
    def evaluate(self, case_text):
        prompt = f"""
You are a prosecutor in a virtual courtroom. Based on the following case description, argue that the case should be denied.
Consider the gravity of the alleged offense and the evidence.

Respond in this exact format:
VERDICT: GRANTED or VERDICT: DENIED

Case:
\"\"\"
{case_text}
\"\"\"
"""
        return self.ask_model(prompt)

    def ask_model(self, prompt):
        try:
            response = model.generate_content(prompt)
            reply = response.text.strip().upper()
            if "DENIED" in reply:
                return 0
            elif "GRANTED" in reply:
                return 1
            else:
                return -1  # Unknown/invalid
        except Exception as e:
            print(f"Error: {e}")
            return -1

class Plaintiff:
    def evaluate(self, case_text):
        prompt = f"""
You are the plaintiff in a virtual courtroom. Based on the following case description, argue that the case should be granted.
Consider the strength of your claims, the law, and any evidence you have.

Respond in this exact format:
VERDICT: GRANTED or VERDICT: DENIED

Case:
\"\"\"
{case_text}
\"\"\"
"""
        return self.ask_model(prompt)

    def ask_model(self, prompt):
        try:
            response = model.generate_content(prompt)
            reply = response.text.strip().upper()
            if "GRANTED" in reply:
                return 1
            elif "DENIED" in reply:
                return 0
            else:
                return -1  # Unknown/invalid
        except Exception as e:
            print(f"Error: {e}")
            return -1

# Combine all agents into a decision-making process
def simulate_courtroom(case_text):
    judge = Judge()
    defendant = Defendant()
    defense_lawyer = DefenseLawyer()
    prosecutor = Prosecutor()
    plaintiff = Plaintiff()

    # Each agent evaluates the case
    verdicts = {
        'Judge': judge.evaluate(case_text),
        'Defendant': defendant.evaluate(case_text),
        'Defense Lawyer': defense_lawyer.evaluate(case_text),
        'Prosecutor': prosecutor.evaluate(case_text),
        'Plaintiff': plaintiff.evaluate(case_text)
    }

    # Simple majority decision
    total_granted = sum([verdict for verdict in verdicts.values()])
    if total_granted >= 2:  # More than half say GRANTED
        final_verdict = 1  # Majority says GRANTED
    elif total_granted < 2:  # Less than half say GRANTED
        final_verdict = 0  # Majority says DENIED
    else:
        final_verdict = -1  

    return final_verdict

# evaluate cases in range
def process_cases_in_range(start_row, end_row):
    predictions = []
    
    filtered_cases = df.iloc[start_row:end_row+1] 
    
    print(f"Processing cases from row {start_row} to {end_row}:")
    print(filtered_cases)  
        if filtered_cases.empty:
        print(f"No cases found in the range {start_row} to {end_row}.")
        return
    
    for i, row in filtered_cases.iterrows():
        case_id = row["id"]  # id is a string, so it won't be NaN
        case_text = row["text"]
        print(f"Processing case {case_id}...")

        verdict = simulate_courtroom(case_text)
        predictions.append((case_id, verdict))
        time.sleep(1)  # To avoid rate limits
    
    # Save the predictions to a CSV file
    with open(r"C:\Users\ESHWAR\OneDrive\Desktop\Programs\python\cynaptics hackathon\submissions2.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0: 
            writer.writerow(["id", "label"])
        writer.writerows(predictions)

    print("✅ Done! Check the updated submission.csv")

start_row = int(input("Enter the starting row number: "))
end_row = int(input("Enter the ending row number: "))

# Process the range of cases
process_cases_in_range(start_row, end_row)
