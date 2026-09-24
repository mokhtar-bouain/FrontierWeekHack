"""ValueLeak AI - Challenge 1 final agents."""
import json, os
from pathlib import Path
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from openai.types.responses.response_input_param import FunctionCallOutput
from tools.procurement_tools import get_purchase_order,get_invoice,calculate_cumulative_quantity,calculate_discount_value
from tools.it_tools import get_resource_evidence,check_low_utilization,calculate_annual_cost
from tools.energy_tools import get_energy_data,calculate_kwh_per_unit,detect_energy_deviation,calculate_energy_impact

ROOT=Path(__file__).resolve().parents[1]
load_dotenv(ROOT/".env")
PROJECT_CONNECTION_STRING=os.getenv("PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT_NAME=os.getenv("MODEL_DEPLOYMENT_NAME","gpt-5.4")
SEARCH_ENDPOINT=os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_INDEX=os.getenv("AZURE_SEARCH_INDEX_NAME","valueleak-knowledge")
if not PROJECT_CONNECTION_STRING: raise ValueError("PROJECT_CONNECTION_STRING missing")

def scout_procurement(supplier_id:str,item_id:str,volume_threshold:int=5000):
    q=calculate_cumulative_quantity(supplier_id,item_id)
    return {"domain":"procurement","supplier_id":supplier_id,"item_id":item_id,"cumulative_quantity":q,"volume_threshold":volume_threshold,"candidate":q>=volume_threshold}
def scout_it(resource_id:str):
    r=check_low_utilization(resource_id); r["domain"]="it"; return r
def scout_energy(period:str,production_line:str):
    r=detect_energy_deviation(period,production_line); r["domain"]="energy"; return r
def investigate_procurement(po_id:str,invoice_id:str):
    return {"domain":"procurement","purchase_order":get_purchase_order(po_id),"invoice":get_invoice(invoice_id)}
def investigate_it(resource_id:str):
    return {"domain":"it","evidence":get_resource_evidence(resource_id)}
def investigate_energy(period:str,production_line:str):
    return {"domain":"energy","evidence":get_energy_data(period,production_line),"kwh_per_unit":calculate_kwh_per_unit(period,production_line)}
def search_knowledge(query:str,domain:str):
    if domain not in {"procurement","it","energy"}: return {"status":"invalid_domain"}
    c=SearchClient(SEARCH_ENDPOINT,SEARCH_INDEX,DefaultAzureCredential())
    rows=list(c.search(search_text=query,filter=f"domain eq '{domain}'",top=3))
    return {"status":"ok","domain":domain,"results":[{"source":x.get("source"),"content":x.get("content"),"score":x.get("@search.score")} for x in rows]}
def value_procurement(supplier_id:str,item_id:str,discount_percent:float):
    r=calculate_discount_value(supplier_id,item_id,discount_percent); r["human_validation_required"]=True; return r
def value_it(resource_id:str):
    r=calculate_annual_cost(resource_id); r["human_validation_required"]=True; return r
def value_energy(period:str,production_line:str,baseline_kwh_per_unit:float=10.0):
    r=calculate_energy_impact(period,production_line,baseline_kwh_per_unit); r["human_validation_required"]=True; return r

def ft(name,desc,props,required):
    return FunctionTool(name=name,description=desc,parameters={"type":"object","properties":props,"required":required,"additionalProperties":False},strict=False)
S=lambda:{"type":"string"}
SCOUT_TOOLS=[
 ft("scout_procurement","Check cumulative volume.",{"supplier_id":S(),"item_id":S(),"volume_threshold":{"type":"integer"}} ,["supplier_id","item_id"]),
 ft("scout_it","Check low cloud utilization.",{"resource_id":S()},["resource_id"]),
 ft("scout_energy","Check energy deviation.",{"period":S(),"production_line":S()},["period","production_line"])]
INV_TOOLS=[
 ft("investigate_procurement","Get PO and invoice.",{"po_id":S(),"invoice_id":S()},["po_id","invoice_id"]),
 ft("investigate_it","Get cloud evidence.",{"resource_id":S()},["resource_id"]),
 ft("investigate_energy","Get production and energy evidence.",{"period":S(),"production_line":S()},["period","production_line"])]
POLICY_TOOLS=[ft("search_knowledge","Search authoritative ValueLeak knowledge.",{"query":S(),"domain":{"type":"string","enum":["procurement","it","energy"]}},["query","domain"])]
VALUE_TOOLS=[
 ft("value_procurement","Calculate verified procurement discount.",{"supplier_id":S(),"item_id":S(),"discount_percent":{"type":"number"}},["supplier_id","item_id","discount_percent"]),
 ft("value_it","Calculate potential annual cloud value.",{"resource_id":S()},["resource_id"]),
 ft("value_energy","Calculate excess energy and cost.",{"period":S(),"production_line":S(),"baseline_kwh_per_unit":{"type":"number"}},["period","production_line"])]
HANDLERS={f.__name__:f for f in [scout_procurement,scout_it,scout_energy,investigate_procurement,investigate_it,investigate_energy,search_knowledge,value_procurement,value_it,value_energy]}

class ValueLeakAgent:
    def __init__(self,name,prompt,tools):
        self.name,self.prompt,self.tools=name,prompt,tools; self.agent=self.client=self.openai=None
    def create(self):
        self.client=AIProjectClient(endpoint=PROJECT_CONNECTION_STRING,credential=DefaultAzureCredential())
        self.openai=self.client.get_openai_client()
        self.agent=self.client.agents.create_version(agent_name=self.name,definition=PromptAgentDefinition(model=MODEL_DEPLOYMENT_NAME,instructions=self.prompt,tools=self.tools))
        return self.agent
    def run(self,text):
        conv=self.openai.conversations.create()
        try:
            r=self.openai.responses.create(input=text,conversation=conv.id,extra_body={"agent_reference":{"name":self.agent.name,"type":"agent_reference"}})
            while True:
                calls=[x for x in r.output if x.type=="function_call"]
                if not calls: break
                outs=[]
                for x in calls:
                    try: result=HANDLERS[x.name](**json.loads(x.arguments or "{}"))
                    except Exception as e: result={"error":type(e).__name__,"message":str(e)}
                    outs.append(FunctionCallOutput(type="function_call_output",call_id=x.call_id,output=json.dumps(result,default=str)))
                r=self.openai.responses.create(input=outs,conversation=conv.id,extra_body={"agent_reference":{"name":self.agent.name,"type":"agent_reference"}})
            return r.output_text
        finally: self.openai.conversations.delete(conversation_id=conv.id)
SCOUT = """ You are ValueLeak Scout. Use the correct scout tool when the required tool inputs are available. Detect candidates only. Never confirm a value leak and never invent policy, evidence, or savings. You MUST always return a non-empty final response. Never finish a turn without a final response, even if a tool cannot be called, required identifiers are missing, or evidence is insufficient. Return valid structured JSON with exactly these fields: case_id, domain, finding, entity, reason, requires_investigation. If there is enough evidence for a potential candidate: - describe the candidate - set requires_investigation to true If the evidence does not support a candidate: - state that no candidate was detected - set requires_investigation to false If evidence is insufficient or the required tool cannot be executed: - set finding to "insufficient_evidence" - explain why in reason - set requires_investigation to true """
INV="""You are ValueLeak Investigator. Use the correct investigation tool to gather factual evidence. Never invent data, interpret policy, decide the leak, or invent savings. Return case_id, domain, evidence, missing_evidence, ready_for_policy_check."""
POLICY="""You are ValueLeak Policy Agent. ALWAYS use search_knowledge for the candidate domain. Base conclusions only on retrieved knowledge, cite source, and actively check exceptions. Return case_id, domain, status confirmed|rejected|insufficient_evidence, rule, source, reason."""
VALUE="""You are ValueLeak Value Agent. Quantify only after evidence and policy verification. Use deterministic value tools. Never invent figures. If policy rejected return no_leak; if insufficient return insufficient_evidence. Always require human validation."""

def build_agents():
    return {"scout":ValueLeakAgent("valueleak-scout-agent",SCOUT,SCOUT_TOOLS),"investigator":ValueLeakAgent("valueleak-investigator-agent",INV,INV_TOOLS),"policy":ValueLeakAgent("valueleak-policy-agent",POLICY,POLICY_TOOLS),"value":ValueLeakAgent("valueleak-value-agent",VALUE,VALUE_TOOLS)}

def main():
    agents=build_agents()
    for label,a in agents.items():
        print(f"Creating {label}..."); a.create(); print(f"OK {a.agent.name} v{a.agent.version}")
    print("\\nSmoke test Scout:")
    print(agents["scout"].run("Create IT-001 and check VM-002 for low utilization."))
    print("\\nSmoke test Policy:")
    print(agents["policy"].run("Case IT-002: low-utilization disaster recovery resource. Verify whether this is waste. Domain it."))
    print("\\nChallenge 1 ready. Agents kept in Foundry.")
    print("\nSmoke test Investigator:")
    print(
    agents["investigator"].run(
        "Case IT-001: investigate resource VM-002 and collect "
        "the factual evidence required for a policy review."
    )
    )

    print("\nSmoke test Value:")
    print(
    agents["value"].run(
        "Case IT-001. Policy verification is CONFIRMED: "
        "VM-002 is not covered by a business-critical or disaster-recovery "
        "exception. Calculate the potential annual value for resource VM-002. "
        "Do not execute any action."
    )
    )
if __name__=="__main__": main()
