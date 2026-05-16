import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.crew_setup import run_study_crew
import traceback
from dotenv import load_dotenv
load_dotenv()

print("Testing crew setup...")
try:
    res = run_study_crew("test task", task_type="explain", context="test context")
    print("Success! Output:")
    print(res)
except Exception as e:
    print("Error during crew setup or execution:")
    traceback.print_exc()
