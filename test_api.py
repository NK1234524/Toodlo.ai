from dotenv import load_dotenv
from google import genai
from toodlo_ai.main import TODO
import os
load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
print("Gemini client created successfully")

response = client.models.generate_content(
    model = "gemini-3.6-flash",
    contents = "I need to prepare my DBMS presentation by Friday. It is very important.",
    config = {
        "response_mime_type":"application/json",
        "response_schema":TODO
    }
)

print(response.text)
