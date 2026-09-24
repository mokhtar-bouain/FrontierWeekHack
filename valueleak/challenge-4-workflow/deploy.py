"""
Challenge 4: Production Workflow -- ValueLeak AI

Adapted from the Microsoft Factory Challenge 4 pattern.

Part 1:
    Python orchestrates the persistent Foundry agents step-by-step.

Part 2:
    Build the same single workflow in the Microsoft Foundry portal:
    Scout -> Investigator -> Policy -> Value

The workflow is the same for every business domain. Only the input data changes.
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai.types.responses.response_input_param import FunctionCallOutput


def _find_valueleak_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / ".env").exists() and (parent / "data").exists():
            return parent
    return here.parent.parent


VALUELEAK_ROOT = _find_valueleak_root()
load_dotenv(VALUELEAK_ROOT / ".env")

# Reuse the exact deterministic tool handlers defined and validated in Challenge 1.
CHALLENGE1_DIR = VALUELEAK_ROOT / "challenge-1-agents"
if str(CHALLENGE1_DIR) not in sys.path:
    sys.path.insert(0, str(CHALLENGE1_DIR))

from agents import HANDLERS

PROJECT_CONNECTION_STRING = (
    os.getenv("PROJECT_CONNECTION_STRING")
    or os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    or os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING")
)

SCOUT_AGENT_NAME = "valueleak-scout-agent"
INVESTIGATOR_AGENT_NAME = "valueleak-investigator-agent"
POLICY_AGENT_NAME = "valueleak-policy-agent"
VALUE_AGENT_NAME = "valueleak-value-agent"

DOMAIN_FILES = {
    "procurement": [
        "procurement/invoices.csv",
        "procurement/purchase_orders.csv",
    ],
    "it": [
        "it/cloud_resources.csv",
        "it/cloud_usage.csv",
        "it/cloud_costs.csv",
    ],
    "energy": [
        "energy/energy_consumption.csv",
        "energy/production_output.csv",
    ],
}


def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Missing data file: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_domain_data(domain: str) -> dict:
    """Load the local CSV files for one business domain."""
    result = {"domain": domain, "files": {}}

    for relative_path in DOMAIN_FILES[domain]:
        path = VALUELEAK_ROOT / "data" / relative_path
        result["files"][Path(relative_path).name] = load_csv(path)

    return result


def format_domain_data(domain: str, domain_data: dict) -> str:
    return (
        f"BUSINESS DOMAIN: {domain.upper()}\n\n"
        "The following business data was loaded from ValueLeak synthetic CSV files.\n"
        "Use only the supplied data. Do not invent missing records or values.\n\n"
        f"{json.dumps(domain_data, indent=2, ensure_ascii=False)}"
    )


def _project_client():
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    return AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )


def ensure_agents_deployed():
    """
    Verify the four persistent agents created in Challenge 1.
    Challenge 4 reuses them instead of creating new domain-specific agents.
    """
    print("=== Step 1: Ensure Agents Are Deployed ===")

    client = _project_client()
    existing_names = {agent.name for agent in client.agents.list()}
    client.close()

    required_agents = [
        SCOUT_AGENT_NAME,
        INVESTIGATOR_AGENT_NAME,
        POLICY_AGENT_NAME,
        VALUE_AGENT_NAME,
    ]

    missing = []
    for name in required_agents:
        if name in existing_names:
            print(f"  Found existing: {name}")
        else:
            print(f"  Missing: {name}")
            missing.append(name)

    if missing:
        raise RuntimeError(
            "Complete Challenge 1 first. Missing agents: " + ", ".join(missing)
        )


def call_agent(agent_name: str, input_text: str) -> str:
    """Call one persistent Foundry agent and execute its function-tool loop."""
    client = _project_client()
    openai_client = client.get_openai_client()
    conversation = openai_client.conversations.create()

    agent_ref = {
        "agent_reference": {
            "name": agent_name,
            "type": "agent_reference",
        }
    }

    try:
        response = openai_client.responses.create(
            input=input_text,
            conversation=conversation.id,
            extra_body=agent_ref,
        )

        # Same function-call pattern validated in Challenge 1.
        # Continue until the agent returns a normal final response.
        for _ in range(10):
            function_calls = [
                item for item in response.output
                if item.type == "function_call"
            ]

            if not function_calls:
                final_text = response.output_text or ""
                if not final_text.strip():
                    raise RuntimeError(
                        f"Agent '{agent_name}' finished without a final text response."
                    )
                return final_text

            outputs = []
            for call in function_calls:
                print(f"  -> Tool call: {call.name}({call.arguments})")

                try:
                    handler = HANDLERS.get(call.name)
                    if handler is None:
                        result = {"error": f"Unknown tool '{call.name}'"}
                    else:
                        args = json.loads(call.arguments or "{}")
                        result = handler(**args)
                except Exception as exc:
                    result = {
                        "error": type(exc).__name__,
                        "message": str(exc),
                    }

                serialized = json.dumps(result, default=str, ensure_ascii=False)
                print(f"  <- Tool result: {serialized[:500]}")

                outputs.append(
                    FunctionCallOutput(
                        type="function_call_output",
                        call_id=call.call_id,
                        output=serialized,
                    )
                )

            response = openai_client.responses.create(
                input=outputs,
                conversation=conversation.id,
                extra_body=agent_ref,
            )

        raise RuntimeError(
            f"Agent '{agent_name}' exceeded the maximum number of tool-call rounds."
        )
    finally:
        openai_client.conversations.delete(conversation_id=conversation.id)
        client.close()


def run_scout(domain: str, domain_data: dict) -> str:
    """Scout discovers candidate value leaks."""
    print(f"\n=== Step 2a: Scout — {domain.upper()} ===")

    prompt = (
        format_domain_data(domain, domain_data)
        + "\n\nIdentify potential business value leaks in this dataset. "
          "Return concise candidate findings and cite the supplied records that support them. "
          "Also distinguish normal situations from potential leaks."
    )

    result = call_agent(SCOUT_AGENT_NAME, prompt)
    print(result)
    return result


def run_investigator(domain: str, domain_data: dict, scout_result: str) -> str:
    """Investigator validates or rejects Scout findings."""
    print(f"\n=== Step 2b: Investigator — {domain.upper()} ===")

    prompt = (
        format_domain_data(domain, domain_data)
        + "\n\nSCOUT FINDINGS:\n"
        + scout_result
        + "\n\nValidate or reject each candidate finding against the supplied data. "
          "Give evidence for the decision and explicitly identify uncertainty."
    )

    result = call_agent(INVESTIGATOR_AGENT_NAME, prompt)
    print(result)
    return result


def run_policy(domain: str, domain_data: dict, investigation_result: str) -> str:
    """
    Policy checks the validated findings.

    RAG is intentionally non-blocking for now. When Azure AI Search is attached
    to this existing Policy agent, this workflow does not need to change.
    """
    print(f"\n=== Step 2c: Policy — {domain.upper()} ===")

    prompt = (
        format_domain_data(domain, domain_data)
        + "\n\nVALIDATED FINDINGS:\n"
        + investigation_result
        + "\n\nAssess the validated findings using the policy/contract knowledge "
          "currently available to you. If the relevant policy cannot be verified "
          "because RAG is not yet available, say so explicitly. Never invent a policy."
    )

    result = call_agent(POLICY_AGENT_NAME, prompt)
    print(result)
    return result


def run_value(
    domain: str,
    domain_data: dict,
    investigation_result: str,
    policy_result: str,
) -> str:
    """Value quantifies and prioritizes confirmed opportunities."""
    print(f"\n=== Step 2d: Value — {domain.upper()} ===")

    prompt = (
        format_domain_data(domain, domain_data)
        + "\n\nINVESTIGATION RESULT:\n"
        + investigation_result
        + "\n\nPOLICY RESULT:\n"
        + policy_result
        + "\n\nQuantify the confirmed value leakage only when the supplied evidence "
          "supports the calculation. State assumptions, business impact and recommended "
          "action. Do not fabricate monetary values. Final action remains subject to "
          "validation by the responsible business owner."
    )

    result = call_agent(VALUE_AGENT_NAME, prompt)
    print(result)
    return result


def run_valueleak_workflow(domain: str) -> dict:
    """
    Orchestrate the same four-agent workflow for one domain:
    Scout -> Investigator -> Policy -> Value.
    """
    domain_data = load_domain_data(domain)

    scout = run_scout(domain, domain_data)
    investigator = run_investigator(domain, domain_data, scout)
    policy = run_policy(domain, domain_data, investigator)
    value = run_value(domain, domain_data, investigator, policy)

    return {
        "domain": domain,
        "scout": scout,
        "investigator": investigator,
        "policy": policy,
        "value": value,
    }


def print_valueleak_report(report: dict):
    print("\n" + "=" * 70)
    print(f"VALUELEAK REPORT — {report['domain'].upper()}")
    print("=" * 70)
    print(report["value"])
    print("\nFinal action: subject to validation by the responsible business owner.")
    print("=" * 70)


def print_global_summary(reports: list[dict]):
    print("\n" + "=" * 70)
    print("VALUELEAK GLOBAL REPORT")
    print("=" * 70)

    for report in reports:
        print(f"\n--- {report['domain'].upper()} ---")
        print(report["value"])

    print("\nDomains were processed independently with the same four-agent workflow.")
    print("Final business decisions remain with the responsible business owners.")
    print("=" * 70)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the ValueLeak multi-agent Python workflow."
    )
    parser.add_argument(
        "--domain",
        choices=["procurement", "it", "energy", "all"],
        default="all",
        help=(
            "Select the business domain. "
            "'all' runs Procurement, IT and Energy sequentially."
        ),
    )
    return parser.parse_args()


def main():
    if not PROJECT_CONNECTION_STRING:
        print(
            "Project endpoint/connection string not found in valueleak/.env. "
            "Run Challenge 0 first."
        )
        sys.exit(1)

    args = parse_args()

    ensure_agents_deployed()

    domains = (
        ["procurement", "it", "energy"]
        if args.domain == "all"
        else [args.domain]
    )

    reports = []

    for domain in domains:
        print("\n" + "#" * 70)
        print(f"PROCESSING DOMAIN: {domain.upper()}")
        print("#" * 70)

        report = run_valueleak_workflow(domain)
        print_valueleak_report(report)
        reports.append(report)

    if args.domain == "all":
        print_global_summary(reports)

    print("\nWorkflow complete! Persistent agents remain deployed in Foundry.")


if __name__ == "__main__":
    main()
