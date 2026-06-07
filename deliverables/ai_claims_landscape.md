# AI-Native Companies in Healthcare Claims — Landscape

*Compiled June 2026. Scope: US-centric, companies built **AI-first** (legacy RCM incumbents such as Optum, R1, and Waystar are excluded). "AI-native" is a spectrum; funding, clients, and positioning are point-in-time and shift monthly.*

**Legend — *Managed services?***: **Yes** = runs the process for the client (managed / BPaaS, often outcome- or transaction-priced) · **Hybrid** = both a software option and a managed/delegated option · **No** = software/platform the client operates. *Clients listed are publicly disclosed; "not public" = customers exist but names aren't disclosed.*

> ⭐ = most relevant to an intake/referral + payer-call use case.

## 1 · Claims intake, referral & payer-call automation
- ⭐ **Tennr** — AI for the patient referral/intake front office: document intake + voice AI that auto-calls payers for benefits, follow-up, confirmations. ~10M docs/mo; $101M Series C (~$605M valuation).
  - *Managed services:* **No** — software/orchestration platform the client operates.
  - *Clients:* DME suppliers, home-health agencies, infusion centers, specialty pharmacies, imaging centers (high-volume treatment providers).
- ⭐ **Infinitus** — purpose-built voice AI for payer-facing work: eligibility, prior auth, claim status, EOB retrieval, appeals, phone submissions. 150+ data points/call.
  - *Managed services:* **No** — voice-AI automation platform (the AI performs calls, sold as software).
  - *Clients:* health systems, pharma manufacturers, and payers (specific names not public).

## 2 · Autonomous medical coding (charts → claims)
- **Fathom** — autonomous coding for high-volume specialties (ED, radiology, primary care, surgery). #1 "Reducing the Cost of Care," 2025 KLAS.
  - *Managed services:* **Yes** — coding delivered as an outcome (autonomous coding service, ~90% of charts).
  - *Clients:* health systems & large physician groups (KLAS-recognized; specific names largely not public).
- **CodaMetrix** — autonomous coding for hospitals/health systems; CMX CARE uses the longitudinal patient record for context.
  - *Managed services:* **Yes** — SaaS-delivered autonomous coding (works in parallel with coding teams).
  - *Clients:* 30+ leading US health systems incl. **Mass General Brigham** (radiology: ~58.7% fewer coding denials).
- **Nym Health** — semantic "clinical language" autonomous coder; strong ED product; Epic Showroom "Fully Autonomous Coding."
  - *Managed services:* **Yes** — autonomous coding engine delivering coded output.
  - *Clients:* 21 provider customers incl. **Geisinger** and **Ochsner Health**.
- **Arintra** — charts → claims at ~96% accuracy; ~43% fewer coding denials, ~11% less undercoding.
  - *Managed services:* **Yes** — autonomous coding (zero-touch).
  - *Clients:* health systems & large physician groups (names not public).
- **RapidClaims · MediCodio · Maverick Medical AI** — newer AI-native coding/claims-automation entrants.
  - *Managed services:* **Hybrid** — coding software with services options.
  - *Clients:* provider groups / RCM teams (names not public).

## 3 · Provider RCM, claims automation & denials
- **Candid Health** — full medical-claims-lifecycle automation; >95% touchless claims reported.
  - *Managed services:* **No** — RCM software platform.
  - *Clients:* 200+ healthcare orgs, weighted to digital-health and specialty practices.
- **Adonis** — AI orchestration + agents for RCM/denials; $40M Series C (’26), >$95M total.
  - *Managed services:* **No** — software/agents the client's RCM team runs (integrates w/ Epic, athenahealth, etc.).
  - *Clients:* **Baptist Health South Florida, ApolloMD, Bicycle Health, Fox Valley Orthopedics**; ~20,000 providers.
- **AKASA** — generative AI across the revenue cycle (prior auth → CDI → coding → claims), trained on each system's own data.
  - *Managed services:* **No** — software for in-house RCM staff.
  - *Clients:* **Cleveland Clinic**; Oracle/Cerner partnership.
- **Sohar Health** — API-first front-end RCM (eligibility + claim accuracy), ~95% automation.
  - *Managed services:* **No** — API/software.
  - *Clients:* digital-health and behavioral-health providers (names largely not public).
- **Syntra · Taiga · LunaBill** — billing/claims for private practices; LunaBill = voice AI for billing follow-up calls.
  - *Managed services:* **Yes** for Syntra/Taiga (outsourced billing run for practices); **No** for LunaBill (tool).
  - *Clients:* independent/private physician practices.
- **Aegis** — automates insurance denial appeals end-to-end for providers.
  - *Managed services:* **Yes** — runs the appeal process (intake → resolution).
  - *Clients:* healthcare providers (names not public).

## 4 · Prior authorization
- **Cohere Health** — market leader; ~47M payer-provider interactions/yr, 85% real-time approvals; ~$200M raised; expanding into payment integrity.
  - *Managed services:* **Hybrid** — in-house software + **delegated, end-to-end managed** option (Cohere Complete™).
  - *Clients:* **Humana** (national MA + Commercial), **Geisinger Health Plan**, **CMS**; ~660K providers on platform.
- **Anterior** (formerly Co:Helm) — AI for health plans: prior auth, payment integrity, risk adjustment; $40M raised.
  - *Managed services:* **No / unconfirmed** — automation for payer back office.
  - *Clients:* **Geisinger Health Plan** (disclosed); other plans not public.

## 5 · Payer-side: payment integrity & claims adjudication
- **Machinify** — unified pre-pay + post-pay payment-integrity platform across the claim lifecycle.
  - *Managed services:* **Hybrid** — platform plus payment-integrity/recovery services (typical for the category; model not fully public).
  - *Clients:* national/regional health plans (names not public).
- **Anomaly (Anomaly Insights)** — AI payer-intelligence for denials/underpayments/adjudication deviations; +$17M (’26).
  - *Managed services:* **No** — software/intelligence platform.
  - *Clients:* 20+ health systems, plus diagnostic labs and outsourced-RCM firms.
- **Alaffia Health** — AI + expert clinicians for end-to-end claims ops (UM, payment integrity, appeals); $55M Series B (Feb ’26).
  - *Managed services:* **Yes** — offers **both** software subscriptions **and managed services**; runs bill/chart reviews on plans' behalf.
  - *Clients:* Medicaid, Medicare Advantage & commercial health plans (up to ~2M members), TPAs, cost-containment firms, gov agencies.
- **Curacel · Amera** — AI claims processing/automation for payers & TPAs; Amera structures messy PDF/EDI/non-standard claim inputs.
  - *Managed services:* **No** — claims infrastructure/software.
  - *Clients:* payers, TPAs, and providers (Curacel strong in emerging markets); specific names not public.

## 6 · Consumer / patient-side denial appeals
- **Counterforce Health** — free AI appeal-letter generator; ~70% appeal success; copies state regulators on filings.
  - *Managed services:* **Yes** (service performed for the patient; free to individuals).
  - *Clients:* individual patients/consumers.
- **Claimable** — AI-generated appeals (~$40/letter); signing deals with drugmakers & health systems to appeal on patients' behalf.
  - *Managed services:* **Yes** (appeals run on the patient's behalf).
  - *Clients:* individual patients; plus drugmaker and health-system partnerships.

---

## Sources
- Tennr ($101M / customers): https://www.fiercehealthcare.com/health-tech/tennr-clinches-101m-build-out-ai-automates-patient-referral-workflows · https://www.tennr.com/about
- Infinitus: https://www.infinitus.ai/solutions/benefit-verification/
- Fathom: https://fathomhealth.com/services · CodaMetrix (MGB / 30+ systems): https://www.codametrix.com/
- Nym (Geisinger, Ochsner; 21 customers): https://medcitynews.com/2024/10/automation-medical-coding-healthcare/
- Coding roundup: https://www.rapidclaims.ai/blogs/top-ai-medical-coding-solutions
- Cohere (Humana, Geisinger, CMS; Cohere Complete): https://www.coherehealth.com/payment-integrity · https://www.coherehealth.com/news/cohere-health-announces-national-expansion-of-humana-partnership
- Anterior ($40M, Geisinger): https://www.fiercehealthcare.com/ai-and-machine-learning/payer-ai-company-anterior-banks-40m-funding-round
- Adonis (Baptist Health, ApolloMD, Bicycle Health): https://hitconsultant.net/2026/03/25/adonis-40m-series-c-funding-ai-revenue-cycle-management-claim-denials/
- AKASA (Cleveland Clinic): https://akasa.com/
- Candid Health: https://candidhealth.com/
- Anomaly (+$17M; 20+ systems): https://hitconsultant.net/2026/05/13/anomaly-insights-funding-payer-intelligence-ai/
- Alaffia ($55M; software + managed services): https://hlth.com/insights/news/alaffia-health-raises-55m-series-b-to-expand-ai-driven-claims-operations-2026-02-04
- Machinify: https://www.machinify.com/resources/how-machinifys-ai-platform-is-rewriting-the-rules-of-payer-ops/
- Counterforce / Claimable (Bloomberg): https://www.bloomberg.com/news/features/2026-04-22/ai-and-mark-cuban-among-startup-s-tools-to-fight-denied-health-care-claims
