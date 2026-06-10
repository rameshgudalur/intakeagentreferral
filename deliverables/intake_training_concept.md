# Experiential Intake Training — "Coached Intake Simulator"

*Concept note · "Intaketraining" workstream · June 2026*

> **Train associates to expert level *before* automation — using the same AI that will later automate the routine work — with hands-on simulation instead of desktop SOP reading.**

## The problem with legacy training
DME/claims intake is still taught the old way: read the SOP deck, watch a few examples, then shadow a senior associate for weeks. It's **passive**, it **doesn't expose people to real variability or edge cases**, there's **no feedback loop**, competency **can't be measured**, and ramp time is long. People learn the rule, not the judgment.

## The idea
The production intake agent already knows the right answer for any referral — it extracts the fields, resolves ICD conflicts, applies 24 cited CMS rules, and decides route-vs-escalate. **Flip it into a coach.** A trainee does the *real task* on a realistic case; the agent **grades and explains instantly, citing the exact rule.**

**The loop:** realistic referral packet → trainee extracts ICD / spots conflict / flags gaps / decides route-or-escalate → agent grades each decision and coaches with the CMS citation → difficulty ramps → competency is scored and certified.

## What makes it experiential (not a slide deck)
- **Do, don't read** — work real packets, make the real decisions.
- **Curveballs injected** — seeded ICD miscodes, missing auth, laterality, bariatric edge cases — like a flight sim throwing failures.
- **Instant, cited coaching** — every case ends with *why*, tied to the rule (e.g., *"post-surgical → S-code not M-code, §I.C.19.a"*).
- **Judgment reps** — explicitly trains *when to escalate vs. decide* — the exact judgment automation leaves to humans.
- **Gamified & measured** — scoring, levels, a certification gate before live work; manager dashboards on accuracy and error patterns.

## Why it beats legacy SOP training
| Legacy desktop SOP | Coached simulation |
|---|---|
| Passive reading | Active doing on real cases |
| No feedback | Instant, cited coaching every case |
| Generic rules | Learn from variability + edge cases |
| Weeks of shadowing | Days to competency |
| Can't measure readiness | Scored, certified, data-driven |

## Strategic payoff
- **A bridge to automation, not separate from it** — the same engine that coaches humans now automates the routine cases later. One asset, two uses.
- **De-risks change management** — associates coached *by* the AI trust it and understand it; reframes "AI is replacing me" into "AI made me an expert faster." The #1 adoption blocker, addressed.
- **Raises the human-in-the-loop quality floor** — after automation, humans handle the hard escalations, so you want them expert. Upskilling, not deskilling.
- **Differentiator** — pairing *"we'll automate your intake"* with *"and we'll make your people experts first, using the same AI"* is a story competitors don't tell.

## Feasibility — it's already prototyped
A working **Coached Intake Simulator** is live in the demo (`/panel/training`): three curated cases (post-surgical miscode, missing authorization, the bariatric trap), the trainee submits ICD / conflict / gaps / decision, and the agent grades each dimension with cited coaching. It reuses what already exists — referral generators (unlimited cases + ground truth), the agent's KG citations (the coach), the escalation logic (judgment), and the observability layer (competency dashboards).

**Next steps:** expand the case bank by difficulty tier · add scoring/leaderboard + certification gate · add a manager competency dashboard · optionally a simulated inbound voice case. A great hands-on **station for the June 10 workshop**.
