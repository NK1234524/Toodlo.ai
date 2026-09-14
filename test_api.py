from dotenv import load_dotenv
from google import genai
from toodlo_ai.main import TODO,AI_Response_Model
from toodlo_ai.AI.Instruction.todo_creation_instruction import TODO_CREATION_INSTRUCTION
import os
load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
print("Gemini client created successfully")

response = client.models.generate_content(
    model = "gemini-3.6-flash",
    contents = "I want to prepare for the DBMS end sems exam by tommorow because my exam is on friday.",
    config = {
        "system_instruction":TODO_CREATION_INSTRUCTION,
        "response_mime_type":"application/json",
        "response_schema":AI_Response_Model
    }
)

print(response.text)
