"""Generate the external-facing POC walkthrough as a Word document."""
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

NAVY = RGBColor(0x1E, 0x3A, 0x5F)
BLUE = RGBColor(0x25, 0x63, 0xEB)
GRAY = RGBColor(0x47, 0x55, 0x69)
GREEN = RGBColor(0x15, 0x80, 0x3D)

doc = Document()

# Base font
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

def heading(text, size=15, color=NAVY, space_before=14, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = color
    return p

def label_say(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    lab = p.add_run("Say:  ")
    lab.bold = True
    lab.font.color.rgb = BLUE
    r = p.add_run("“" + text + "”")
    r.italic = True
    return p

def label_screen(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    lab = p.add_run("On screen:  ")
    lab.bold = True
    lab.font.color.rgb = GRAY
    p.add_run(text)
    return p

def key(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.space_after = Pt(8)
    lab = p.add_run("Key message:  ")
    lab.bold = True
    lab.font.color.rgb = GREEN
    r = p.add_run(text)
    return p

def body(text, space_after=8):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.add_run(text)
    return p

# ── Title ──
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.LEFT
r = t.add_run("Intake Agent — Live Demonstration Walkthrough")
r.bold = True
r.font.size = Pt(22)
r.font.color.rgb = NAVY
sub = doc.add_paragraph()
rs = sub.add_run("A guided walkthrough of the working intake agent, on real referral packages.")
rs.italic = True
rs.font.size = Pt(12)
rs.font.color.rgb = GRAY
doc.add_paragraph().add_run("—" * 30).font.color.rgb = RGBColor(0xCB,0xD5,0xE1)

# ── Intro ──
heading("Before you begin", 13)
body("This guide walks an audience through the intake agent end to end — from a stack of "
     "referral documents to a complete, routed, fully auditable record. It is a working proof of "
     "concept running on real referral packages, not a slide presentation. Read the lines aloud as "
     "written, or in your own words; the goal is to let the system show its work at every step.")
body("Allow roughly 25–30 minutes for the walkthrough, with time for questions at the end.")

# ── 1 ──
heading("1.  Opening — the problem in one breath")
label_say("Every referral that arrives today is a person reading three or four documents — a "
          "referral form, clinical notes, a prescription — pulling out the key fields by hand, "
          "spotting what’s missing, and chasing the case manager for the rest. It’s accurate "
          "when people are fresh, and slower when they’re buried. What you’re about to see is "
          "an agent doing that same intake work end to end, on real referral packages, and showing "
          "its reasoning at every step.")
key("We are not replacing judgment. We are removing the manual reading and the chasing, and making "
    "every decision traceable.")

# ── 2 ──
heading("2.  The starting point — what the system covers")
label_screen("The launch hub, with its set of capability cards.")
label_say("Everything launches from one place. The centerpiece is the live intake agent. Around it "
          "sit live operational metrics, an analytics layer, a scale-and-cost view, and a training "
          "module for new associates. We’ll spend most of our time in the live agent and come "
          "back to the rest.")

# ── 3 ──
heading("3.  Live processing — watch it work")
label_screen("A queue of incoming referrals processing in real time.")
label_say("These are real referral packages going through the agent right now. For each one it reads "
          "every page, extracts the fields, checks them against a rules engine, scores its own "
          "confidence, and decides: route it, or flag a gap. Watch the rows resolve — patient, "
          "equipment, priority, missing items — with no manual data entry.")
key("Outreach is drafted, never blind-sent — a person still approves anything that leaves the building.")
body("As the queue runs, point out one referral you’ll open in detail, and say you’ll go in "
     "while the others finish.", space_after=10)

# ── 4 ──
heading("4.  Inside one referral — the “is it real?” moment")
label_screen("The full step-by-step pipeline for a single referral.")
body("Walk the steps from the top.")
label_say("Three source documents. The agent pulled every field and tells you exactly where each "
          "value came from. Nothing is invented — if it isn’t in the documents, it’s a "
          "gap, not a guess.")
label_say("Extraction alone isn’t trust. Every field is then checked against a rules engine built "
          "on published clinical and coverage rules, each one cited. This is the difference between "
          "‘the AI said so’ and ‘the rule says so, and here’s the citation.’")
label_say("Here’s where it gets honest. The three documents disagree on diagnosis codes. The "
          "agent resolves the ones it’s confident about — but on one of them the evidence is "
          "split, its confidence drops below the threshold, and it stops. It does not guess. It "
          "escalates to a human, with its reasoning attached.")
key("The restraint is the feature. The agent knows what it doesn’t know, and escalates instead "
    "of guessing.")
label_say("It also reads the jurisdiction and applies the right turnaround clock — some states "
          "carry a tighter service-level deadline, and the agent prioritizes accordingly.")

# ── 5 ──
heading("5.  Reaching out — email, then a live phone call")
label_screen("The outreach step, where the agent contacts the case manager for the missing items.")
label_say("For the missing items, the agent first drafts an email to the case manager, ready for a "
          "person to approve and send. When email goes unanswered, it picks up the phone.")
body("At this point the agent places a live outbound call to collect the outstanding details. "
     "Put the call on speaker so the audience can hear it.")
label_say("Listen for a few things: it reads the claim number clearly, it confirms the physician’s "
          "identifier is complete, it repeats each item back to me — and then it thanks me and "
          "closes the call properly. No awkward silences, no abrupt hang-up.")
label_say("And now — only once the call has actually gone out — the transcript appears, "
          "logged automatically against this referral.")

# ── 6 ──
heading("6.  The complete record — and the audit trail")
label_screen("The final referral record, then the audit trail for the same referral.")
label_say("Every field populated, every gap resolved — by email, by phone, or by the agent’s "
          "own correction. The moment this record locks, it’s ready to dispatch.")
label_say("And this is the part the compliance and technology leads care about. For any referral you "
          "get the full trace: what the agent read, which rules fired and their citations, its "
          "confidence at each decision, the jurisdiction logic, and every outreach action taken.")
key("Defensibility is one click, not an investigation.")

# ── 7 ──
heading("7.  Intake by fax — live")
label_screen("The incoming-fax panel, showing the live intake fax number.")
label_say("Intake doesn’t only come from a neat queue — a great deal of it still arrives by "
          "fax. This is our live intake line. Fax a referral package — the three documents "
          "together — to this number, and it lands in the processing queue automatically; the "
          "agent begins working on it within about thirty seconds.")
body("You can demonstrate this live by faxing a package to the number on screen and watching a new "
     "row appear at the top of the queue, or use the on-screen sample to show the same flow.")

# ── 8 ──
heading("8.  Scale and cost — the honest version")
label_screen("The scale-and-cost view, with adjustable inputs.")
label_say("The question every leader asks: does this hold up at volume, and what does it cost? "
          "Here’s the honest answer — and you can change the inputs yourself.")
body("Walk the three scenarios: today’s standard configuration; a scaled, real-time "
     "configuration that processes roughly ten thousand referrals in about seven minutes; and an "
     "asynchronous batch mode at roughly half the per-referral cost for non-urgent volume.")
key("Cost is a few cents per referral, measured on the actual run — not estimated — and the "
    "numbers move the moment you change the inputs. We add capacity; there is no hidden cap.")

# ── 9 ──
heading("9.  The broader layer (optional)")
label_screen("Live metrics, analytics, and the training module.")
label_say("The agent is one layer. Around it you get live observability, an analytics view of trends "
          "like escalation and auto-routing rates, and a path to bring your associates along — "
          "so this augments your team rather than becoming a black box.")

# ── 10 ──
heading("10.  Closing")
label_say("What you’ve seen is a working proof of concept on real referral packages. It reads, it "
          "validates against cited rules, it knows its own confidence, it escalates instead of "
          "guessing, it reaches out by email and by phone, it takes in faxes live, and it logs every "
          "step for audit. The next step isn’t ‘will it work’ — you’ve just "
          "watched it. The next step is to run it on a sample of your own intake packages, with no "
          "integration and nothing sensitive shared, so we start from your data.")

# ── cheat sheet ──
heading("Quick reference — lines to land", 13)
data = [
    ("Why it’s credible", "It shows its work at every step."),
    ("The escalation moment", "The agent does not guess — that restraint is the feature."),
    ("For compliance", "Defensibility is one click, not an investigation."),
    ("The phone call", "It reads clearly, confirms each item, thanks the caller, and closes — no dead air."),
    ("On cost", "A few cents per referral, measured — and the numbers move when you move the inputs."),
    ("On scale", "We add capacity, not magic."),
    ("The close", "The question isn’t ‘will it work.’ You just watched it."),
]
table = doc.add_table(rows=1, cols=2)
table.style = "Light Grid Accent 1"
hdr = table.rows[0].cells
hdr[0].paragraphs[0].add_run("Moment").bold = True
hdr[1].paragraphs[0].add_run("Line to land").bold = True
for moment, line in data:
    cells = table.add_row().cells
    cells[0].text = moment
    cells[1].text = line

# Save to Desktop and deliverables
import os
desktop = Path(os.path.join(os.path.expanduser("~"), "Desktop"))
out1 = desktop / "Intake Agent - Demo Walkthrough.docx"
out2 = Path(__file__).parent / "deliverables" / "poc_walkthrough_external.docx"
doc.save(str(out1))
doc.save(str(out2))
print("Saved:", out1)
print("Saved:", out2)
