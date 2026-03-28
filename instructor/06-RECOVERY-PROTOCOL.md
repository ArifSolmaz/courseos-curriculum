# Recovery Protocol

## Philosophy

Recovery is built into the course design. It is not a penalty — it is a support mechanism. The goal is to prevent silent failure while maintaining standards.

---

## When to trigger recovery

A student enters recovery when ANY of these occur during a session:

1. **Cannot complete must-pass core** by the pre-submit checkpoint (4:35 in CP1/CP2, 2:40 in OOP/DSA)
2. **Universal check fails** and cannot be fixed before end of session
3. **Cannot explain their code** in a 2-minute oral check
4. **Repo is broken** (imports fail, structure wrong, files deleted)

---

## Recovery ticket process

### Student submits (before leaving class)

The ticket has 3 required fields:
1. **What failed** — specific: "clean_data() crashes on row 3 with ValueError"
2. **What I tried** — specific: "I checked the type, tried float(), added try/except"
3. **Next steps** — specific: "I'll re-read W11 exceptions notebook and fix the type check"

### Instructor reviews (same day or next day)

- Add a short note: guidance, a hint, or "see me next week"
- Mark as: `open` → `in_progress` → `resolved`

### Student resolves (before next session)

- Fix the code in their repo
- Push the fix
- Must-pass core must work when the next session starts

---

## Limits

| Situation | Policy |
|-----------|--------|
| 1st–3rd recovery ticket (per semester) | Full weekly credit at core level (70%) if resolved |
| 4th+ ticket | Capped at 60% for that week |
| Ticket not filed (left class without pass or ticket) | Week counts as incomplete (0–40%) |
| Ticket filed but never resolved | Converts to incomplete after 2 weeks |
| Repeated unresolved tickets | Triggers mandatory instructor meeting |

---

## Red list escalation

Students go on the red list when:
- 2+ failed checks in a row
- 2+ open (unresolved) recovery tickets
- Cannot explain code in oral check

**Red list treatment (automatic, not punitive):**
1. Next week: start with rescue lane (simpler tasks, more scaffolding)
2. Mandatory instructor checkpoint at mid-session
3. Reduced scope: must-pass core only until stable
4. Weekly 5-minute check-in with instructor

**Exit red list when:**
- 2 consecutive weeks with must-pass core completed
- Can explain their code
- Recovery tickets resolved

---

## Repo recovery

If the repo structure is broken (deleted files, broken imports, wrong paths):

1. Student restores from last known-working commit: `git log`, find it, `git checkout <hash> -- src/`
2. If no working commit exists: instructor provides a clean recovery template for that week
3. Student must restore repo to passing state before continuing with new content
4. Repeated repo breakage triggers a structure check + mandatory instructor review

---

## Communication templates

### Ticket acknowledgment (instructor → student)
> "Got your recovery ticket. The issue is [brief diagnosis]. Try [specific hint]. Come to next session with this fixed — I'll check it during the first 15 minutes."

### Red list notification (instructor → student)
> "You're on the support list for the next session. This means you'll start with the guided rescue tasks and I'll check in with you at the mid-session checkpoint. This is support, not a penalty — the goal is to get you back on track."

### Escalation (instructor → student, after 3+ unresolved weeks)
> "I'm seeing a pattern of incomplete work over the past few weeks. Let's meet for 10 minutes [time] to figure out what's blocking you and make a concrete plan. Bring your laptop with your repo open."
