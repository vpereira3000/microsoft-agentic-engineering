# Microsoft Agentic Engineering

Practical examples for learning AI agent development with **Microsoft Foundry, Python, Visual Studio Code, and Microsoft Entra ID**.

This first example runs a simple agent using a deployed model and service principal authentication. It accompanies the article:

**[Setting Up Microsoft Foundry for AI Agent Development with Python and VS Code](https://pereiravictor.com/blog/setting-up-microsoft-foundry-python-vscode.html)**

The author successfully ran the original example with a **GPT-5 mini** deployment using settings loaded from a local `.env` file. This repository provides a sanitized, commented version for learning and adaptation.

## Files

| File | Purpose |
| --- | --- |
| `hello_aget.py` | Creates an agent, authenticates with a service principal, and prints one response. |
| `.env` | Public configuration template with private values masked as `*****`. |
| `README.md` | Setup and usage instructions. |

The script filename is intentionally shown as supplied: **`hello_aget.py`**. If you rename it to `hello_agent.py`, adjust the commands below.

## Prerequisites

- Python supported by the current Microsoft Agent Framework packages.
- Visual Studio Code with the Microsoft Python extension, or another Python editor.
- An Azure subscription and a Microsoft Foundry project.
- A successfully provisioned model deployment accessible through that project.
- A Microsoft Entra application registration with a service principal and client secret.
- Appropriate Foundry permissions assigned to that service principal, directly or through a security group.

Creating a project does not automatically create a model deployment. Registering an application does not automatically grant access to Azure resources.

## 1. Prepare the Python environment

Open the folder containing the example in VS Code. In its PowerShell terminal, run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install agent-framework python-dotenv azure-identity
```

In VS Code, open the Command Palette, select **Python: Select Interpreter**, and choose the interpreter inside `.venv`.

If PowerShell blocks activation, use the virtual environment interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install agent-framework python-dotenv azure-identity
.\.venv\Scripts\python.exe hello_aget.py
```

## 2. Configure service principal access

1. In Azure portal, create an application registration in **Microsoft Entra ID**.
2. Record its **Application (client) ID** and **Directory (tenant) ID** locally.
3. Create a client secret and record its **Value**, not its secret ID.
4. Assign the application identity appropriate access to the Foundry resource. For this walkthrough, use **Foundry User**, which may appear as **Azure AI User** in some interfaces.
5. If using a security group, add the service principal as a member and assign the role to that group.
6. Allow role assignments to propagate before testing.

The script uses `ClientSecretCredential`; Azure CLI installation and an `az login` session are not required for this authentication path.

See [Microsoft's service principal setup guide](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/local-development-service-principal).

## 3. Configure your local environment

Keep `.env` beside `hello_aget.py`. Replace the asterisks **only in your local copy**:

```dotenv
AZURE_TENANT_ID=*****
AZURE_CLIENT_ID=*****
AZURE_CLIENT_SECRET=*****
AZURE_PROJECT_ENDPOINT=*****
AZURE_MODEL_DEPLOYMENT_NAME=gpt-5-mini

# Optional: retained for future experiments; not used by this request.
AZURE_API_KEY=*****
AZURE_OPENAI_ENDPOINT=*****
AZURE_AI_REGION=*****
```

| Setting | Where the value comes from |
| --- | --- |
| `AZURE_TENANT_ID` | Directory (tenant) ID in the app registration. |
| `AZURE_CLIENT_ID` | Application (client) ID in the app registration. |
| `AZURE_CLIENT_SECRET` | Client secret **Value** from Certificates & secrets. |
| `AZURE_PROJECT_ENDPOINT` | **Project endpoint** displayed in your Foundry project. |
| `AZURE_MODEL_DEPLOYMENT_NAME` | Exact name of a successful deployment in the resource used by your project. |

The project endpoint has this structure, with private components masked:

```text
https://*****.services.ai.azure.com/api/projects/*****
```

`gpt-5-mini` is the deployment name used in the author's working setup. If your deployment has another name, use that exact name instead.

`python-dotenv` loads settings into the Python process. It does not create credentials or Azure resources. The script loads `.env` relative to its own location; existing process environment variables take precedence over values in the file.

### Protect your credentials

The published `.env` contains illustrative values only. **Never upload a populated `.env`, client secret, token, or private endpoint.**

For ongoing development, publish this template as `.env.example`, create an untracked local `.env`, and add these entries to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
```

If `.env` is already tracked, adding it to `.gitignore` does not untrack it. Before entering real values, remove it from Git tracking while keeping the local file:

```powershell
git rm --cached .env
```

Commit that change along with the sanitized `.env.example` and `.gitignore`. If a real secret was published, revoke or rotate it; deleting the current file does not remove the secret from repository history.

## 4. Run the agent

```powershell
python hello_aget.py
```

The script:

1. Loads local configuration.
2. Checks that required settings are present and not masked.
3. Authenticates with the service principal.
4. Creates an `Agent` using `FoundryChatClient` and your deployment name.
5. Sends one question and prints the response.

The prompt asks for the largest city in the United States by population. A typical response identifies **New York City**; wording and additional details can vary.

The script defines the agent locally. It does not create a named, server-managed agent in the Foundry portal. The optional API key, Azure OpenAI endpoint, and region settings remain available for future experiments but do not affect this request.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Missing or masked setting | Replace `*****` locally and check environment variable names. |
| Authentication failure | Check tenant ID, client ID, and the secret value and expiration. |
| `403 PermissionDenied` | Verify the service principal's role, scope, group membership, propagation, and resource network restrictions. |
| `404` deployment does not exist | Verify the project endpoint, successful deployment status, and exact deployment name. |
| `429 Too Many Requests` | Check assigned quota, reduce request frequency, and follow service retry guidance. |
| Unexpected configuration | Check for existing shell environment variables overriding `.env`. |

Do not include credentials, tokens, or private endpoint values when sharing diagnostic output.

## Cost awareness

Model requests can incur Azure charges. Start with short prompts and sequential requests. Check available model capacity before requesting additional quota.

**Azure Cost Management budgets provide alerts; they do not automatically stop spending.** TPM and RPM quotas limit throughput, not monthly expenditure. When extending this example, bound retries, tool calls, agent loops, and execution time.

For Azure-hosted applications, consider managed identity instead of maintaining a client secret.

## References

- [Microsoft Agent Framework: Your First Agent](https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent?pivots=programming-language-python)
- [Azure Python authentication overview](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/overview)
- [Local development using service principals](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/local-development-service-principal)
- [Microsoft Foundry role-based access control](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry)
- [Create and manage Azure budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets)
- [Manage model quota](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/quota)
- [AI Agents for Beginners](https://microsoft.github.io/ai-agents-for-beginners/)

## Author

**Victor Pereira** — personal training, technical writing, and experiments in agentic engineering.

- [Technical writings](https://pereiravictor.com/blog/technical_writing.html)
- [Companion repository](https://github.com/vpereira3000/microsoft-agentic-engineering)

This example adapts Microsoft's first-agent tutorial with attribution. It is a learning example; configuration, model availability, and package requirements may change.
