import pandas as pd
import google.generativeai as genai
import csv
import time

# choosing model
genai.configure(api_key="gemini-api-key")  
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# loading data
df = pd.read_csv(r"C:\Users\ESHWAR\OneDrive\Desktop\Programs\python\cynaptics hackathon\cases.csv") 
df['id'] = df['id'].astype(str)  # convert 'id' to string 

# judge simulation
def ask_judge(case_text):
    prompt = f"""
You are a judge in a virtual courtroom. Based on the following case description, determine the final verdict.
Respond in this exact format:
VERDICT: GRANTED or VERDICT: DENIED
Case:
\"\"\"
{case_text}
\"\"\"
"""
    try:
        response = model.generate_content(prompt)
        reply = response.text.strip().upper()
        if "GRANTED" in reply:
            return 1
        elif "DENIED" in reply:
            return 0
        else:
            return -1  
    except Exception as e:
        print(f"Error: {e}")
        return -1

# get verdict for cases in a particular range
def process_cases_in_range(start_row, end_row):
    predictions = []
    
    # cases in the range
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

        verdict = ask_judge(case_text)
        predictions.append((case_id, verdict))
        time.sleep(1)  # avoid rate limits
    
    # update the submissions in a csv file
    with open(r"C:\Users\ESHWAR\OneDrive\Desktop\Programs\python\cynaptics hackathon\submissions.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0: 
            writer.writerow(["id", "label"])
        writer.writerows(predictions)

    print("✅ Done! Check the updated submission.csv")

# ==== STEP 5: USER INPUT FOR ROW RANGE ====
start_row = int(input("Enter the starting row number: "))
end_row = int(input("Enter the ending row number: "))

# Process the range of cases
process_cases_in_range(start_row, end_row)
