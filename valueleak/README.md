# 💰 ValueLeak AI

## Turn Hidden Waste into Measurable Value

> **An autonomous multi-agent value leakage hunter built with Microsoft
> Foundry.**\
> ValueLeak AI proactively detects hidden financial, operational, and
> sustainability opportunities across enterprise data --- then validates
> the evidence, checks business rules, quantifies the impact, and keeps
> a human in control.

------------------------------------------------------------------------

## 🎯 The Problem

Companies rarely lose value through one obvious mistake.

Instead, value leaks through small signals scattered across different
systems:

-   a contractual discount that was not applied;
-   a cloud resource that costs money while barely being used;
-   an apparent anomaly that is actually a legitimate business
    exception;
-   an industrial process consuming more energy than its expected
    baseline.

The data is often already available.

**The evidence is scattered.**

ValueLeak AI connects those signals and turns them into
**evidence-backed, measurable opportunities**.

------------------------------------------------------------------------

## 🚀 The Mission

Build a reusable AI agent system that can:

1.  **Detect** potential value leakage proactively.
2.  **Investigate** the underlying business evidence.
3.  **Verify** contracts, policies, rules, and exceptions using RAG.
4.  **Quantify** financial or environmental impact with deterministic
    tools.
5.  **Recommend** an evidence-backed next step.
6.  **Require human validation** before any business action.

ValueLeak AI is not designed as another chatbot.

It is a **proactive value discovery system**.

------------------------------------------------------------------------

## ✨ What Makes ValueLeak AI Different?

A low-utilization VM is not necessarily waste.

A higher invoice price is not necessarily an overcharge.

Higher energy consumption is not necessarily inefficiency.

The same signal can represent either **real value leakage or a
legitimate exception**.

That is why ValueLeak AI separates detection from business validation:

``` text
Signal ≠ Leak

Signal
  ↓
Evidence
  ↓
Policy / Contract / Business Rule
  ↓
Deterministic Quantification
  ↓
Evidence-backed Opportunity
  ↓
Human Decision
```

This reduces false positives and makes every recommendation explainable.

------------------------------------------------------------------------

# 🧠 Multi-Agent Architecture

ValueLeak AI uses **four shared specialized agents** across all business
domains.

``` text
                         VALUELEAK AI

 Enterprise Data
       │
       ▼
┌───────────────────────┐
│     🔎 SCOUT AGENT    │
│ Detect candidates     │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│  🕵️ INVESTIGATOR      │
│ Gather evidence       │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐       ┌─────────────────────┐
│  📚 POLICY AGENT      │◄─────►│ Azure AI Search RAG │
│ Rules + exceptions    │       │ Contracts / Policies│
└──────────┬────────────┘       └─────────────────────┘
           │
           ▼
┌───────────────────────┐
│    💶 VALUE AGENT     │
│ Quantify impact       │
└──────────┬────────────┘
           │
           ▼
  Evidence-backed
  Value Opportunity
           │
           ▼
      👤 HUMAN
   Validate / Reject
```

### 🔎 Scout Agent

Answers:

> **Is there something worth investigating?**

It scans business data using domain-specific deterministic tools and
identifies candidates.

It does **not** confirm leakage and does **not** calculate savings.

### 🕵️ Investigator Agent

Answers:

> **What does the evidence actually show?**

It gathers relevant records, validates the candidate, identifies
contradictions, and explicitly reports missing evidence.

### 📚 Policy Agent

Answers:

> **Does the business context confirm or reject the candidate?**

It uses **Azure AI Search RAG** to retrieve contracts, FinOps policies,
and energy guidelines.

It checks exceptions before a candidate is treated as an opportunity.

### 💶 Value Agent

Answers:

> **What is the measurable potential value?**

It quantifies only policy-supported opportunities using deterministic
calculation tools.

Financial and energy values are not left to free-form LLM arithmetic.

------------------------------------------------------------------------

# 💼 Three Business Domains --- One Reusable Architecture

The same four agents operate across all three demonstration domains.

Domain-specific behavior lives in **tools and knowledge**, not in
separate agents.

------------------------------------------------------------------------

## 🛒 Procurement --- Recover Missed Contract Value

### Scenario

A supplier contract defines:

``` text
Supplier: SUP-001
Item: COMP-A
Base price: EUR 12/unit

Annual cumulative volume >= 5,000 units
→ 10% retroactive discount
```

Actual annual purchases:

``` text
3 purchase orders × 2,000 units
= 6,000 units

Gross value
= 6,000 × EUR 12
= EUR 72,000
```

The Scout detects the volume threshold.

The Investigator validates the POs and invoices.

The Policy Agent retrieves the applicable contract through Azure AI
Search.

The Value Agent performs the deterministic calculation:

``` text
EUR 72,000 × 10% = EUR 7,200
```

### 💰 Potential Value

> **EUR 7,200**

subject to Procurement / AP validation.

### 🛡️ False Positive Prevention

ValueLeak also detects an apparent mismatch:

``` text
PO price      = EUR 25/unit
Invoice price = EUR 27/unit
```

At first glance:

> Possible overcharge.

But the Policy Agent retrieves the contract and discovers:

``` text
Certified expedited delivery
→ authorized surcharge = EUR 2/unit
```

The purchase order explicitly requests expedited delivery.

**Result: NO LEAK.**

The system avoids turning a valid contractual charge into a false saving
opportunity.

------------------------------------------------------------------------

## ☁️ IT / Cloud --- Find Hidden Infrastructure Waste

The Scout identifies two resources with extremely low utilization.

### VM-002 --- Test Resource

``` text
Resource: VM-TEST-03
Environment: test
CPU: 0.8%
Monthly requests: 12
Monthly cost: EUR 500
```

The Investigator validates the evidence.

The Policy Agent retrieves the FinOps policy and confirms that sustained
low-utilization non-production resources may be considered optimization
candidates after owner validation.

The Value Agent calculates:

``` text
EUR 500 × 12
= EUR 6,000/year
```

### 💰 Potential Value

> **Up to EUR 6,000/year**

depending on the owner-approved optimization action.

### 🛡️ Disaster Recovery Exception

Another VM looks even less utilized:

``` text
Resource: VM-BACKUP-01
CPU: 0.3%
Monthly requests: 1
```

A naive optimization engine could flag it as obvious waste.

But the Investigator discovers:

``` text
Environment = disaster_recovery
Criticality = critical
```

The Policy Agent retrieves the FinOps exception:

> Disaster Recovery resources are intentionally maintained in a ready
> state. Low utilization alone must not be interpreted as waste.

**Result: NO LEAK.**

------------------------------------------------------------------------

## 🌱 Energy / Sustainability --- Detect Efficiency Drift

ValueLeak compares energy consumption normalized by production output.

For LINE-01 / PRODUCT-A:

``` text
Normal baseline ≈ 10 kWh/unit
April 2026      = 13 kWh/unit
Production      = 1,000 units
```

The Policy Agent retrieves the applicable energy guideline and confirms
the expected baseline.

The deterministic Value tool calculates:

``` text
Expected energy = 10,000 kWh
Actual energy   = 13,000 kWh
--------------------------------
Potential excess = 3,000 kWh
```

At:

``` text
EUR 0.20/kWh
```

the potential excess cost is:

``` text
3,000 × EUR 0.20 = EUR 600
```

### 🌱 Potential Value

> **3,000 kWh potential excess consumption**\
> **EUR 600 potential excess energy cost**

The result is treated as an efficiency anomaly requiring investigation
--- not as proof of root cause.

------------------------------------------------------------------------

# 📊 Demonstrated Value

  ------------------------------------------------------------------------
  Domain                Finding                       Measurable Potential
  --------------------- --------------------- ----------------------------
  🛒 Procurement        Missed volume                        **EUR 7,200**
                        discount              

  ☁️ IT / Cloud         Low-utilization test      **Up to EUR 6,000/year**
                        VM                    

  🌱 Energy             Energy-efficiency          **3,000 kWh / EUR 600**
                        anomaly               

  🛡️ Procurement        Authorized expedited      **Rejected --- No Leak**
  exception             surcharge             

  🛡️ IT exception       Critical Disaster         **Rejected --- No Leak**
                        Recovery VM           
  ------------------------------------------------------------------------

> ValueLeak AI is designed not only to **find value**, but also to
> explain when an apparent opportunity **is not actually a leak**.

------------------------------------------------------------------------

# 🏗️ Microsoft Foundry Architecture

The hackathon implementation uses:

-   **Microsoft Foundry Project**
-   **GPT-5.4 deployment**
-   **Persistent Foundry Agents**
-   **Azure AI Search**
-   **Application Insights**
-   **Log Analytics**
-   **OpenTelemetry / Foundry tracing**
-   **Python FunctionTools**
-   **Deterministic business calculations**

The implementation deliberately separates:

``` text
LLM reasoning
     +
Deterministic tools
     +
Grounded enterprise knowledge
     +
Human decision
```

------------------------------------------------------------------------

# 📚 Grounding with Azure AI Search

The Policy Agent uses RAG over synthetic enterprise knowledge:

``` text
supplier_contracts.md
finops_policy.md
energy_guidelines.md
```

Knowledge is indexed in Azure AI Search.

The Policy Agent is instructed to:

-   retrieve relevant knowledge;
-   use retrieved rules only;
-   cite the source;
-   check exceptions;
-   avoid inventing business policy.

This is what allows ValueLeak AI to distinguish **anomaly** from
**actionable value leakage**.

------------------------------------------------------------------------

# 🧮 Deterministic Tools

Business facts and calculations are handled through Python tools.

### Procurement

``` text
get_purchase_order
get_invoice
calculate_cumulative_quantity
calculate_discount_value
```

### IT / Cloud

``` text
get_cloud_resource
get_cloud_usage
get_resource_evidence
check_low_utilization
calculate_annual_cost
```

### Energy

``` text
get_energy_data
calculate_kwh_per_unit
detect_energy_deviation
calculate_energy_impact
```

This keeps critical calculations reproducible and auditable.

------------------------------------------------------------------------

# 👤 Human-in-the-Loop

ValueLeak AI is **advisory by design**.

It does not automatically:

-   stop cloud resources;
-   modify supplier invoices;
-   execute financial transactions;
-   change production equipment.

Actionable findings include:

``` text
human_validation_required = true
```

The responsible business owner decides whether the recommendation should
be accepted or rejected.

------------------------------------------------------------------------

# 🔭 Observability

ValueLeak AI uses Microsoft Foundry tracing and Application Insights.

The implementation provides visibility into:

-   agent invocation;
-   model execution;
-   tool calls;
-   tool results;
-   latency;
-   token usage;
-   workflow execution.

This makes the agentic workflow inspectable rather than a black box.

------------------------------------------------------------------------

# 🧪 Evaluation

A dedicated evaluation dataset contains:

``` text
30 cases
├── 10 Procurement
├── 10 IT / Cloud
└── 10 Energy
```

The Scout Agent was evaluated in Microsoft Foundry.

Validated results:

  Evaluator                 Result
  ----------- --------------------
  Coherence     **100% --- 30/30**
  Fluency       **100% --- 30/30**

The evaluation cycle was also used to improve the Scout prompt so that
it always returns a non-empty structured response.

------------------------------------------------------------------------

# 🔄 Production Workflow

The validated SDK workflow is:

``` text
Business Data
     ↓
Scout
     ↓
Investigator
     ↓
Policy / Azure AI Search
     ↓
Value
     ↓
ValueLeak Report
     ↓
Human Validation
```

The same workflow was executed for:

``` text
procurement
it
energy
all
```

The `all` mode demonstrates that the same agentic architecture can be
reused across multiple business domains.

------------------------------------------------------------------------

# 🖥️ Foundry Visual Workflow

The same architecture was also modeled in the Microsoft Foundry Workflow
designer:

``` text
Start
  ↓
valueleak-scout-agent
  ↓
valueleak-investigator-agent
  ↓
valueleak-policy-agent
  ↓
valueleak-value-agent
  ↓
End
```

Workflow variables connect the agent outputs:

``` text
scout_output
     ↓
investigator_output
     ↓
policy_output
     ↓
value_output
```

Foundry Preview successfully invoked the deployed Scout Agent and the
execution was visible in Foundry traces.

The ValueLeak deterministic tools are currently implemented as local
Python `FunctionTool` handlers. Full end-to-end execution therefore uses
the Python SDK runtime, which executes each requested function and
returns its `FunctionCallOutput` to the agent.

For a production-hosted version, these business tools can be exposed
through supported hosted or remote tool mechanisms.

------------------------------------------------------------------------

# 🧩 Hackathon Challenges

The project follows the Microsoft Factory challenge progression.

  ---------------------------------------------------------------------------
  \#              Challenge       ValueLeak                  Status
                                  Implementation    
  --------------- --------------- ----------------- -------------------------
  0               **Setup**       Deploy Foundry,              ✅
                                  GPT-5.4, AI       
                                  Search, App       
                                  Insights and Log  
                                  Analytics         

  1               **Build         Scout +                      ✅
                  Agents**        Investigator +    
                                  Policy + Value    

  2               **Monitor**     Foundry /                    ✅
                                  OpenTelemetry     
                                  tracing           

  3               **Evaluate**    30-case                      ✅
                                  systematic Scout  
                                  evaluation        

  4               **Production    Multi-agent SDK              ✅
                  Workflow**      orchestration +   
                                  Foundry visual    
                                  workflow          
  ---------------------------------------------------------------------------

------------------------------------------------------------------------

# 🧭 Why the Challenges Are in This Order

### Build first

A value-leak detector without grounded tools could produce convincing
but unsupported savings claims.

The deterministic domain tools ensure that agents reason from actual
supplied business records.

### Then monitor

A correct-looking final answer is not enough.

Tracing lets us verify whether an agent actually called the expected
tool, which model executed, and how the workflow behaved.

### Then evaluate

Tracing proves that the system ran.

Evaluation measures whether it behaved consistently across repeatable
test cases and provides a regression baseline for prompt or model
changes.

### Then orchestrate

The final workflow connects detection, investigation, policy
verification, and quantification into a reusable multi-agent business
process.

This progression follows the same Build → Monitor → Evaluate → Deploy
logic as the Microsoft Factory scenario.

------------------------------------------------------------------------

# 📁 Repository Structure

``` text
valueleak/
│
├── challenge-0-setup/
│   └── Foundry infrastructure deployment
│
├── challenge-1-agents/
│   ├── agents.py
│   └── tools/
│       ├── procurement_tools.py
│       ├── it_tools.py
│       └── energy_tools.py
│
├── challenge-2-monitor/
│   └── monitor.py
│
├── challenge-3-evaluate/
│   └── eval_portal.jsonl
│
├── challenge-4-workflow/
│   └── deploy_challenge4_toolloop_fixed.py
│
└── data/
    ├── procurement/
    ├── it/
    ├── energy/
    └── knowledge/
```

Each challenge contains its own README with implementation and
validation details.

------------------------------------------------------------------------

# 🚀 From Hackathon to Production

ValueLeak AI is designed as a reusable **value-discovery asset**, not a
one-off scenario.

### 1. Connect Real Enterprise Data

Replace synthetic CSV sources with governed enterprise connectors such
as:

``` text
ERP / Procurement
Cloud Cost Management
FinOps platforms
Fabric / Data platforms
Industrial / Energy systems
```

### 2. Host Business Tools

Move local Python FunctionTools behind managed APIs or supported hosted
tool endpoints so the full workflow can execute independently of a
developer machine.

### 3. Discover Multiple Opportunities

Evolve the Scout from a single-case path to:

``` text
Scout
  ↓
[candidate 1, candidate 2, candidate 3, ...]
  ↓
parallel / iterative investigation
  ↓
portfolio of opportunities
```

### 4. Add Confidence and Risk

Rank opportunities using:

``` text
Potential value
× Confidence
× Cost of change
× Operational risk
```

### 5. Integrate Evaluation into CI/CD

Run regression evaluations whenever:

-   prompts change;
-   tools change;
-   knowledge changes;
-   models are upgraded.

### 6. Build the Value Discovery Dashboard

Surface findings as business opportunities:

``` text
VALUE OPPORTUNITY

Domain: IT / Cloud
Resource: VM-TEST-03

Potential value
EUR 6,000/year

Evidence
✓ EUR 500/month
✓ CPU 0.8%
✓ 12 requests/month
✓ Policy checked

Recommendation
Review resource for optimization.

[ REJECT ]   [ VALIDATE ]
```

------------------------------------------------------------------------

# 🌍 Beyond Cost Savings

The same architecture can expand beyond direct financial leakage.

``` text
Phase 1 — Find the Value
Procurement + IT / Cloud

Phase 2 — Expand the Value
Energy + Sustainability

Phase 3 — Scale the Asset
Additional enterprise domains
```

The core pattern remains:

> **Detect → Investigate → Verify → Quantify → Human Decision**

------------------------------------------------------------------------

# 🏆 Hackathon Takeaway

ValueLeak AI demonstrates that agentic AI can do more than answer
questions.

It can **proactively discover business value**.

The system combines:

-   specialized agents;
-   deterministic tools;
-   enterprise RAG;
-   policy-aware reasoning;
-   false-positive prevention;
-   measurable impact;
-   observability;
-   evaluation;
-   human governance.

And it does so with a reusable architecture that can expand across
enterprise domains.

------------------------------------------------------------------------

## 💰 ValueLeak AI

### **Turn Hidden Waste into Measurable Value.**
