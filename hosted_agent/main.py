import asyncio
import logging
import os
from pathlib import Path

from agent_framework_foundry_hosting import ResponsesHostServer
from dotenv import load_dotenv

from agent import create_agent


async def main() -> None:
    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False, interpolate=False)
    if not os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME"):
        os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = os.environ.get("FOUNDRY_MODEL", "")
    if not os.environ.get("TOOLBOX_ENDPOINT"):
        project = os.environ.get("FOUNDRY_PROJECT_ENDPOINT", "").rstrip("/")
        name = os.environ.get("FOUNDRY_TOOLBOX_NAME", "")
        version = os.environ.get("FOUNDRY_TOOLBOX_VERSION", "").strip()
        suffix = f"/versions/{version}" if version else ""
        os.environ["TOOLBOX_ENDPOINT"] = f"{project}/toolboxes/{name}{suffix}/mcp?api-version=v1"
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    async with create_agent() as agent:
        server = ResponsesHostServer(agent)
        await server.run_async(host="0.0.0.0", port=8088)


if __name__ == "__main__":
    asyncio.run(main())
