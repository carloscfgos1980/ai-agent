import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main(text_content):
    user_prompt = text_content

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )
    # print(response.text)
    prompt_token_count = response.usage_metadata.prompt_token_count
    candidates_token_count = response.usage_metadata.candidates_token_count
    if sys.argv and len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")


if sys.argv and len(sys.argv) < 2:
    print("Usage: python3 main.py '<text_content>'")
    sys.exit(1)
else:
    main(sys.argv[1])
