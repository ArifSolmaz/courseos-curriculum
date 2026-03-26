// ── CourseOS Static Platform — SPA Router & Renderer ───────────

let state = loadState();

// ── Router ─────────────────────────────────────────────────────

function navigate(hash) {
  window.location.hash = hash;
}

function getRoute() {
  const hash = window.location.hash.slice(1) || "dashboard";
  const parts = hash.split("/");
  return { page: parts[0], params: parts.slice(1) };
}

window.addEventListener("hashchange", render);
window.addEventListener("DOMContentLoaded", () => {
  if (!state.setup) {
    window.location.hash = "#setup";
  }
  render();
});

function render() {
  const route = getRoute();
  const app = document.getElementById("app");
  const sidebar = document.getElementById("sidebar");

  if (!state.setup && route.page !== "setup") {
    window.location.hash = "#setup";
    return;
  }

  if (route.page === "setup") {
    sidebar.style.display = "none";
    app.innerHTML = renderSetup();
  } else {
    sidebar.style.display = "";
    updateSidebarActive(route);
    switch (route.page) {
      case "dashboard": app.innerHTML = renderDashboard(); break;
      case "course": app.innerHTML = renderCourse(route.params[0]); break;
      case "week": app.innerHTML = renderWeek(route.params[0], parseInt(route.params[1])); break;
      case "project": app.innerHTML = renderProject(); break;
      case "track": app.innerHTML = renderTrack(); break;
      default: app.innerHTML = renderDashboard();
    }
  }
  animateProgressBars();
}

function animateProgressBars() {
  document.querySelectorAll(".progress-fill").forEach(bar => {
    const w = bar.style.width;
    bar.style.width = "0%";
    requestAnimationFrame(() => requestAnimationFrame(() => { bar.style.width = w; }));
  });
}

function updateSidebarActive(route) {
  document.querySelectorAll(".sidebar-nav a").forEach(a => {
    a.classList.remove("active");
    if (a.dataset.page === route.page || (route.page === "week" && a.dataset.page === "course" && a.dataset.code === route.params[0])) {
      a.classList.add("active");
    }
  });
}

// ── Setup Page ─────────────────────────────────────────────────

function renderSetup() {
  return `
  <div class="auth-container">
    <div class="auth-card">
      <h1>CourseOS</h1>
      <div class="subtitle">Set up your student profile</div>
      <div class="form-group">
        <label>Full Name</label>
        <input type="text" id="setup-name" placeholder="Your full name" value="${state.student.name}">
      </div>
      <div class="form-group">
        <label>Student ID</label>
        <input type="text" id="setup-id" placeholder="e.g. 2025-MC-001" value="${state.student.studentId}">
      </div>
      <button class="btn btn-primary" style="width:100%;margin-top:8px;" onclick="completeSetup()">Get Started</button>
    </div>
  </div>`;
}

function completeSetup() {
  const name = document.getElementById("setup-name").value.trim();
  const id = document.getElementById("setup-id").value.trim();
  if (!name || !id) return alert("Please fill in both fields.");
  state.student.name = name;
  state.student.studentId = id;
  state.setup = true;
  saveState(state);
  navigate("dashboard");
}

// ── Dashboard ──────────────────────────────────────────────────

function renderDashboard() {
  const track = TRACKS[state.student.track];
  const trackLabel = track ? `${track.icon} <strong>${track.name}</strong>` : `<a href="#track" class="btn btn-primary btn-sm">Select your track</a>`;
  const trackBadge = state.student.trackConfirmed ? `<span class="badge badge-success">Confirmed</span>` : (track ? `<span class="badge badge-warning">Exploring</span>` : "");

  const recentChecks = getRecentChecks(state);
  const checksHTML = recentChecks.length ? recentChecks.map(c => `
    <div class="flex-between" style="padding:10px 0;border-bottom:1px solid var(--border-light);">
      <div class="flex-center gap-1">
        <span class="badge ${c.passed ? 'badge-success' : 'badge-danger'}">${c.passed ? 'PASSED' : 'FAILED'}</span>
        <span class="text-sm font-medium">${c.course.toUpperCase()} W${c.week}</span>
        <span class="text-sm text-muted">— ${c.title}</span>
      </div>
      <span class="text-xs text-muted">${c.checks || ''}</span>
    </div>`).join("") : `<div class="empty-state"><p>No checks recorded yet</p></div>`;

  return `
  <div class="page-header">
    <h1>Welcome back, ${esc(state.student.name)}</h1>
    <div class="subtitle">Track: ${trackLabel} ${trackBadge}</div>
  </div>

  <div class="card mb-3">
    <div class="card-header"><h2>Pipeline Evolution</h2><a href="#project" class="btn btn-outline btn-sm">View project</a></div>
    <div class="evolution-pipeline">
      ${Object.values(COURSES).map((c, i, arr) => {
        const pct = getProgress(state, c.code);
        const cls = pct === 100 ? "completed" : pct > 0 ? "active" : "";
        return `<div class="evo-stage ${cls}">
          <div class="evo-version">${c.version}</div>
          <h4>${c.code.toUpperCase()}</h4>
          <div class="evo-desc">${c.desc}</div>
          <div class="mt-1">
            <div class="progress-bar" style="height:5px"><div class="progress-fill ${pct===100?'success':''}" style="width:${pct}%"></div></div>
            <div class="text-xs text-muted mt-1">${pct}%</div>
          </div>
        </div>${i < arr.length - 1 ? '<div class="evo-arrow">➔</div>' : ''}`;
      }).join("")}
    </div>
  </div>

  <div class="grid grid-4 mb-3">
    <div class="card stat-card"><div class="stat-value">${getOverallProgress(state)}%</div><div class="stat-label">Overall Progress</div></div>
    <div class="card stat-card"><div class="stat-value">${recentChecks.filter(c=>c.passed).length}/${recentChecks.length}</div><div class="stat-label">Recent Checks</div></div>
    <div class="card stat-card"><div class="stat-value">${Object.keys(state.recovery).length}</div><div class="stat-label">Recovery Tickets</div></div>
    <div class="card stat-card"><div class="stat-value">${getCurrentVersion(state)}</div><div class="stat-label">Current Version</div></div>
  </div>

  <div class="section-header"><h2>Your Courses</h2></div>
  <div class="grid grid-2 mb-3">
    ${Object.values(COURSES).map(c => {
      const pct = getProgress(state, c.code);
      return `<a href="#course/${c.code}" style="text-decoration:none;color:inherit;">
        <div class="card course-card">
          <span class="version-badge">${c.version}</span>
          <div class="course-code">${c.code}</div>
          <h3>${c.name}</h3>
          <div class="course-desc">${c.desc}</div>
          <div class="course-meta"><span>Year ${c.year}, Sem ${c.semester}</span><span>${c.hours}h/week</span><span>14 weeks</span></div>
          <div class="mt-2">
            <div class="progress-label"><span>Progress</span><span>${pct}%</span></div>
            <div class="progress-bar"><div class="progress-fill ${pct===100?'success':''}" style="width:${pct}%"></div></div>
          </div>
        </div>
      </a>`;
    }).join("")}
  </div>

  <div class="card">
    <div class="card-header"><h2>Recent Checks</h2></div>
    ${checksHTML}
  </div>`;
}

// ── Course View ────────────────────────────────────────────────

function renderCourse(code) {
  const c = COURSES[code];
  if (!c) return "<p>Course not found</p>";
  const weeks = WEEKS[code] || [];
  const passedCount = weeks.filter(w => state.weeks[`${code}-${w.num}`]?.passed).length;
  const pct = Math.round(passedCount / weeks.length * 100);

  return `
  <div class="breadcrumb">
    <a href="#dashboard">Dashboard</a><span class="sep">/</span><span class="current">${code.toUpperCase()} — ${c.name}</span>
  </div>
  <div class="page-header">
    <h1>${c.name}</h1>
    <div class="subtitle">Year ${c.year}, Semester ${c.semester} · ${c.hours}h/week · Target: <strong>${c.version}</strong></div>
  </div>
  <div class="card mb-3">
    <div class="progress-label"><span>Course Progress</span><span>${passedCount} of ${weeks.length} weeks passed</span></div>
    <div class="progress-bar" style="height:10px"><div class="progress-fill ${pct===100?'success':''}" style="width:${pct}%"></div></div>
  </div>
  <ul class="week-list">
    ${weeks.map(w => {
      const key = `${code}-${w.num}`;
      const ws = state.weeks[key];
      const passed = ws?.passed;
      const numClass = passed === true ? "passed" : passed === false ? "failed" : "";
      const numContent = passed === true ? "✓" : passed === false ? "✗" : w.num;
      const badge = passed === true ? '<span class="badge badge-success">Passed</span>' : passed === false ? '<span class="badge badge-danger">Failed</span>' : '<span class="badge badge-muted">Pending</span>';
      const done = getDeliverablesDone(state, code, w.num);
      return `<a href="#week/${code}/${w.num}" style="text-decoration:none;color:inherit;">
        <li class="week-item">
          <div class="week-num ${numClass}">${numContent}</div>
          <div class="week-info">
            <h4>Week ${w.num}: ${w.title}</h4>
            ${w.sprint ? `<span class="sprint-tag">Sprint ${w.sprint}</span>` : ''}
          </div>
          <div class="week-meta">
            <span class="text-sm">${done}/${DELIVERABLES.length}</span>
            ${badge}
          </div>
        </li>
      </a>`;
    }).join("")}
  </ul>`;
}

// ── Week Detail ────────────────────────────────────────────────

function renderWeek(code, num) {
  const c = COURSES[code];
  const weeks = WEEKS[code] || [];
  const w = weeks.find(x => x.num === num);
  if (!c || !w) return "<p>Week not found</p>";

  const key = `${code}-${num}`;
  const ws = state.weeks[key] || {};
  const ref = state.reflections[key] || {};
  const rec = state.recovery[key];
  const prev = num > 1 ? num - 1 : null;
  const next = num < 14 ? num + 1 : null;

  const checkBadge = ws.passed === true ? '<span class="badge badge-success">PASSED · ' + (ws.checks||'') + '</span>'
    : ws.passed === false ? '<span class="badge badge-danger">FAILED · ' + (ws.checks||'') + '</span>'
    : '<span class="badge badge-muted">Not run yet</span>';

  return `
  <div class="breadcrumb">
    <a href="#dashboard">Dashboard</a><span class="sep">/</span>
    <a href="#course/${code}">${code.toUpperCase()}</a><span class="sep">/</span>
    <span class="current">Week ${num}: ${w.title}</span>
  </div>

  <div class="flex-between mb-2">
    ${prev ? `<a href="#week/${code}/${prev}" class="btn btn-outline btn-sm">← Week ${prev}</a>` : '<div></div>'}
    ${next ? `<a href="#week/${code}/${next}" class="btn btn-outline btn-sm">Week ${next} →</a>` : '<div></div>'}
  </div>

  <div class="page-header">
    <h1>Week ${num}: ${w.title}</h1>
    <div class="subtitle">${c.name}${w.sprint ? ' · Sprint ' + w.sprint : ''}</div>
  </div>

  <div class="grid grid-3 mb-3">
    <div class="target-card must-pass"><div class="target-label">Must-Pass Core</div><p class="text-sm">Complete the minimum working version</p></div>
    <div class="target-card standard"><div class="target-label">Standard Target</div><p class="text-sm">Complete the normal weekly goal</p></div>
    <div class="target-card stretch"><div class="target-label">Stretch</div><p class="text-sm">Optional extension for fast students</p></div>
  </div>

  <div class="card mb-3">
    <div class="card-header"><h2>Universal Check</h2>${checkBadge}</div>
    <div class="inline-form">
      <select id="check-passed"><option value="true">Passed</option><option value="false">Failed</option></select>
      <input type="text" id="check-score" placeholder="e.g. 8/10" value="${ws.checks||''}" style="width:100px">
      <button class="btn btn-primary btn-sm" onclick="saveCheck('${code}',${num})">Record</button>
    </div>
  </div>

  <div class="card mb-3">
    <div class="card-header"><h2>Deliverables</h2><span class="text-sm text-muted">${getDeliverablesDone(state,code,num)}/${DELIVERABLES.length} complete</span></div>
    ${DELIVERABLES.map(d => {
      const dk = `${code}-${num}-${d.type}`;
      const st = state.deliverables[dk] || "";
      const done = ["submitted","passed"].includes(st);
      return `<div class="deliverable-item">
        <div class="check-icon ${done?'done':'pending'}">${done?'✓':'·'}</div>
        <div class="deliverable-info"><h5>${d.name}</h5><span class="type-tag">${d.type}</span>
          ${st ? `<span class="badge ${st==='passed'?'badge-success':st==='submitted'?'badge-info':'badge-danger'}" style="margin-left:6px">${st}</span>` : ''}
        </div>
        <div class="inline-form">
          <select id="del-${dk}"><option value="">—</option><option value="submitted" ${st==='submitted'?'selected':''}>Submitted</option><option value="passed" ${st==='passed'?'selected':''}>Passed</option><option value="failed" ${st==='failed'?'selected':''}>Needs Work</option></select>
          <button class="btn btn-primary btn-sm" onclick="saveDeliverable('${dk}')">Save</button>
        </div>
      </div>`;
    }).join("")}
  </div>

  <div class="card mb-3">
    <div class="card-header"><h2>Weekly Reflection</h2>${ref.learned ? '<span class="badge badge-success">Saved</span>' : ''}</div>
    <div class="grid grid-2">
      <div class="form-group"><label>What I learned today</label><textarea id="ref-learned" rows="2">${esc(ref.learned||'')}</textarea></div>
      <div class="form-group"><label>What was hardest</label><textarea id="ref-hardest" rows="2">${esc(ref.hardest||'')}</textarea></div>
      <div class="form-group"><label>What I still don't understand</label><textarea id="ref-unclear" rows="2">${esc(ref.unclear||'')}</textarea></div>
      <div class="form-group"><label>What I'll review next</label><textarea id="ref-next" rows="2">${esc(ref.next||'')}</textarea></div>
    </div>
    <div class="form-group"><label>AI tools used (if any)</label><textarea id="ref-ai" rows="1">${esc(ref.ai||'')}</textarea></div>
    <button class="btn btn-primary" onclick="saveReflection('${code}',${num})">Save Reflection</button>
  </div>

  ${!ws.passed ? `
  <div class="card recovery-card mb-3">
    <div class="card-header"><h2>Recovery Ticket</h2>${rec ? '<span class="badge badge-warning">Submitted</span>' : ''}</div>
    ${rec ? `<div class="text-sm" style="line-height:1.8"><strong>What failed:</strong> ${esc(rec.whatFailed)}<br><strong>What tried:</strong> ${esc(rec.whatTried)}<br><strong>Next steps:</strong> ${esc(rec.nextSteps)}</div>` : `
    <p class="text-sm text-muted mb-2">Can't finish the must-pass core? Submit a recovery ticket.</p>
    <div class="form-group"><label>What failed?</label><textarea id="rec-failed" rows="2"></textarea></div>
    <div class="form-group"><label>What did you try?</label><textarea id="rec-tried" rows="2"></textarea></div>
    <div class="form-group"><label>Next steps?</label><textarea id="rec-next" rows="2"></textarea></div>
    <button class="btn btn-warning" onclick="saveRecovery('${code}',${num})">Submit Recovery Ticket</button>`}
  </div>` : ''}`;
}

// ── Project View ───────────────────────────────────────────────

function renderProject() {
  const track = TRACKS[state.student.track];
  const productName = track ? `${track.icon} ${track.product}` : "Select a track first";

  return `
  <div class="breadcrumb"><a href="#dashboard">Dashboard</a><span class="sep">/</span><span class="current">My Project</span></div>
  <div class="page-header">
    <h1>${productName}</h1>
    <div class="subtitle">Track: <strong>${track ? track.name : 'Undecided'}</strong></div>
  </div>

  <div class="card mb-3">
    <div class="card-header"><h2>Pipeline Evolution</h2></div>
    <div class="evolution-pipeline">
      ${Object.values(COURSES).map((c, i, arr) => {
        const pct = getProgress(state, c.code);
        const cls = pct === 100 ? "completed" : pct > 0 ? "active" : "";
        return `<div class="evo-stage ${cls}">
          <div class="evo-version">${c.version}</div><h4>${c.code.toUpperCase()}</h4>
          <div class="evo-desc">${c.desc}</div>
          <div class="mt-1"><div class="progress-bar" style="height:5px"><div class="progress-fill ${pct===100?'success':''}" style="width:${pct}%"></div></div><div class="text-xs text-muted mt-1">${pct}%</div></div>
        </div>${i < arr.length-1 ? '<div class="evo-arrow">➔</div>' : ''}`;
      }).join("")}
    </div>
  </div>

  <div class="grid grid-2 mb-3">
    ${Object.entries(VERSION_INFO).map(([v, info]) => `
      <div class="card" style="border-top:3px solid var(--accent);">
        <h3>${info.label}</h3><p class="text-xs text-muted mb-1">End of ${info.course}</p>
        <ul class="text-sm" style="list-style:none;padding:0;color:var(--text-secondary);line-height:2;">
          ${info.items.map(it => `<li>✓ ${it}</li>`).join("")}
        </ul>
      </div>`).join("")}
  </div>

  <div class="card mb-3">
    <div class="card-header"><h2>Update Project Phase</h2></div>
    <div class="grid grid-2">
      <div class="form-group"><label>Course</label><select id="phase-course">${Object.values(COURSES).map(c=>`<option value="${c.code}">${c.code.toUpperCase()} — ${c.name}</option>`).join("")}</select></div>
      <div class="form-group"><label>Version</label><select id="phase-version">${Object.entries(VERSION_INFO).map(([v,i])=>`<option value="${v}">${i.label}</option>`).join("")}</select></div>
      <div class="form-group"><label>Status</label><select id="phase-status"><option value="in_progress">In Progress</option><option value="submitted">Submitted</option><option value="approved">Approved</option><option value="needs_work">Needs Work</option></select></div>
      <div class="form-group"><label>Git Commit</label><input type="text" id="phase-commit" placeholder="e.g. abc1234"></div>
    </div>
    <div class="form-group"><label>What changed?</label><textarea id="phase-desc" rows="2"></textarea></div>
    <button class="btn btn-primary" onclick="savePhase()">Save Update</button>
  </div>

  ${state.phases.length ? `<div class="card"><div class="card-header"><h2>Project History</h2></div>
    <div class="timeline">${state.phases.slice().reverse().map(p => `
      <div class="timeline-item ${p.status}">
        <div class="timeline-date">${p.date} · <strong>${p.course.toUpperCase()}</strong></div>
        <div class="timeline-version">${p.version} <span class="badge ${p.status==='approved'?'badge-success':p.status==='in_progress'?'badge-warning':'badge-info'}">${p.status}</span></div>
        ${p.desc ? `<div class="text-sm text-secondary mt-1">${esc(p.desc)}</div>` : ''}
        ${p.commit ? `<div class="text-xs text-muted mt-1">Commit: <code style="background:var(--bg);padding:2px 6px;border-radius:4px;">${esc(p.commit)}</code></div>` : ''}
      </div>`).join("")}</div></div>` : `<div class="card"><div class="empty-state"><div class="empty-icon">🚀</div><p>No project updates yet. Record your first phase above!</p></div></div>`}`;
}

// ── Track Selection ────────────────────────────────────────────

function renderTrack() {
  return `
  <div class="breadcrumb"><a href="#dashboard">Dashboard</a><span class="sep">/</span><span class="current">Track Selection</span></div>
  <div class="page-header">
    <h1>Choose Your Track</h1>
    <div class="subtitle">All tracks follow the same contract and grading. Pick the domain that excites you most.${!state.student.trackConfirmed ? '<br>Explore during Weeks 1–2, confirm by Week 3.' : ''}</div>
  </div>
  <div class="grid grid-3 mb-3">
    ${Object.entries(TRACKS).map(([k, t]) => `
      <div class="card track-card ${state.student.track===k?'selected':''}" onclick="selectTrack('${k}')">
        <div class="track-icon">${t.icon}</div>
        <div class="track-name">${t.name}</div>
        <div class="track-product">${t.product}</div>
      </div>`).join("")}
  </div>
  <div class="card" id="track-confirm" style="${state.student.track==='undecided'?'display:none':''}">
    <h3 id="track-selected-name">${TRACKS[state.student.track]?.name || ''}</h3>
    <p class="text-sm text-muted mb-2" id="track-selected-product">${TRACKS[state.student.track]?.product || ''}</p>
    ${!state.student.trackConfirmed ? `<label class="text-sm"><input type="checkbox" id="track-lock"> <strong>Lock</strong> this track (cannot change after confirmation)</label><br><br>` : '<span class="badge badge-success mb-2">Track confirmed and locked</span><br><br>'}
    <button class="btn btn-primary" onclick="confirmTrack()">Save Track</button>
  </div>`;
}

// ── Actions ────────────────────────────────────────────────────

let _selectedTrack = null;

function selectTrack(key) {
  _selectedTrack = key;
  document.querySelectorAll(".track-card").forEach(c => c.classList.remove("selected"));
  event.currentTarget.classList.add("selected");
  document.getElementById("track-confirm").style.display = "";
  document.getElementById("track-selected-name").textContent = TRACKS[key].name;
  document.getElementById("track-selected-product").textContent = TRACKS[key].product;
}

function confirmTrack() {
  const key = _selectedTrack || state.student.track;
  if (!key || key === "undecided") return;
  state.student.track = key;
  const lockEl = document.getElementById("track-lock");
  if (lockEl && lockEl.checked) state.student.trackConfirmed = true;
  saveState(state);
  render();
}

function saveCheck(code, num) {
  const key = `${code}-${num}`;
  const passed = document.getElementById("check-passed").value === "true";
  const checks = document.getElementById("check-score").value;
  state.weeks[key] = { passed, checks, title: WEEKS[code]?.find(w=>w.num===num)?.title };
  saveState(state);
  render();
}

function saveDeliverable(dk) {
  const val = document.getElementById(`del-${dk}`).value;
  if (val) state.deliverables[dk] = val;
  else delete state.deliverables[dk];
  saveState(state);
  render();
}

function saveReflection(code, num) {
  const key = `${code}-${num}`;
  state.reflections[key] = {
    learned: document.getElementById("ref-learned").value,
    hardest: document.getElementById("ref-hardest").value,
    unclear: document.getElementById("ref-unclear").value,
    next: document.getElementById("ref-next").value,
    ai: document.getElementById("ref-ai").value,
  };
  saveState(state);
  render();
}

function saveRecovery(code, num) {
  const key = `${code}-${num}`;
  state.recovery[key] = {
    whatFailed: document.getElementById("rec-failed").value,
    whatTried: document.getElementById("rec-tried").value,
    nextSteps: document.getElementById("rec-next").value,
  };
  saveState(state);
  render();
}

function savePhase() {
  state.phases.push({
    course: document.getElementById("phase-course").value,
    version: document.getElementById("phase-version").value,
    status: document.getElementById("phase-status").value,
    commit: document.getElementById("phase-commit").value,
    desc: document.getElementById("phase-desc").value,
    date: new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }),
  });
  saveState(state);
  render();
}

function resetData() {
  if (confirm("Reset all progress? This cannot be undone.")) {
    localStorage.removeItem(STATE_KEY);
    state = getDefaultState();
    navigate("setup");
  }
}

function esc(str) {
  if (!str) return "";
  return str.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}
