from dotenv import load_dotenv
from google import genai
from toodlo_ai.AI.Instruction.todo_creation_instruction import TODO_CREATION_INSTRUCTION
from ..Schemas.schema import TODO,AI_Response_Model
import os
load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
