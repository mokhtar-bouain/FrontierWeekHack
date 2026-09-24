"""
ValueLeak AI — Challenge 2: Monitor with Application Insights

Enables GenAI tracing and executes a real ValueLeak Scout Agent call so the
interaction can be inspected in Microsoft Foundry and Application Insights.

Usage:
    python monitor.py

IMPORTANT:
Environment variables are loaded before importing azure.ai.projects because
GenAI tracing must be enabled before SDK initialization.
"""

import os
import sys
import time
import json
from pathlib import Path

from dotenv import load_dotenv


# =============================================================================
# Load environment FIRST
# =============================================================================

def _find_valueleak_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists():
            return parent
    return Path(__file__).resolve().parents[1]


VALUELEAK_ROOT = _find_valueleak_root()
load_dotenv(VALUELEAK_ROOT / ".env")

if os.getenv("AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING") != "true":
    print("ERROR: AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING must be 'true' in .env")
    sys.exit(1)

PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.4")
APPINSIGHTS_CONN_STRING = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")


# Reuse the tested IT tool from Challenge 1.
CHALLENGE1_DIR = VALUELEAK_ROOT / "challenge-1-agents"
if str(CHALLENGE1_DIR) not in sys.path:
    sys.path.insert(0, str(CHALLENGE1_DIR))

from tools.it_tools import check_low_utilization

def scout_it(resource_id: str) -> dict:
    result = check_low_utilization(resource_id)
    result["domain"] = "it"
    return result


# =============================================================================
# Tracing
# =============================================================================

def setup_tracing():
    """Configure Foundry GenAI instrumentation and Azure Monitor export."""
    print("=== Setting up ValueLeak tracing ===")
    print("OK AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING is enabled")

    from azure.ai.projects.telemetry import AIProjectInstrumentor
    AIProjectInstrumentor().instrument()
    print("OK AIProjectInstrumentor configured")

    if not APPINSIGHTS_CONN_STRING:
        print("ERROR: APPLICATIONINSIGHTS_CONNECTION_STRING is not set")
        sys.exit(1)

    from azure.monitor.opentelemetry import configure_azure_monitor
    configure_azure_monitor(
        connection_string=APPINSIGHTS_CONN_STRING,
        enable_live_metrics=True,
    )
    print("OK Azure Monitor exporter connected")


# =============================================================================
# Real ValueLeak agent call
# =============================================================================

def run_traced_valueleak_call():
    """
    Invoke the existing ValueLeak Scout Agent.

    Challenge 1 created this agent and kept it in Foundry. This challenge
    references that same agent instead of creating an unrelated tracing agent.
    """
    print("\n=== Running traced ValueLeak Scout call ===")

    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    openai_client = client.get_openai_client()

    conversation = openai_client.conversations.create()

    try:
        response = openai_client.responses.create(
            input=(
                "Create monitoring case MON-IT-001. "
                "Analyze resource VM-002 for a potential ValueLeak IT/Cloud opportunity. "
                "You MUST use the appropriate Scout tool to obtain the utilization evidence. "
                "Determine whether the resource requires investigation. "
                "Do not classify it as confirmed waste."
            ),
            conversation=conversation.id,
            extra_body={
                "agent_reference": {
                    "name": "valueleak-scout-agent",
                    "type": "agent_reference",
                }
            },
        )

        # Handle the Scout FunctionTool call so it is part of the traced run.
        while True:
            function_calls = [
                item for item in response.output
                if item.type == "function_call"
            ]
            if not function_calls:
                break

            from openai.types.responses.response_input_param import FunctionCallOutput

            outputs = []
            for item in function_calls:
                if item.name != "scout_it":
                    result = {"error": f"Unexpected tool: {item.name}"}
                else:
                    args = json.loads(item.arguments or "{}")
                    result = scout_it(args["resource_id"])

                outputs.append(
                    FunctionCallOutput(
                        type="function_call_output",
                        call_id=item.call_id,
                        output=json.dumps(result, default=str),
                    )
                )

            response = openai_client.responses.create(
                input=outputs,
                conversation=conversation.id,
                extra_body={
                    "agent_reference": {
                        "name": "valueleak-scout-agent",
                        "type": "agent_reference",
                    }
                },
            )

        print("OK ValueLeak Scout responded")
        print(response.output_text)
        print(f"Conversation ID: {conversation.id}")

    finally:
        openai_client.conversations.delete(conversation_id=conversation.id)
        client.close()


# =============================================================================
# Verification guidance
# =============================================================================

def verify_traces():
    """Allow telemetry to propagate before portal inspection."""
    print("\n=== Waiting for telemetry propagation ===")
    print("Waiting 30 seconds...")
    time.sleep(30)

    print("\nOK ValueLeak trace should now be available.")
    print("Check Microsoft Foundry:")
    print("  valueleak-scout-agent -> Traces")
    print("")
    print("Check Application Insights:")
    print("  Investigate -> Search")
    print("  Time range: Last 30 minutes")
    print("")
    print("Verify:")
    print("  - agent run")
    print("  - model call")
    print("  - input/output")
    print("  - duration / latency")
    print("  - token usage")
    print("  - errors, if any")


# =============================================================================
# Main
# =============================================================================

def main():
    if not PROJECT_CONNECTION_STRING:
        print("ERROR: PROJECT_CONNECTION_STRING not set. Run Challenge 0 first.")
        sys.exit(1)

    setup_tracing()
    run_traced_valueleak_call()
    verify_traces()

    print("\nMonitoring test completed.")
    print("The existing ValueLeak agents are kept in Foundry.")


if __name__ == "__main__":
    main()
