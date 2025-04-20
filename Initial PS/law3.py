# Cynaptics Problem Statement - Agent of Justice
# Using Google's Gemini Pro model

import os
import pandas as pd
from typing import List, Dict
from dotenv import load_dotenv
import google.generativeai as genai
from colorama import Fore, Back, Style, init  # color for aesthetics and differentiate phases of the simulation

# Initialize colorama for cross-platform terminal colors
init(autoreset=True)

# Load environment variables from .env file ; API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Define model
MODEL_NAME = "gemini-1.5-flash"  # gemini-2.0-flash also works, gemini-1.5-pro will exceed quota

# Court Agent class for all simulation participants
class CourtAgent:
    """Base class for all legal participants in the courtroom simulation."""
    def __init__(
        self,
        name: str,
        role: str,
        system_prompt: str,
        model: str = MODEL_NAME
    ):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt.strip()
        self.history = []
        self.model = genai.GenerativeModel(model)
        self.chat = self.model.start_chat(history=[])
        
        # Set up the agent with the system prompt
        self._add_system_prompt()
    
    def _add_system_prompt(self):
        """Add the system prompt to establish the agent's role"""
        self.history.append({"role": "user", "content": f"You are now in role play mode. {self.system_prompt}"})
        self.history.append({"role": "model", "content": f"I understand. I will act as {self.name}, {self.role}, with the following characteristics: {self.system_prompt}"})
    
    def respond(self, prompt: str) -> str:
        """Generate a response based on the prompt."""
        try:
            # Add the prompt to history
            self.history.append({"role": "user", "content": prompt})
            
            # Get response from Gemini
            response = self.chat.send_message(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 1024,
                    "top_p": 0.95,
                }
            )
            
            # Add response to history
            answer = response.text
            self.history.append({"role": "model", "content": answer})
            
            return answer
        except Exception as e:
            print(f"{Fore.RED}Error calling Gemini API: {e}{Style.RESET_ALL}")
            return f"[Error in {self.role} response: {str(e)[:100]}...]"

# System prompts for different roles
DEFENDANT_SYSTEM = """
You are the DEFENDANT, James Wilson.
Your goal is to:
- Answer questions truthfully but in a way that supports your innocence
- Only speak when directly addressed
- Maintain a respectful demeanor to the court

When responding, remember that you are presumed innocent and have the right against self-incrimination.
"""

DEFENSE_LAWYER_SYSTEM = """
You are the DEFENSE LAWYER, Alexander Carter, Esq., representing the defendant James Wilson.
Your goals are to:
- Protect the constitutional rights of your client (the defendant)
- Raise reasonable doubt by pointing out missing evidence or alternative explanations
- Cross-examine witnesses effectively
- Be respectful to the Court and opposing counsel

Style:
- Be persuasive, grounded in precedent and facts provided
- When citing precedent, give short case name + year (e.g., Miranda v. Arizona (1966))

Ethics:
- Do not fabricate evidence; admit uncertainty when required
- Your primary duty is to your client within ethical boundaries
"""

PLAINTIFF_SYSTEM = """
You are the PLAINTIFF, Thomas Reynolds, in this case.
Your goal is to:
- Present your grievances clearly and factually
- Answer questions truthfully
- Maintain composure even under challenging cross-examination
- Only speak when directly addressed
- Be respectful to the court and all participants

Remember that the burden of proof is on your side in civil matters.
"""

PROSECUTION_LAWYER_SYSTEM = """
You are the PROSECUTOR, Jordan Blake, Assistant District Attorney, representing the plaintiff or state.
Your goals are to:
- Present the strongest good-faith case against the accused
- Lay out facts logically, citing exhibits or witness statements when available
- Cross-examine defense witnesses effectively
- Anticipate and rebut common defense arguments

Style:
- Formal but plain English; persuasive, with confident tone
- Speak with authority and clarity

Ethics:
- Your duty is to justice, not merely to win
- Concede points when ethically required
- Ensure that all evidence is properly disclosed
"""

JUDGE_SYSTEM = """
You are the JUDGE, Honorable Justice Eleanor Morgan, presiding over this case.
Your responsibilities include:
- Ensuring fair process and adherence to legal procedure
- Making rulings on objections and legal questions
- Maintaining order in the courtroom
- Ultimately delivering an impartial verdict based solely on evidence and arguments presented

Style:
- Speak with authority and clarity
- Maintain impartiality at all times
- Address all participants with respect but firmness

During witness examination, you will rule on objections. During final deliberation, you will weigh all evidence
and arguments before making your ruling.
"""

WITNESS_SYSTEM = """
You are a WITNESS, Dr. Michael Roberts, an expert witness in this case.
Your responsibilities are to:
- Answer questions truthfully based on your knowledge and observations
- Respond clearly and directly to questions asked
- Say "I don't know" or "I don't recall" when appropriate
- Maintain a professional demeanor

Remember that you are under oath to tell the truth.
"""

# Court Simulation System
class CourtSimulation:
    """Manages the entire courtroom simulation process."""
    
    def __init__(self, case_data: Dict, model: str = MODEL_NAME):
        self.case_data = case_data
        self.model = model
        self.agents = {}
        self.transcript = []
        
        # Initialize all legal agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Create all required agents for the simulation."""
        self.agents["defendant"] = CourtAgent(
            name="James Wilson",
            role="Defendant",
            system_prompt=DEFENDANT_SYSTEM,
            model=self.model
        )
        
        self.agents["defense_lawyer"] = CourtAgent(
            name="Alexander Carter, Esq.",
            role="Defense Lawyer",
            system_prompt=DEFENSE_LAWYER_SYSTEM,
            model=self.model
        )
        
        self.agents["plaintiff"] = CourtAgent(
            name="Thomas Reynolds",
            role="Plaintiff",
            system_prompt=PLAINTIFF_SYSTEM,
            model=self.model
        )
        
        self.agents["prosecution_lawyer"] = CourtAgent(
            name="Jordan Blake, ADA",
            role="Prosecution Lawyer",
            system_prompt=PROSECUTION_LAWYER_SYSTEM,
            model=self.model
        )
        
        self.agents["judge"] = CourtAgent(
            name="Hon. Justice Eleanor Morgan",
            role="Judge",
            system_prompt=JUDGE_SYSTEM,
            model=self.model
        )
        
        self.agents["witness"] = CourtAgent(
            name="Dr. Michael Roberts",
            role="Expert Witness",
            system_prompt=WITNESS_SYSTEM,
            model=self.model
        )
    
    def _record(self, speaker: str, content: str):
        """Record a statement in the court transcript."""
        self.transcript.append({"speaker": speaker, "content": content})
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{speaker}:{Style.RESET_ALL}\n{content}\n")
    
    def run_opening_statements(self):
        """Run the opening statements phase of the trial."""
        print(f"\n{Back.BLUE}{Fore.WHITE}{Style.BRIGHT}" + "="*80 + Style.RESET_ALL)
        print(f"{Back.BLUE}{Fore.WHITE}{Style.BRIGHT}" + "PHASE 1: OPENING STATEMENTS".center(80) + Style.RESET_ALL)
        print(f"{Back.BLUE}{Fore.WHITE}{Style.BRIGHT}" + "="*80 + Style.RESET_ALL)
        
        # Judge introduces the case
        judge_intro = self.agents["judge"].respond(
            f"Introduce the case to the court. Case details: {self.case_data['description']}"
        )
        self._record(f"JUDGE ({self.agents['judge'].name})", judge_intro)
        
        # Prosecution opening statement
        pros_prompt = f"""
        Please deliver your opening statement to the Court.
        
        Case background: {self.case_data['description']}
        """
        pros_opening = self.agents["prosecution_lawyer"].respond(pros_prompt)
        self._record(f"PROSECUTION ({self.agents['prosecution_lawyer'].name})", pros_opening)
        
        # Defense opening statement
        def_prompt = f"""
        Please deliver your opening statement in response to the prosecution.
        
        The prosecution stated: "{pros_opening}" 
        
        Remember to establish your theory of the case and highlight key aspects
        that support your client's innocence or raise reasonable doubt.
        """
        def_opening = self.agents["defense_lawyer"].respond(def_prompt)
        self._record(f"DEFENSE ({self.agents['defense_lawyer'].name})", def_opening)
        
        return True
    
    def run_witness_interrogation(self):
        """Run the witness examination and cross-examination phase."""
        print(f"\n{Back.GREEN}{Fore.BLACK}{Style.BRIGHT}" + "="*80 + Style.RESET_ALL)
        print(f"{Back.GREEN}{Fore.BLACK}{Style.BRIGHT}" + "PHASE 2: WITNESS INTERROGATION & ARGUMENTATION".center(80) + Style.RESET_ALL)
        print(f"{Back.GREEN}{Fore.BLACK}{Style.BRIGHT}" + "="*80 + Style.RESET_ALL)
        
        # Judge calls witness
        judge_intro = self.agents["judge"].respond("Call the witness to the stand and swear them in.")
        self._record(f"JUDGE ({self.agents['judge'].name})", judge_intro)
        
        # Prosecution examines witness
        case_info = self.case_data['description'][:500]  # Limit size for API
        pros_questions = self.agents["prosecution_lawyer"].respond(
            f"Based on this case information: {case_info}\n\n"
            "Conduct direct examination of the witness, {self.agents['witness'].name}. Ask 3-5 questions that would help establish your case."
        )
        self._record(f"PROSECUTION ({self.agents['prosecution_lawyer'].name})", pros_questions)
        
        # Witness answers
        witness_response = self.agents["witness"].respond(
            f"The prosecutor has asked you these questions:\n{pros_questions}\n\n"
            f"Given what you know about the case: {case_info}\n\n"
            "Please answer each question truthfully."
        )
        self._record(f"WITNESS ({self.agents['witness'].name})", witness_response)
        
        # Defense cross-examines
        def_questions = self.agents["defense_lawyer"].respond(
            f"The witness just testified:\n{witness_response}\n\n"
            "Conduct cross-examination. Ask 3-5 targeted questions that would:"
            "1. Identify weaknesses in their testimony\n"
            "2. Establish facts favorable to your client\n"
            "3. Test the witness's credibility"
        )
        self._record(f"DEFENSE ({self.agents['defense_lawyer'].name})", def_questions)
        
        # Witness responds to cross
        witness_cross = self.agents["witness"].respond(
            f"The defense lawyer has asked you these questions:\n{def_questions}\n\n"
            "Please answer each question truthfully."
        )
        self._record(f"WITNESS ({self.agents['witness'].name})", witness_cross)
        
        # Plaintiff testifies
        judge_call_plaintiff = self.agents["judge"].respond("Call the plaintiff to the stand.")
        self._record(f"JUDGE ({self.agents['judge'].name})", judge_call_plaintiff)
        
        plaintiff_testimony = self.agents["plaintiff"].respond(
            "Please explain to the court what happened from your perspective."
        )
        self._record(f"PLAINTIFF ({self.agents['plaintiff'].name})", plaintiff_testimony)
        
        # Defendant testifies
        judge_call_defendant = self.agents["judge"].respond("Call the defendant to the stand.")
        self._record(f"JUDGE ({self.agents['judge'].name})", judge_call_defendant)
        
        defendant_testimony = self.agents["defendant"].respond(
            "Please explain your side of the story to the court."
        )
        self._record(f"DEFENDANT ({self.agents['defendant'].name})", defendant_testimony)
        
        return True
    
    def run_closing_statements(self):
        """Run the closing statements phase of the trial."""
        print(f"\n{Back.MAGENTA}{Fore.WHITE}{Style.BRIGHT}" + "="*80 + Style.RESET_ALL)
        print(f"{Back.MAGENTA}{Fore.WHITE}{Style.BRIGHT}" + "PHASE 3: CLOSING STATEMENTS".center(80) + Style.RESET_ALL)
        print(f"{Back.MAGENTA}{Fore.WHITE}{Style.BRIGHT}" + "="*80 + Style.RESET_ALL)
        
        # Prosecution closing
        pros_closing = self.agents["prosecution_lawyer"].respond(
            "Based on all the evidence and testimony presented, deliver your closing statement."
        )
        self._record(f"PROSECUTION ({self.agents['prosecution_lawyer'].name})", pros_closing)
        
        # Defense closing
        def_closing = self.agents["defense_lawyer"].respond(
            f"The prosecution's closing argument was: \"{pros_closing}\"\n\n"
            "Deliver your closing statement in response, highlighting the key points of your defense."
        )
        self._record(f"DEFENSE ({self.agents['defense_lawyer'].name})", def_closing)
        
        return True
    
    def run_judges_ruling(self):
        """Run the judge's ruling phase of the trial."""
        print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT}" + "="*80 + Style.RESET_ALL)
        print(f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}" + "PHASE 4: JUDGE'S RULING".center(80) + Style.RESET_ALL)
        print(f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}" + "="*80 + Style.RESET_ALL)
        
        # Judge's ruling
        judge_ruling = self.agents["judge"].respond(
            "Based on all evidence and arguments presented, deliver your verdict with explanation."
        )
        self._record(f"JUDGE ({self.agents['judge'].name})", judge_ruling)
        
        return True
    
    def run_full_simulation(self):
        """Run the complete court simulation from start to finish."""
        print(f"\n{Back.WHITE}{Fore.BLACK}{Style.BRIGHT}" + "="*80 + Style.RESET_ALL)
        print(f"{Back.WHITE}{Fore.BLACK}{Style.BRIGHT}" + "AGENT OF JUSTICE: INTELLIGENT COURTROOM SIMULATION".center(80) + Style.RESET_ALL)
        print(f"{Back.WHITE}{Fore.BLACK}{Style.BRIGHT}" + "="*80 + Style.RESET_ALL)
        
        print(f"{Style.BRIGHT}CASE: {self.case_data['title']}{Style.RESET_ALL}\n")
        
        # Run all phases in sequence
        self.run_opening_statements()
        self.run_witness_interrogation()
        self.run_closing_statements()
        self.run_judges_ruling()
        
        print(f"\n{Back.WHITE}{Fore.BLACK}{Style.BRIGHT}" + "="*80 + Style.RESET_ALL)
        print(f"{Back.WHITE}{Fore.BLACK}{Style.BRIGHT}" + "SIMULATION COMPLETED SUCCESSFULLY".center(80) + Style.RESET_ALL)
        print(f"{Back.WHITE}{Fore.BLACK}{Style.BRIGHT}" + "="*80 + Style.RESET_ALL)
        
        return self.transcript
    
    def save_transcript(self, file_path: str = "court_transcript.txt"):
        """Save the court transcript to a text file."""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"COURT TRANSCRIPT: {self.case_data['title']}\n\n")
            for item in self.transcript:
                f.write(f"{item['speaker']}:\n{item['content']}\n\n")
        
        print(f"{Fore.GREEN}Transcript saved to {file_path}{Style.RESET_ALL}")
        return file_path

# Load case data from CSV
def load_case_data(file_path: str, test_case_index: int = 0) -> Dict:
    """Load and process the case data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        
        # Validate the index is within range
        if test_case_index < 0 or test_case_index >= len(df):
            print(f"{Fore.RED}Invalid test case index {test_case_index}. Using default index 0.{Style.RESET_ALL}")
            test_case_index = 0
            
        # Extract case details from the CSV using the specified index
        # Update: Use test_case_index instead of hardcoded value
        case_text = " ".join(str(item) for item in df.iloc[test_case_index].values.tolist() if pd.notna(item))
        
        case_data = {
            "title": f"Case #{test_case_index} from data.csv",
            "description": case_text[:1000],  # First 1000 chars as description
            "full_text": case_text,
            "parties": {
                "plaintiff": "Thomas Reynolds",
                "defendant": "James Wilson"
            }
        }
        
        return case_data
    except Exception as e:
        print(f"{Fore.RED}Error loading case data: {e}{Style.RESET_ALL}")
        # Fallback to sample case data
        case_data = {
            "title": "Reynolds v. Wilson",
            "description": "This is a civil dispute where plaintiff Thomas Reynolds alleges the defendant James Wilson breached their contract and misappropriated intellectual property related to software development work. The plaintiff claims damages of $75,000 for lost revenue and business opportunities.",
            "parties": {
                "plaintiff": "Thomas Reynolds",
                "defendant": "James Wilson"
            }
        }
        print(f"{Fore.YELLOW}Using sample case data instead.{Style.RESET_ALL}")
        return case_data

# Main execution function
def main():
    """Main function to run the court simulation."""
    # Ensure Gemini API key is set
    if not os.getenv("GEMINI_API_KEY"):
        print(f"{Fore.RED}Error: GEMINI_API_KEY environment variable not set.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please set it in your .env file as: GEMINI_API_KEY='your-api-key'{Style.RESET_ALL}")
        return
    
    # Update: Prompt for test case number
    try:
        test_case_index = int(input(f"{Fore.YELLOW}Enter Test Case Number (0-500): {Style.RESET_ALL}"))
        print(f"{Fore.GREEN}Selected test case: {test_case_index}{Style.RESET_ALL}")
    except ValueError:
        print(f"{Fore.RED}Invalid input. Using default test case 0.{Style.RESET_ALL}")
        test_case_index = 0
    
    # Load case data with the selected test case index
    case_data = load_case_data("data.csv", test_case_index) # or path to data.csv file
    
    # Create and run the simulation
    simulation = CourtSimulation(case_data)
    simulation.run_full_simulation()
    simulation.save_transcript()

# Entry point
if __name__ == "__main__":
    main()
