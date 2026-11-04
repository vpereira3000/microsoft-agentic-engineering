import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Retrieve the variables
azure_api_key = os.getenv("AZURE_API_KEY")
azure_project_endpoint = os.getenv("AZURE_PROJECT_ENDPOINT")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

# Test to make sure they loaded correctly
print(f"Project Endpoint: {azure_project_endpoint}")
print(f"OpenAI Endpoint: {azure_openai_endpoint}")
print(f"Key loaded successfully: {bool(azure_api_key)}")
