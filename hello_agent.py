import os
import asyncio

from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import ClientSecretCredential

# Load the environment variables from the .env file
load_dotenv()

tenant_id = os.environ.get("AZURE_TENANT_ID")
client_id = os.environ.get("AZURE_CLIENT_ID")
client_secret = os.environ.get("AZURE_CLIENT_SECRET")
model_deployment_name = os.environ.get("AZURE_MODEL_DEPLOYMENT_NAME")

client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# Retrieve the variables
azure_api_key = os.getenv("AZURE_API_KEY")
azure_project_endpoint = os.getenv("AZURE_PROJECT_ENDPOINT")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

async def main() -> None:
    agent = Agent(
        client=FoundryChatClient(
            project_endpoint=azure_project_endpoint,
            model=model_deployment_name,
            credential=client_credential,
        ),
        instructions="You are a friendly assistant. Keep your answers brief.",
    )
    print(await agent.run("What is the largest city of United States?"))


if __name__ == "__main__":
    asyncio.run(main())