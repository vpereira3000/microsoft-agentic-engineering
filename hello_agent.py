"""Run a first Microsoft Foundry agent using a service principal.

Adapted from Microsoft's first-agent tutorial:
https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent

Install in your virtual environment:
    python -m pip install agent-framework python-dotenv azure-identity

Place your LOCAL, populated .env beside this file, then run:
    python hello_aget.py

The published .env contains masked examples only. Keep actual credentials
outside Git. This script never prints credentials or endpoint values.
"""

import asyncio
import os
from pathlib import Path

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv


def required_setting(name: str) -> str:
    """Require a configured value without including it in an error message."""
    value = os.getenv(name, "").strip()
    if not value or "*****" in value:
        raise ValueError(f"Configure {name} locally; it is missing or masked.")
    return value


async def main() -> None:
    # Resolve .env relative to this script, regardless of the terminal directory.
    # Existing process environment variables take precedence over .env values.
    load_dotenv(Path(__file__).resolve().with_name(".env"), override=False)

    tenant_id = required_setting("AZURE_TENANT_ID")
    client_id = required_setting("AZURE_CLIENT_ID")
    client_secret = required_setting("AZURE_CLIENT_SECRET")
    azure_project_endpoint = required_setting("AZURE_PROJECT_ENDPOINT")
    model_deployment_name = required_setting("AZURE_MODEL_DEPLOYMENT_NAME")

    # Retained for future experiments. This request uses Entra authentication,
    # not the API key or the separate Azure OpenAI endpoint.
    azure_api_key = os.getenv("AZURE_API_KEY")
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    # The app identity needs appropriate Foundry access, directly or via a group.
    # An identity alone does not grant permission or create a model deployment.
    with ClientSecretCredential(tenant_id, client_id, client_secret) as credential:
        agent = Agent(
            client=FoundryChatClient(
                project_endpoint=azure_project_endpoint,
                # Use your deployment NAME, which can differ from the model ID.
                model=model_deployment_name,
                credential=credential,
            ),
            instructions="You are a friendly assistant. Keep your answers brief.",
        )
        # One inference request; Azure usage charges may apply.
        response = await agent.run(
            "What is the largest city in the United States by population?"
        )
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
