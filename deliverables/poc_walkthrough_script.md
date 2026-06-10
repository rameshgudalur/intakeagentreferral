# Intake Agent POC — Live Walkthrough Script

**Audience:** client team (intake lead, ops, compliance/tech lead, exec sponsor)
**Duration:** ~25–30 min live + Q&A
**Presenter:** narrator + SME on standby for clinical/compliance questions
**Public URL:** https://web-production-efe30.up.railway.app  ·  **Password:** (team lead has it)

> Framing word: this is a **POC** — a working proof of concept on real referral
> packages, not a slide deck. Production-track foundation; still needs hardening
> (integrations, security review) before it touches live PHI.

---

## 0 · Pre-flight checklist (do this 10 min before)

- [ ] Open the public URL, log in, land on the **Hub**. Leave it on the Hub.
- [ ] Confirm the latest deploy is live (queue says "referrals ready", fax modal
      shows **+1 (609) 637-1507**, James pipeline shows *his own* conflict log).
- [ ] Phone nearby and charged — you'll receive the **outbound voice call** live.
- [ ] If demoing inbound fax live: have a 3-page referral ready to fax to
      **+1 (609) 637-1507** (referral form + clinical notes + prescription, one transmission).
- [ ] Have a backup ready: the **"Process Sample Fax"** button and the pre-loaded
      queue both work without any external dependency.
- [ ] Browser zoom ~90% so the full queue and pipeline fit on screen.

---

## 1 · Open — the problem, in one breath (60 sec)

**[SAY]**
> "Every referral that comes in today is a person reading three or four PDFs —
> a referral form, clinical notes, a prescription — pulling fields by hand,
> spotting what's missing, and chasing the case manager for the rest. It's
> accurate when people are fresh and slower when they're buried. What you're
> about to see is an agent doing that same intake work end-to-end, on real
> referral packages, and showing its work at every step."

**[KEY POINT]** We're not replacing judgment — we're removing the manual reading
and chasing, and making every decision auditable.

---

## 2 · The Hub — what's in the POC (60 sec)

**[CLICK]** Stay on the Hub. Gesture across the cards.

**[SAY]**
> "One launch point. The centerpiece is the **Live Intake Agent POC**. Around it:
> live operational **metrics**, an **analytics** layer, a **scale & cost**
> calculator, and a **training** module for associates. We'll spend most of our
> time in the live POC and come back to the rest."

**[CLICK]** Open **Launch POC**.

---

## 3 · Live processing — watch it work (4–5 min)

**[CLICK]** Start the run. Let the queue process.

**[SAY] while it runs**
> "These are real referral packages going through the agent right now. For each
> one it's reading every page, extracting the fields, checking them against a
> rules engine, scoring its own confidence, and deciding: route it, or flag a
> gap. Watch the rows resolve — patient, equipment, priority, gaps — with no
> manual entry."

**[KEY POINTS]**
- Each row shows **channel** (fax/voice), **priority**, and **gaps** as they're found.
- Outreach is **drafted**, not blind-sent — a human still approves the send.
- Point out **James Holloway (WC-2026-084431)** — "we'll open this one in detail."

**[SAY] when the hint appears mid-run**
> "Notice the agent surfacing James Holloway as worth a closer look — let's go
> in while the rest finish."

**[CLICK]** Open James Holloway's pipeline (**Open Pipeline →**).

---

## 4 · The pipeline — the "is it real?" moment (6–8 min)

This is the heart of the demo. Walk the 7 steps top to bottom.

**[SAY] — Steps 1–2 (Extraction)**
> "Three source documents. The agent pulled every field and tells you *where*
> each value came from. Nothing is invented — if it's not in the documents,
> it's a gap, not a guess."

**[SAY] — Step 3 (Knowledge Graph validation)**
> "Extraction isn't trust. Every field is checked against a rules engine — CMS-cited
> rules — that fires deterministically. This is the difference between 'the AI
> said so' and 'the rule says so, here's the citation.'"

**[SAY] — ICD Conflict Log (Holloway's own)**
> "Here's where it gets honest. The three documents *disagree* on diagnosis codes.
> The agent resolves the ones it's confident about — and look at conflict three:
> the evidence is split two-to-one, confidence drops to 71%, below our 80%
> threshold. **The agent does not guess.** It escalates to a human, with the
> reasoning attached. That restraint is the feature."

**[KEY POINT for the compliance/tech lead]** Confidence tiers drive autonomy:
high → act, medium → spot-check, low → escalate. The agent knows what it doesn't know.

**[SAY] — Jurisdiction / SLA**
> "It also reads the jurisdiction and applies the turnaround clock — a Texas
> referral carries a tighter SLA than others, and the agent prioritizes accordingly."

**[SAY] — Step 5 (Email outreach)**
> "For the missing items, it drafts the outreach to the case manager — ready for
> a human to approve and send."

---

## 5 · Voice outreach — live call (3–4 min)  ⭐ NEW BEHAVIOR

**[CLICK]** Advance to **Step 6 (Voice Outreach)**. The call auto-triggers.

**[SAY] as the call card shows "placing call now"**
> "When email goes unanswered, the agent picks up the phone. It's calling the
> case manager right now to collect the outstanding items — this is a real
> outbound AI voice call."

**[ACTION]** Your phone rings — **answer it on speaker** and let the team hear it.

**[SAY] before answering]**
> "Listen for a few things: it reads the claim number cleanly, it validates the
> physician NPI is a full ten digits, and it confirms each item back to me — then
> it thanks me and closes properly. No dead air, no abrupt hang-up."

**[ON THE CALL]** Provide the missing items. If you want to show the NPI guard,
give a short number first — the agent will ask you to repeat the full 10-digit NPI.

**[SAY] after the call]**
> "Now — and only now that the call has gone out — the transcript appears below,
> logged automatically against the episode."

**[CLICK]** Show the revealed transcript + the "all fields collected" confirmation.

---

## 6 · Route output + audit trail (2–3 min)

**[CLICK]** Advance to **Step 7 (Route Output)** — show the final episode record.

**[SAY]**
> "Every field populated, every gap resolved — by email, by call, or by the
> agent's own correction. The moment this locks, it's ready to dispatch."

**[CLICK]** Open the **audit trail** for this claim.

**[SAY] (aimed at compliance/tech lead)**
> "This is defensibility. For any episode you get the full trace: what the agent
> read, which rules fired and their citations, the confidence at each decision,
> the jurisdiction logic, and every outreach action. If anyone ever asks 'why did
> the system do that?' — the answer is one click, not an investigation."

---

## 7 · Inbound fax — live, if you want it (2–3 min)  ⭐ NEW

**[CLICK]** Back on the main screen, open **Receive New Fax**.

**[SAY]**
> "Intake doesn't only come from a queue — most of it arrives by fax. Here's our
> live intake line. If you fax a referral package — the three documents together —
> to this number, it lands in the processing queue automatically and the agent
> starts on it within about thirty seconds."

**[ACTION — live option]** Have a client fax 3 docs to **+1 (609) 637-1507**;
watch the new row appear at the top of the queue and process.
**[ACTION — safe option]** Click **Process Sample Fax** to show the same flow
without an external dependency.

---

## 8 · Scale & cost — the honest version (3–4 min)

**[CLICK]** Open the **Scale & Cost calculator** (link on the main screen, or from the Hub).

**[SAY]**
> "The question every exec asks: does this hold up at volume, and what does it
> cost? Here's the honest answer, and you can change the inputs live."

**[WALK THE THREE ROWS]**
- **Standard (20 workers):** today's configuration — steady throughput.
- **Scaled real-time (~500 workers):** ~10,000 referrals in roughly 7 minutes —
  "throughput scales with concurrency; we add workers, not magic."
- **Batch API (~50% cost):** for non-urgent volume, asynchronous at about half the
  per-referral cost.

**[KEY POINT]** Per-referral LLM cost is ~**$0.03** (≈2,500 input + 1,500 output
tokens, measured on the actual POC run — not estimated). Infrastructure scales
with concurrency. **No silent caps — the number moves when you move the inputs.**

---

## 9 · The rest of the layer (90 sec — optional)

**[CLICK]** Quick tour: **Live Metrics** (system health, confidence, rule fires),
**Analytics** (trends, escalation rate, auto-route rate), **Training** (associate
upskilling from SOP-based to experiential).

**[SAY]**
> "The agent is one layer. Around it you get observability, analytics, and a path
> to bring your associates along — so this augments the team, it doesn't black-box them."

---

## 10 · Close (60 sec)

**[SAY]**
> "What you saw is a working POC on real referral packages: it reads, validates
> against cited rules, knows its own confidence, escalates instead of guessing,
> reaches out by email and by voice, ingests faxes live, and logs every step for
> audit. The next step isn't 'will it work' — you just saw it. It's a 48-hour
> proof-of-concept on a sample of *your* intake packages, with no integration and
> no PHI shared, so we start from your data."

**[Q&A]** Hand to SME for clinical/compliance specifics.

---

## Quick reference — talk-track one-liners

| Moment | One line |
|---|---|
| Why it's credible | "It shows its work at every step." |
| ICD escalation | "The agent does not guess — that restraint is the feature." |
| Compliance | "Defensibility is one click, not an investigation." |
| Voice call | "Reads cleanly, validates the NPI, confirms, thanks, and closes — no dead air." |
| Cost | "~3 cents a referral, measured — and the number moves when you move the inputs." |
| Scale | "We add workers, not magic." |
| Close | "The question isn't 'will it work.' You just watched it." |

## If something fails live (recovery lines)
- **Deploy/queue slow:** "It's processing live on a shared instance — give it a beat."
- **Voice call doesn't connect:** "Carrier hiccup — here's the logged transcript
  from a prior run," then continue. (Don't retry more than once on stage.)
- **Live fax doesn't arrive:** switch to **Process Sample Fax** — same pipeline.
- **Anything else:** narrate the intent and move on; the audit trail backs the story.
