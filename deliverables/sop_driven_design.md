# SOP-Driven Processing — Design (Horizon 2)
*Coastal DME / Live Intake & Referral Agent — for technology-leader review*

## 1. Objective
Make the **ingested SOP the actual source of the agent's decision rules** — gap criteria, coding-authority reasoning, confidence/jurisdiction thresholds, escalation triggers — so a referral's outcome genuinely changes with the SOP. The **Intelligence Layer (Step 03)** then shows the *real* SOP rules in effect, the LLM's actual reasoning on inconsistencies, and the CMS/knowledge-graph checks that fired. **Code-review-grade real — no mapping facade, no fabricated data.**

## 2. Current state (honest baseline)
**Already real:**
- PDF ingestion + field extraction — LLM (`intake_agent.extract_fields`, Claude Sonnet via `_call_claude`).
- ICD-conflict detection & resolution — LLM during extraction (returns `icd_conflict`, detail, confidence).
- Knowledge-graph validation — deterministic CMS rules (`knowledge_graph.validate` over `rules.json`, 24 ICD-10/LCD-cited rules), returns fired rules + citations.
- Confidence scoring, jurisdiction/SLA, gap detection.

**Not yet real (what this design fixes):**
- SOP rules are **evaluated/labeled against** decisions (`demo_server._sop_trace`) but don't **drive** them.
- Decision thresholds are **hardcoded**: `intake_agent.HARD_BLOCKS`, the 80% confidence cut in `policy.confidence_tier`, `policy.JURISDICTION_SLA`.
- The featured **Holloway `icd_conflicts` are seeded (fabricated)** in `demo_server.process_referral` — must be removed.

## 3. SOP rule schema (typed, enforceable)
`/api/ingest-sop` will have the LLM emit **typed, executable rule specs** (not prose). Persisted to `output/active_sop_rules.json`.

```
[
  {"id":"sop-2.1","clause":"2.1","type":"required_field","field":"auth_ref",
   "severity":"hard_block","citation":"SOP §2.1","source":"client_sop"},
  {"id":"sop-3.4","clause":"3.4","type":"coding_authority",
   "priority_order":["clinical_notes","prescription","referral_form"],
   "citation":"ICD-10-CM §I.B.13"},
  {"id":"sop-6.1","clause":"6.1","type":"confidence_gate","auto_min":90,"spotcheck_min":80,
   "citation":"SOP §6.1"},
  {"id":"sop-5.2","clause":"5.2","type":"jurisdiction_sla","state":"TX","business_days":2,
   "citation":"State WC fee schedule"},
  {"id":"sop-4.2","clause":"4.2","type":"coverage_check","applies_to":"dme",
   "ruleset":"CMS_LCD","citation":"CMS LCD L33803"},
  {"id":"sop-8.0","clause":"8.0","type":"escalation",
   "on":["split_evidence","laterality_conflict"],"action":"human_review","citation":"SOP §8.0"}
]
```
Validation/normalization on ingest; documented default set used **only** when no SOP is ingested (clearly labeled, not silent).

## 4. Architecture & data flow
1. **Ingest** — `/api/ingest-sop` → LLM → typed rules → persist (real).
2. **Load** — NEW `sop_rules.py`: `get_active_rules()` + typed accessors `required_fields()`, `confidence_thresholds()`, `jurisdiction_sla(state)`, `coding_authority_order()`, `escalation_triggers()`, `coverage_rulesets()`.
3. **`process_referral` consumes them:**
   - `extract_fields(docs, claim, coding_authority_order)` — the SOP's coding-authority order is injected into the LLM prompt, so inconsistency resolution **follows the SOP**; returns the resolved code + **reasoning text** + governing clause.
   - `check_completeness(fields, required_rules)` — required / hard-block fields come **from the SOP**.
   - `knowledge_graph.validate(fields)` — real CMS checks; `coverage_check` rules select which rulesets apply; panel shows fired rules + citations.
   - `policy.confidence_tier(conf, thresholds)` and jurisdiction SLA — thresholds **from the SOP**.
   - escalation — triggered by the SOP's `escalation` rule.
4. **Record real decisions** — each decision stored as `{decision, value, sop_rule_id, clause, citation, reasoning}` on the episode (replaces the `_sop_trace` mapping).
5. **Intelligence panel (Step 03)** renders that real per-episode record: SOP rules in effect · LLM inconsistency reasoning · CMS rules fired (citations) · confidence · decision — each tied to its clause.

## 5. File-by-file changes
- **`sop_rules.py` (NEW)** — load `active_sop_rules.json`; typed accessors; documented defaults.
- **`intake_agent.py`** — `extract_fields(..., coding_authority_order=None)`: include the SOP coding rule in the prompt; return structured conflict reasoning. `check_completeness(fields, required_rules=None)`: derive hard-block/required from SOP (param), default-fallback preserved (backward compatible).
- **`policy.py`** — `confidence_tier(conf, thresholds=None)`, `assess_jurisdiction(fields, sla_map=None)` accept SOP-derived params.
- **`knowledge_graph.py`** — unchanged core (real); optionally filter rulesets by `coverage_check`. Panel already gets `fired_rules` + citations.
- **`demo_server.py`** — upgrade `/api/ingest-sop` prompt to the typed schema; in `process_referral` load `sop_rules` and pass them through; build the real `sop_decisions` record; **delete the Holloway `icd_conflicts` seed**; `_sop_trace` reads the real record.
- **`pipeline.html`** — Step 03 Intelligence Layer + "SOPs Applied" render the real `sop_decisions` (rule + reasoning + KG checks + citation).
- **`sops.html`** — display the typed rules (already shows generated rules).

## 6. Honesty / code-review fixes (mandatory)
- **Remove** the fabricated Holloway `icd_conflicts` seed → use real LLM-extracted conflicts.
- **Citations come from the matched rule**, not hardcoded "§2.1" strings.
- **Thresholds/SLAs come from the SOP**, not constants.
- **Fallback is explicit & documented** — default rules only when no SOP is ingested.

## 7. Phased plan + acceptance criteria
| Phase | Deliverable | Acceptance |
|---|---|---|
| **P1** | `sop_rules.py` + typed-rule ingestion | Ingest → typed rules persisted; accessors return them |
| **P2** | Wire `check_completeness` / confidence / jurisdiction to SOP | Editing a SOP threshold changes the episode outcome |
| **P3** | Coding-authority LLM reasoning driven by SOP | Conflict resolution follows the SOP order; reasoning surfaced |
| **P4** | Intelligence panel renders real `sop_decisions` | Panel shows real SOP rules + reasoning + CMS checks per episode |
| **P5** | Remove seed; end-to-end verify on real referrals | No fabricated data; trace = real decisions, traced to clause+citation |

## 8. Risks & mitigations
- **LLM rule-extraction variability** → strict schema validation + normalization; cache; documented defaults.
- **Signature changes** (`check_completeness`, `extract_fields`) → keep backward-compatible optional params.
- **Demo richness without the seed** → use a genuinely conflict-rich real referral as the featured case (verify which of the 40/75 actually has a multi-doc ICD conflict).
- **Latency** → coding rule is added to the *existing* extraction prompt (no extra LLM call).

## 9. What a technology leader will see in the code
SOP document → typed rules (`active_sop_rules.json`) → `sop_rules.py` accessors → `process_referral` reads them → `extract_fields` reasons per the SOP coding rule → `knowledge_graph.validate` runs the real CMS rules → decisions recorded with clause + citation + reasoning → Intelligence panel renders it. **One real path, no mapping layer, no seeded data.**
