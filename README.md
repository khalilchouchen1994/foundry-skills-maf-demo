# Foundry skills with Microsoft Agent Framework

Four Python notebooks demonstrating **existing skill -> Foundry Toolbox -> MAF
agent -> hosted agent**. Manage skill versions with the Foundry SDK, expose
instructions over MCP, and deploy the agent to Foundry.

## Azure setup

1. Create a resource group and a **Foundry resource with a project** in
   [Microsoft Foundry](https://ai.azure.com). Use the current Foundry experience,
   not a classic hub.
2. Deploy a model supporting function calling and the Responses API, e.g.
   **GPT-5.4 mini**.
3. Give the account running the notebooks **Foundry User** access on the project.
4. Copy the project endpoint from its overview:
   `https://<resource>.services.ai.azure.com/api/projects/<project>`.

## Run

Python 3.11+, Azure CLI and VS Code with Jupyter support:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
# Fill .env with your project endpoint, model deployment name and account IDs.
az login --tenant "<your-tenant-id>"
az account set --subscription "<your-subscription-id>"
```

Select `.venv` as the notebook kernel. Use your organization's approved
package feed. Authentication uses Azure CLI: **do not save passwords, API keys
or access tokens in `.env`**.

| Notebook | What it does |
|---|---|
| [01 - Skill management](notebooks/01_skill_management.ipynb) | Import SKILL.md, create a revision and publish a default skill version. |
| [02 - Toolbox MCP](notebooks/02_toolbox_mcp.ipynb) | Attach the skill version, inspect MCP resources and publish the Toolbox configuration. |
| [03 - MAF agent](notebooks/03_maf_toolbox_agent.ipynb) | Discover and load the skill through MCP, run an assessment and verify loading and report structure. |
| [04 - Hosted agent](notebooks/04_deploy_hosted_agent.ipynb) | Review the runtime files, ZIP and upload through the Python SDK, then invoke the hosted agent. |

Run cells in order. After notebook 01, copy its printed
`FOUNDRY_SKILL_NAME` and `FOUNDRY_SKILL_VERSION` into `.env` before notebook 02.
The included [skill](.github/skills/engineering-impact-assessment/SKILL.md) is a
sample; importing a different skill also requires adapting the task and checks
in notebook 03. Inline import supports single-file skills only.

The notebooks are self-contained and load the root `.env`. Existing process
variables take precedence; restart the kernel after changing configuration.
Keep [notebooks/images](notebooks/images) with the notebooks for the portal
screenshots.

Notebook 04 starts with a file-by-file review of [hosted_agent](hosted_agent),
already supplied for the tutorial. Python creates an allowlisted ZIP and the
Foundry SDK uploads it with `create_version_from_code`. Foundry builds runtime
dependencies from the approved feed specified in the notebook-04 environment
settings. No Docker, ACR or azd is required. The deploying account needs
Foundry Project Manager access; the hosted identity needs Foundry User.
No new resource group, project or model is created by this walkthrough.

## Behavior and boundaries

- **Skill versions** store instructions; **Toolbox versions** store a
  configuration referencing specific skill versions.
- **Publish** selects a default, not public access. **Pin** selects an explicit
  version; **rollback** selects an earlier retained default. Clients may cache
  skill content.
- Toolbox has `tools=[]`. MAF supplies the client-side `load_skill` function
  and retrieves instructions through MCP resources.
- Notebook 03 runs the MAF agent in the notebook process. Notebook 04 deploys
  it as a hosted agent; scalability testing is not included.
- Calls are real and model usage is billable. Repeating create cells adds
  immutable versions. Review and remove unused Azure resources when finished.
- Skills, Toolbox and the native MAF MCP skill source are preview/experimental
  surfaces. Notebook outputs and local execution artifacts are not published.

[Foundry skills](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/skills) |
[Foundry Toolbox](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/toolbox) |
[MAF skills](https://learn.microsoft.com/agent-framework/agents/skills?pivots=programming-language-python)
