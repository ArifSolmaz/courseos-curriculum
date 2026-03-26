// ── CourseOS Static Data & State ────────────────────────────────

const TRACKS = {
  robotics: { name: "Robotics / Mechatronics", product: "MechaSense Studio", icon: "🤖", color: "#E53935" },
  data:     { name: "Data / AI", product: "CleanReport Pipeline", icon: "📊", color: "#1E88E5" },
  simulation: { name: "Simulation / Games", product: "SimLab Engine", icon: "🎮", color: "#43A047" },
  space:    { name: "Space / Astro", product: "Lightcurve Explorer", icon: "🌌", color: "#8E24AA" },
  iot:      { name: "IoT / Reporting", product: "AutoDashboard Reporter", icon: "📡", color: "#FB8C00" },
};

const COURSES = {
  cp1: { code: "cp1", name: "Computer Programming 1", semester: 1, year: 1, hours: 5, version: "v1", desc: "Python fundamentals → v1 functional pipeline" },
  cp2: { code: "cp2", name: "Computer Programming 2", semester: 2, year: 1, hours: 5, version: "v2", desc: "Robust data handling → v2 professional tool" },
  oop: { code: "oop", name: "Object-Oriented Programming", semester: 3, year: 2, hours: 3, version: "v3-arch", desc: "Refactor into architecture → v3 components" },
  dsa: { code: "dsa", name: "Data Structures & Algorithms", semester: 4, year: 2, hours: 3, version: "v3-perf", desc: "Optimize + benchmark → v3 performance proof" },
};

const WEEKS = {
  cp1: [
    { num: 1, title: "Welcome to Python & Your Pipeline", sprint: "S1" },
    { num: 2, title: "Variables, Types & Numbers", sprint: "S1" },
    { num: 3, title: "Making Decisions (Conditionals)", sprint: "S2" },
    { num: 4, title: "Decision Logic & Classification", sprint: "S2" },
    { num: 5, title: "Loops: Scanning Data", sprint: "S3" },
    { num: 6, title: "Loops: Counting Events", sprint: "S3" },
    { num: 7, title: "Lists: Indexing & Windows", sprint: "S4" },
    { num: 8, title: "Strings: Parsing Data", sprint: "S4" },
    { num: 9, title: "Functions: Building Blocks", sprint: "S5" },
    { num: 10, title: "Functions: Decomposition & Reuse", sprint: "S5" },
    { num: 11, title: "Exceptions: Handling Errors", sprint: "S6" },
    { num: 12, title: "File I/O: Reading & Writing", sprint: "S6" },
    { num: 13, title: "Integration: End-to-End Pipeline", sprint: "S6" },
    { num: 14, title: "v1 Release & Demo", sprint: "S6" },
  ],
  cp2: [
    { num: 1, title: "Schema Validation", sprint: "S7" },
    { num: 2, title: "Dict Analytics", sprint: "S7" },
    { num: 3, title: "Configurable Cleaning Pipeline", sprint: "S8" },
    { num: 4, title: "Data Quality Reports", sprint: "S8" },
    { num: 5, title: "Matplotlib Standards", sprint: "S9" },
    { num: 6, title: "Report Generation", sprint: "S9" },
    { num: 7, title: "NumPy Introduction", sprint: "S10" },
    { num: 8, title: "Timing & Performance", sprint: "S10" },
    { num: 9, title: "Testing: Expanded Self-Check", sprint: "S11" },
    { num: 10, title: "Golden Outputs", sprint: "S11" },
    { num: 11, title: "Modularize into /src", sprint: "S12" },
    { num: 12, title: "Package Hygiene", sprint: "S12" },
    { num: 13, title: "Integration on Larger Data", sprint: "S12" },
    { num: 14, title: "v2 Release & Demo", sprint: "S12" },
  ],
  oop: [
    { num: 1, title: "OOP Kickoff: Classes & Objects", sprint: "" },
    { num: 2, title: "Composition: DataSource & Dataset", sprint: "" },
    { num: 3, title: "Cleaner Component", sprint: "" },
    { num: 4, title: "Analyzer Component", sprint: "" },
    { num: 5, title: "Plotter & Reporter Components", sprint: "" },
    { num: 6, title: "Domain Exceptions & Validation", sprint: "" },
    { num: 7, title: "SOLID Principles (SRP/OCP)", sprint: "" },
    { num: 8, title: "Strategy Pattern", sprint: "" },
    { num: 9, title: "Factory & Registry Pattern", sprint: "" },
    { num: 10, title: "Testing with pytest", sprint: "" },
    { num: 11, title: "Package Hygiene", sprint: "" },
    { num: 12, title: "Plugin Exercise", sprint: "" },
    { num: 13, title: "Architecture Freeze", sprint: "" },
    { num: 14, title: "v3 Architecture Demo", sprint: "" },
  ],
  dsa: [
    { num: 1, title: "Big-O & Python Cost Model", sprint: "" },
    { num: 2, title: "Benchmark Literacy", sprint: "" },
    { num: 3, title: "Searching: Linear vs Binary", sprint: "" },
    { num: 4, title: "Sorting Algorithms", sprint: "" },
    { num: 5, title: "Hashing & Indexing", sprint: "" },
    { num: 6, title: "Heap & Priority Queue", sprint: "" },
    { num: 7, title: "Performance Sprint 1", sprint: "" },
    { num: 8, title: "Performance Sprint 2", sprint: "" },
    { num: 9, title: "Trees & BST", sprint: "" },
    { num: 10, title: "Graphs: BFS & DFS", sprint: "" },
    { num: 11, title: "Shortest Paths", sprint: "" },
    { num: 12, title: "Dynamic Programming", sprint: "" },
    { num: 13, title: "Final Integration", sprint: "" },
    { num: 14, title: "Final Performance Report", sprint: "" },
  ],
};

const DELIVERABLES = [
  { type: "core_notebook", name: "Core Notebook" },
  { type: "studio_notebook", name: "Studio Notebook" },
  { type: "check", name: "Universal Check" },
  { type: "homework", name: "Homework" },
  { type: "export", name: "Required Exports" },
  { type: "code", name: "Pipeline Code Update" },
];

const VERSION_INFO = {
  v1: { label: "v1 — Functional Pipeline", course: "CP1", items: ["load_data()", "clean_data()", "analyze()", "plot()", "export_results()", "self_check()"] },
  v2: { label: "v2 — Professional Tool", course: "CP2", items: ["Schema validation", "Configurable cleaning", "Professional plots", "JSON + MD reports", "Modularized /src", "Golden output tests"] },
  "v3-arch": { label: "v3 — Architecture", course: "OOP", items: ["5 OOP components", "Strategy pattern", "Factory / registry", "Custom exceptions", "pytest suite", "Plugin-ready"] },
  "v3-perf": { label: "v3 — Performance", course: "DSA", items: ["Optimized dsa/ module", "Baseline vs optimized", "Big-O analysis", "Benchmark plots", "≥1.5× speedup", "Wired into product"] },
};

// ── State Management (localStorage) ────────────────────────────

const STATE_KEY = "courseos_state";

function getDefaultState() {
  return {
    student: { name: "", studentId: "", track: "undecided", trackConfirmed: false },
    weeks: {},      // { "cp1-1": { passed: true, checks: "8/10" }, ... }
    deliverables: {}, // { "cp1-1-core_notebook": "submitted", ... }
    reflections: {},  // { "cp1-1": { learned: "...", ... } }
    phases: [],       // [{ course: "cp1", version: "v1", status: "in_progress", date: "...", desc: "..." }]
    recovery: {},     // { "cp1-3": { whatFailed: "...", ... } }
    setup: false,
  };
}

function loadState() {
  try {
    const raw = localStorage.getItem(STATE_KEY);
    if (raw) return { ...getDefaultState(), ...JSON.parse(raw) };
  } catch (e) {}
  return getDefaultState();
}

function saveState(state) {
  localStorage.setItem(STATE_KEY, JSON.stringify(state));
}

function getProgress(state, courseCode) {
  const weeks = WEEKS[courseCode] || [];
  if (!weeks.length) return 0;
  let passed = 0;
  weeks.forEach(w => {
    const key = `${courseCode}-${w.num}`;
    if (state.weeks[key] && state.weeks[key].passed) passed++;
  });
  return Math.round(passed / weeks.length * 100);
}

function getOverallProgress(state) {
  const codes = Object.keys(COURSES);
  const total = codes.reduce((s, c) => s + getProgress(state, c), 0);
  return Math.round(total / codes.length);
}

function getDeliverablesDone(state, courseCode, weekNum) {
  let done = 0;
  DELIVERABLES.forEach(d => {
    const key = `${courseCode}-${weekNum}-${d.type}`;
    if (state.deliverables[key] && ["submitted", "passed"].includes(state.deliverables[key])) done++;
  });
  return done;
}

function getCurrentVersion(state) {
  if (!state.phases.length) return "—";
  return state.phases[state.phases.length - 1].version;
}

function getRecentChecks(state, limit = 5) {
  const checks = [];
  Object.keys(COURSES).forEach(code => {
    (WEEKS[code] || []).forEach(w => {
      const key = `${code}-${w.num}`;
      if (state.weeks[key]) {
        checks.push({ course: code, week: w.num, title: w.title, ...state.weeks[key] });
      }
    });
  });
  return checks.slice(-limit).reverse();
}
