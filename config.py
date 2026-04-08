import os

# The model name can be set via the MODEL_NAME environment variable.
# If not set, it defaults to "anthropic:claude-haiku-4-5".
MODEL_NAME = os.getenv("MODEL_NAME", "anthropic:claude-haiku-4-5")

# required for some small models. For larger models, it doesn't change much.
SYSTEM_PROMPT = "You are a helpful assistant for geospatial data. You can use the  tools to answer questions about geospatial data."

from langchain_mcp_adapters.client import MultiServerMCPClient

def get_mcp_client():
    # Préparer les variables d'environnement pour le proxy
    env = os.environ.copy()
    proxy_vars = ["HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY"]
    proxy_env = {var: env[var] for var in proxy_vars if var in env}
    log_level = env.get("GEOCONTEXT_LOG_LEVEL", "error")

    client = MultiServerMCPClient(
        {
            "geocontext": {
                "command": "npx",
                "args": ["-y", "@ignfab/geocontext"],
                "transport": "stdio",
                "env": {**proxy_env, "LOG_LEVEL": log_level} if proxy_env else {"LOG_LEVEL": log_level}
            }
        }
    )
    return client

