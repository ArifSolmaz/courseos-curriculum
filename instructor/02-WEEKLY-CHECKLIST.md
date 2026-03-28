# Weekly Instructor Checklist

Use this every session. Print it or keep it open.

---

## CP1 / CP2 — 5-hour session

### Before class (15 min prep)
- [ ] Review this week's Core + Studio notebooks (skim for issues)
- [ ] Prepare micro-quiz (5 questions on last week's concepts, 10 min)
- [ ] Check red list from last week — who needs rescue lane?
- [ ] Have recovery template ready for students who can't finish

### 0:00–0:20 — Warm-up
- [ ] Run micro-quiz (paper or Colab form)
- [ ] State today's acceptance criteria on board/screen:
  - Must-pass core: _____
  - Standard target: _____
  - Stretch: _____
- [ ] Red-list students start with rescue lane tasks

### 0:20–1:30 — Core notebook (self-paced)
- [ ] Students work through Core notebook independently
- [ ] Walk the room — watch for students stuck on setup
- [ ] If 3+ students hit the same issue → 5-min mini-clinic on board
- [ ] **No lecturing** — coach, don't teach

### 1:30–1:45 — Break

### 1:45–2:30 — Mid-session checkpoint
- [ ] **Must-pass core check**: every student/team must show the core milestone
- [ ] Students who haven't reached it → switch to rescue lane immediately
- [ ] Quick oral check: pick 2–3 students, ask "explain this line"
- [ ] Log who passed / who didn't

### 2:30–3:15 — Studio sprint
- [ ] Students work on track-specific Studio notebook
- [ ] Help queue: track + week + cell number + error + what they tried
- [ ] Don't solve it for them — guide with questions

### 3:15–3:25 — Break

### 3:25–4:35 — Check + hardening
- [ ] Students run Universal Check notebook
- [ ] Fix failures in `/src`, NOT in the notebook
- [ ] Students export required artifacts
- [ ] Walk the room checking exports exist

### 4:35–5:00 — Demo + reflection
- [ ] 2–3 voluntary demos (2 min each)
- [ ] Everyone completes reflection cell
- [ ] Students who didn't finish must-pass core → recovery ticket
- [ ] **Anti-silent-failure rule**: nobody leaves without a pass OR a recovery ticket

### After class (10 min)
- [ ] Update red list
- [ ] Note common issues for next week's mini-clinic
- [ ] Check that repos have new commits (quick scan)
- [ ] Grade/mark recovery tickets from last week

---

## OOP / DSA — 3-hour session

### 0:00–0:15 — Warm-up
- [ ] Code-reading quiz or "explain this class/algorithm" oral check
- [ ] State acceptance criteria

### 0:15–1:20 — Core notebook
- [ ] Self-paced with coaching
- [ ] Mini-clinic if needed (architecture/algorithm explanation)
- [ ] For DSA: ensure students understand Big-O before implementing

### 1:20–1:30 — Break

### 1:30–2:40 — Studio work
- [ ] Refactor/implement/benchmark sprint
- [ ] Checkpoint at 2:00 — must-pass core milestone
- [ ] Help queue active

### 2:40–3:00 — Tests/benchmarks + engineering note
- [ ] Students run pytest (OOP) or benchmark (DSA)
- [ ] Write engineering note: what they did, why, what's next
- [ ] Recovery ticket if incomplete

---

## Red list management

A student goes on the red list if:
- Failed the same check **2 times**
- Did not complete must-pass core
- Cannot explain their own code in a 2-min oral check
- Keeps patching notebooks without fixing `/src`

**Red list students automatically get:**
1. Next week's rescue lane tasks first
2. Mandatory instructor checkpoint before submission
3. Simpler acceptance criteria until stable

**Remove from red list when:**
- 2 consecutive weeks with must-pass core completed
- Can explain their code in oral check
