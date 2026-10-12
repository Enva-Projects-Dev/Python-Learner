/* Python Learner - die UI */
(function () {
"use strict";

/* ---------- backend-adapter ---------- */
/* pywebview injected window.pywebview.api erst asynchron nach dem
   document load; drauf warten, aber plain browser nicht ewig hängen lassen */
var backendReady = new Promise(function (res) {
  var t0 = Date.now();
  (function poll() {
    if (window.pywebview && window.pywebview.api) return res();
    var waited = Date.now() - t0;
    if (!window.pywebview && waited > 1500) return res();   // normaler browser ohne pywebview
    if (waited > 10000) return res();                     // aufgeben, kommt wohl nicht mehr
    setTimeout(poll, 100);
  })();
});

function call(method, params) {
  params = params || {};
  return backendReady.then(function () {
    if (window.pywebview && window.pywebview.api && window.pywebview.api[method]) {
      return window.pywebview.api[method](params);
    }
    return fetch("/api/" + method, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params),
    }).then(function (r) { return r.json(); });
  }).catch(function (e) {
    return { error: String(e) };
  });
}

/* ---------- state ---------- */
var state = {
  content: null,
  progress: null,
  stats: null,
  locks: {},
  currentId: null,
  view: "dashboard",
  editor: null,
  hintLevel: 0,
  draftTimer: null,
  running: false,
};

var ITEMS = [];          // flache item-liste für prev/next
var ITEM_MAP = {};

function flatten() {
  ITEMS = [];
  state.content.chapters.forEach(function (ch) {
    ch.items.forEach(function (it) {
      ITEMS.push(it);
      ITEM_MAP[it.id] = { item: it, chapter: ch };
    });
  });
}

function isDone(id) {
  return !!(state.progress.completed || {})[id];
}

/* ---------- chapter-locks ---------- */
function lockOf(ch) {
  return (state.locks || {})[ch.id] || { locked: false, pct: 0, needed_pct: 90 };
}
function lockMessage(ch) {
  var l = lockOf(ch);
  return "Unlocks at " + l.needed_pct + "% of " + (l.prev_title || "the previous chapter")
    + " - you're at " + l.pct + "%";
}
function chapterById(id) {
  var found = null;
  (state.content ? state.content.chapters : []).forEach(function (ch) {
    if (ch.id === id) found = ch;
  });
  return found;
}

/* ---------- schlichter hinweis-toast ---------- */
function showToast(text) {
  var holder = document.getElementById("toast-holder");
  if (!holder) {
    holder = el("div");
    holder.id = "toast-holder";
    document.body.appendChild(holder);
  }
  var t = el("div", "toast", text);
  holder.appendChild(t);
  var dismiss = setTimeout(function () {
    t.classList.add("out");
    setTimeout(function () { t.remove(); }, 300);
  }, 3500);
  t.onclick = function () { clearTimeout(dismiss); t.remove(); };
}

function copyText(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    return navigator.clipboard.writeText(text).catch(function () {
      legacyCopy(text);
    });
  }
  legacyCopy(text);
  return Promise.resolve();
}
function legacyCopy(text) {
  var ta = document.createElement("textarea");
  ta.value = text;
  ta.style.position = "fixed";
  ta.style.opacity = "0";
  document.body.appendChild(ta);
  ta.select();
  try { document.execCommand("copy"); } catch (e) { /* egal */ }
  ta.remove();
}

function friendlyHtml(text) {
  return '<div class="friendly-callout"><div class="friendly-title">'
    + "What went wrong</div>" + escapeHtml(text) + "</div>";
}

function fmtNum(n) {
  return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

/* ---------- reward toast ---------- */
function showReward(rw) {
  if (!rw) return;
  var hasAch = (rw.achievements_unlocked || []).length > 0;
  var levelUp = rw.level_after > rw.level_before;
  var rankUp = rw.rank_after !== rw.rank_before;
  if (!rw.xp_gained && !hasAch && !levelUp) return;

  var toast = el("div", "reward-toast");
  var amount = el("div", "r-amount", "+0 XP");
  toast.appendChild(amount);
  (rw.breakdown || []).forEach(function (b) {
    var line = el("div", "r-line");
    line.appendChild(el("span", null, b.label));
    line.appendChild(el("span", null, String(b.value)));
    toast.appendChild(line);
  });
  if (hasAch) {
    var box = el("div", "r-ach", "Achievement unlocked");
    rw.achievements_unlocked.forEach(function (a) {
      box.appendChild(el("div", "a", a.title + " - +" + a.xp + " XP"));
    });
    toast.appendChild(box);
  }
  if (rankUp) {
    toast.appendChild(el("div", "r-rank", "New rank: " + rw.rank_after));
  }
  if (levelUp) {
    toast.appendChild(el("div", "r-levelup", "Level up - LV " + rw.level_after));
  }
  var holder = document.getElementById("toast-holder");
  if (!holder) {
    holder = el("div");
    holder.id = "toast-holder";
    document.body.appendChild(holder);
  }
  holder.appendChild(toast);

  var target = rw.xp_gained || 0, t0 = performance.now();
  (function tick(t) {
    var k = Math.min(1, (t - t0) / 600);
    amount.textContent = "+" + fmtNum(Math.round(target * k)) + " XP";
    if (k < 1) requestAnimationFrame(tick);
  })(t0);

  var dismiss = setTimeout(remove, 6000);
  function remove() { toast.remove(); }
  toast.onclick = function () { clearTimeout(dismiss); remove(); };
}

function applyStats(stats) {
  if (!stats) return;
  var before = state.locks || {};
  state.stats = stats;
  if (stats.locks) {
    state.locks = stats.locks;
    Object.keys(stats.locks).forEach(function (cid) {
      if (before[cid] && before[cid].locked && !stats.locks[cid].locked) {
        var ch = chapterById(cid);
        showToast("Chapter unlocked: " + (ch ? ch.title : cid));
      }
    });
    renderSidebar();
  }
  renderPlayer();
}

function renderPlayer() {
  var box = document.getElementById("player-card");
  if (!box || !state.stats) return;
  var s = state.stats;
  box.innerHTML = "";
  box.appendChild(el("div", "level-badge", "LV " + s.level));
  var meta = el("div", "player-meta");
  meta.appendChild(el("div", "rank-name", s.rank.name));
  var xl = el("div", "xp-line");
  var track = el("div", "progress-track");
  var fill = el("div", "progress-fill");
  fill.style.width = Math.round((s.level_progress || 0) * 100) + "%";
  track.appendChild(fill);
  xl.appendChild(track);
  xl.appendChild(el("span", "xp-text",
    fmtNum(s.xp) + " / " + fmtNum(s.next_level_xp) + " XP"));
  meta.appendChild(xl);
  var st = el("div", "streak-line" + (s.streak.count > 0 ? " on" : ""),
    s.streak.count > 0 ? s.streak.count + "-day streak" : "no streak yet");
  meta.appendChild(st);
  box.appendChild(meta);
}

/* ---------- hilfsfunktionen ---------- */
function el(tag, cls, text) {
  var e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined) e.textContent = text;
  return e;
}
function md(text) {
  var html = marked.parse(text || "");
  // callout-blöcke: > **Titel** -> gold label in großbuchstaben im quote
  return html.replace(
    /<blockquote>\s*<p><strong>([^<]+)<\/strong>/g,
    '<blockquote class="callout"><p><span class="callout-title">$1</span>');
}
function modal(title, body, okLabel) {
  return new Promise(function (resolve) {
    document.getElementById("modal-title").textContent = title;
    document.getElementById("modal-body").textContent = body;
    document.getElementById("modal-ok").textContent = okLabel || "OK";
    var bd = document.getElementById("modal-backdrop");
    bd.classList.remove("hidden");
    function done(v) {
      bd.classList.add("hidden");
      document.getElementById("modal-ok").onclick = null;
      document.getElementById("modal-cancel").onclick = null;
      resolve(v);
    }
    document.getElementById("modal-ok").onclick = function () { done(true); };
    document.getElementById("modal-cancel").onclick = function () { done(false); };
    bd.onclick = function (e) { if (e.target === bd) done(false); };
  });
}
// whats-new popup nach nem update - einmal pro version
function showWhatsNew(res) {
  if (!res || !res.show || !res.notes) return;
  var n = res.notes;
  var bd = document.getElementById("whatsnew-backdrop");
  document.getElementById("whatsnew-title").innerHTML =
    (n.title || "").replace("Änderungen", '<span class="hl">Änderungen</span>');
  document.getElementById("whatsnew-intro").textContent = n.intro || "";
  document.getElementById("whatsnew-outro").textContent = n.outro || "";
  var fill = function (id, items) {
    var ul = document.getElementById(id);
    ul.innerHTML = "";
    (items || []).forEach(function (t) {
      var li = document.createElement("li");
      li.textContent = t;
      ul.appendChild(li);
    });
  };
  fill("whatsnew-changes", n.changes);
  fill("whatsnew-new", n.new);
  bd.classList.remove("hidden");

  var escH = null;
  function close() {
    bd.classList.add("hidden");
    if (escH) document.removeEventListener("keydown", escH);
  }
  function weiter() { call("dismiss_whats_new"); close(); }
  escH = function (e) { if (e.key === "Escape") weiter(); };
  document.addEventListener("keydown", escH);
  bd.onclick = function (e) { if (e.target === bd) weiter(); };
  document.getElementById("whatsnew-ok").onclick = weiter;
  document.getElementById("whatsnew-reset").onclick = function () {
    modal("Wirklich alles zurücksetzen?",
      "Dein alter Stand wird vorher als Backup gespeichert.",
      "Zurücksetzen").then(function (ok) {
      if (!ok) return;
      call("reset_progress").then(function (r) {
        if (r && r.stats) applyStats(r.stats);
        call("get_progress").then(function (p) {
          state.progress = p || state.progress;
          flatten();
          renderAll();
        });
        showToast("Zurückgesetzt - Backup liegt neben progress.json");
        close();  // reset markiert die version schon als gesehen
      });
    });
  };
}

function btnLoading(btn, on, label) {
  if (on) {
    btn.dataset.label = btn.innerHTML;
    btn.innerHTML = '<span class="spinner"></span>' + (label || "Running...");
    btn.disabled = true;
  } else {
    btn.innerHTML = btn.dataset.label || label || "Run";
    btn.disabled = false;
  }
}

/* ---------- theme ---------- */
function applyTheme(t) {
  document.documentElement.setAttribute("data-theme", t === "dark" ? "dark" : "light");
  if (state.editor) state.editor.refresh();
}
function toggleTheme() {
  var cur = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
  applyTheme(cur);
  call("save_progress", { theme: cur });
}

/* ---------- sidebar ---------- */
function renderSidebar() {
  var list = document.getElementById("chapter-list");
  list.innerHTML = "";
  var doneCount = 0, checkable = 0;
  state.content.chapters.forEach(function (ch) {
    var lock = lockOf(ch);
    var chEl = el("div", "chapter" + (ch._open ? " open" : "") + (lock.locked ? " locked" : ""));
    var head = el("div", "chapter-head");
    head.appendChild(el("span", "chapter-num", String(ch.number)));
    var ct = el("span", "chapter-title", ch.title);
    ct.title = ch.title;
    head.appendChild(ct);
    var total = 0, done = 0;
    ch.items.forEach(function (i) {
      if (i.type === "task" || i.type === "quiz") { total++; checkable++; if (isDone(i.id)) { done++; doneCount++; } }
    });
    if (lock.locked) head.appendChild(el("span", "chapter-lock", "🔒"));
    head.appendChild(el("span", "chapter-count", done + "/" + total));
    head.onclick = function () { ch._open = !ch._open; renderSidebar(); };
    chEl.appendChild(head);
    var bar = el("div", "chapter-bar");
    var barFill = el("i");
    barFill.style.width = total ? (done / total * 100) + "%" : "0";
    bar.appendChild(barFill);
    chEl.appendChild(bar);
    if (lock.locked && ch._open) {
      chEl.appendChild(el("div", "lock-note", lockMessage(ch)));
    }

    var items = el("div", "chapter-items");
    ch.items.forEach(function (it) {
      var row = el("div", "item-row" + (isDone(it.id) ? " done" : "")
        + (state.currentId === it.id ? " active" : "")
        + (lock.locked ? " locked" : ""));
      var chk = el("span", "item-check", "✓");
      row.appendChild(chk);
      var itt = el("span", "item-title", it.title);
      itt.title = it.title;
      row.appendChild(itt);
      if (it.boss) {
        row.appendChild(el("span", "item-kind item-boss", "boss"));
      } else {
        row.appendChild(el("span", "item-kind", it.type === "lesson" ? "lesson" : it.type === "quiz" ? "quiz" : "task"));
      }
      if (lock.locked) {
        row.onclick = function () { showToast(lockMessage(ch)); };
      } else {
        row.onclick = function () { navigate(it.id); };
      }
      items.appendChild(row);
    });
    chEl.appendChild(items);
    list.appendChild(chEl);
  });
  var pct = checkable ? Math.round(doneCount / checkable * 100) : 0;
  document.getElementById("overall-fill").style.width = pct + "%";
  document.getElementById("overall-label").textContent = pct + "%";
}

/* ---------- breadcrumb / navigation ---------- */
function renderTopbar() {
  var bc = document.getElementById("breadcrumb");
  bc.innerHTML = "";
  if (state.view === "dashboard") {
    bc.innerHTML = "<b>Home</b>";
    return;
  }
  var ref = ITEM_MAP[state.currentId];
  if (!ref) return;
  bc.innerHTML = "";
  bc.appendChild(el("span", null, "Chapter " + ref.chapter.number + " - " + ref.chapter.title));
  bc.appendChild(el("span", null, " › "));
  var b = el("b", null, ref.item.title);
  bc.appendChild(b);
  var idx = ITEMS.indexOf(ref.item);
  document.getElementById("prev-item").disabled = idx <= 0;
  document.getElementById("next-item").disabled = idx >= ITEMS.length - 1;
}

function navigate(id) {
  state.currentId = id;
  state.hintLevel = 0;
  var ref = ITEM_MAP[id];
  if (!ref) { state.view = "dashboard"; renderAll(); return; }
  if (lockOf(ref.chapter).locked) {
    showToast(lockMessage(ref.chapter));
    state.view = "dashboard";
    renderAll();
    return;
  }
  ref.chapter._open = true;
  state.view = ref.item.type;
  call("save_progress", { last_task_id: id });
  renderAll();
}

function stepItem(dir) {
  var ref = ITEM_MAP[state.currentId];
  var idx = ref ? ITEMS.indexOf(ref.item) : -1;
  var next = ITEMS[idx + dir];
  if (next) navigate(next.id);
}

function renderAll() {
  renderSidebar();
  renderTopbar();
  var v = document.getElementById("view");
  v.innerHTML = "";
  if (state.view === "dashboard") renderDashboard(v);
  else if (state.view === "lesson") renderLesson(v, ITEM_MAP[state.currentId].item);
  else if (state.view === "quiz") renderQuiz(v, ITEM_MAP[state.currentId].item);
  else if (state.view === "task") renderTask(v, ITEM_MAP[state.currentId].item);
}

/* ---------- dashboard ---------- */
function renderDashboard(v) {
  var d = el("div", "dash");
  var s = state.stats || {};
  var t = s.totals || {};
  d.appendChild(el("div", "eyebrow", "Your progress"));
  var h1 = el("h1", "page-title");
  h1.innerHTML = 'Keep <span class="hl">grinding</span>';
  d.appendChild(h1);
  d.appendChild(el("div", "sub",
    "Level " + (s.level || 0) + " - " + ((s.rank || {}).name || "Novice") +
    " - learn Python through interactive tasks."));

  var achUnlocked = (s.achievements || []).filter(function (a) { return a.unlocked; }).length;
  var grid = el("div", "stat-grid");
  function stat(num, lbl, bar) {
    var c = el("div", "card stat");
    var n = el("div", "num"); n.innerHTML = num;
    c.appendChild(n);
    c.appendChild(el("div", "lbl", lbl));
    if (bar !== undefined) {
      var mb = el("div", "mini-bar");
      var f = document.createElement("i");
      f.style.width = Math.min(100, Math.round(bar * 100)) + "%";
      mb.appendChild(f);
      c.appendChild(mb);
    }
    grid.appendChild(c);
  }
  stat(fmtNum(s.xp || 0), "XP total");
  stat("LV " + (s.level || 0), "Level");
  stat(((s.streak || {}).count || 0) + '<span class="small">d</span>', "Streak");
  stat((t.tasks_done || 0) + '<span class="small">/' + (t.tasks_total || 0) + "</span>", "Tasks done");
  stat((t.quizzes_done || 0) + '<span class="small">/' + (t.quizzes_total || 0) + "</span>", "Quizzes");
  stat(String(t.chapters_cleared || 0) + '<span class="small">/' + (state.content ? state.content.chapters.length : 20) + '</span>', "Chapters cleared");
  stat(fmtNum(s.today_xp || 0) + '<span class="small">/' + fmtNum(s.daily_goal || 300) + "</span>",
       "Today - daily goal", (s.today_xp || 0) / (s.daily_goal || 300));
  stat(achUnlocked + '<span class="small">/10</span>', "Achievements");
  d.appendChild(grid);

  var lastId = state.progress.last_task_id;
  if (lastId && ITEM_MAP[lastId]) {
    var cc = el("div", "card continue-card");
    var grow = el("div", "grow");
    grow.appendChild(el("div", "label", "Continue where you left off"));
    var ref = ITEM_MAP[lastId];
    grow.appendChild(el("div", "title", "Chapter " + ref.chapter.number + " - " + ref.item.title));
    cc.appendChild(grow);
    var go = el("button", "btn btn-primary", "Continue");
    go.onclick = function () { navigate(lastId); };
    cc.appendChild(go);
    d.appendChild(cc);
  }

  /* rang-leiter */
  var rt = el("div", "section-title");
  rt.innerHTML = 'Rank <span class="hl">ladder</span>';
  d.appendChild(rt);
  var track2 = el("div", "rank-track");
  (s.ranks || []).forEach(function (r, i, all) {
    var cur = (s.rank || {}).name === r.name;
    var step = el("div", "rank-step" + (cur ? " current" : (s.level || 0) >= r.min_level ? " done" : ""));
    var hi = (i + 1 < all.length) ? "-" + (all[i + 1].min_level - 1) : "+";
    step.appendChild(el("div", "lvl", "LV " + r.min_level + hi));
    step.appendChild(el("div", "name", r.name));
    step.appendChild(el("div", "desc", r.desc));
    track2.appendChild(step);
  });
  d.appendChild(track2);

  /* achievements */
  var at = el("div", "section-title");
  at.innerHTML = 'Achi<span class="hl">eve</span>ments';
  d.appendChild(at);
  var ag = el("div", "ach-grid");
  (s.achievements || []).forEach(function (a) {
    var c = el("div", "card ach-card" + (a.unlocked ? " unlocked" : ""));
    c.appendChild(el("div", "a-title", a.title));
    c.appendChild(el("div", "a-desc", a.desc));
    c.appendChild(el("div", "a-xp", "+" + a.xp + " XP"));
    ag.appendChild(c);
  });
  d.appendChild(ag);

  /* letzte aktivität */
  var et = el("div", "section-title");
  et.innerHTML = 'Recent <span class="hl">activity</span>';
  d.appendChild(et);
  var evs = el("div", "event-list");
  if ((s.recent_events || []).length) {
    s.recent_events.forEach(function (e) {
      var row = el("div", "event-row");
      row.appendChild(el("div", "e-xp", "+" + e.xp));
      row.appendChild(el("div", "e-note", e.note || e.item_id || ""));
      row.appendChild(el("div", "e-kind", e.kind));
      evs.appendChild(row);
    });
  } else {
    evs.appendChild(el("div", "event-empty", "No XP earned yet - complete a task to get started."));
  }
  d.appendChild(evs);

  var ct = el("div", "section-title");
  ct.innerHTML = 'Chap<span class="hl">ters</span>';
  d.appendChild(ct);
  var grid = el("div", "chapter-grid");
  state.content.chapters.forEach(function (ch) {
    var lock = lockOf(ch);
    var c = el("div", "card chapter-card" + (lock.locked ? " locked" : ""));
    c.appendChild(el("div", "num", "Chapter " + ch.number + (lock.locked ? " 🔒" : "")));
    c.appendChild(el("h3", null, ch.title));
    c.appendChild(el("p", null, ch.summary || ""));
    var total = 0, dn = 0;
    ch.items.forEach(function (i) {
      if (i.type === "task" || i.type === "quiz") { total++; if (isDone(i.id)) dn++; }
    });
    if (lock.locked) {
      c.appendChild(el("div", "lock-note", lockMessage(ch)));
      // dünner balken zeigt den fortschritt im vorgänger-kapitel
      var prev = chapterById(lock.prev_id);
      var pdn = 0, ptot = 0;
      if (prev) prev.items.forEach(function (i) {
        ptot++; if (isDone(i.id)) pdn++;
      });
      var ptrack = el("div", "progress-track");
      var pfill = el("div", "progress-fill");
      pfill.style.width = (lock.pct || 0) + "%";
      ptrack.appendChild(pfill);
      var pw = el("div", "prev-progress");
      pw.appendChild(el("div", "prev-label", (prev ? prev.title : "Previous chapter") + " - " + (lock.pct || 0) + "%"));
      pw.appendChild(ptrack);
      c.appendChild(pw);
    } else {
      var track = el("div", "progress-track");
      var fill = el("div", "progress-fill");
      fill.style.width = total ? (dn / total * 100) + "%" : "0";
      track.appendChild(fill);
      c.appendChild(track);
      c.onclick = function () {
        ch._open = true;
        navigate(ch.items[0].id);
      };
    }
    grid.appendChild(c);
  });
  d.appendChild(grid);
  v.appendChild(d);
}

/* ---------- lesson ---------- */
function highlightCode(codeEl) {
  var src = codeEl.textContent;
  codeEl.parentElement.classList.add("cm-s-default");
  try {
    CodeMirror.runMode(src, "python", codeEl);
  } catch (e) { /* dann halt einfach plain text */ }
  return src;
}

function attachRunButtons(container) {
  container.querySelectorAll("pre code").forEach(function (code) {
    var pre = code.parentElement;
    if (!/\bpython\b|language-/.test(code.className) && code.className !== "") return;
    var src = highlightCode(code);
    var wrap = el("div", "code-run");
    var stdinTa = null;
    if (/\binput\s*\(/.test(src)) {
      var stdinRow = el("div", "stdin-row");
      stdinRow.appendChild(el("div", "stdin-label", "Program input - one line per input() call"));
      stdinTa = document.createElement("textarea");
      stdinTa.spellcheck = false;
      stdinRow.appendChild(stdinTa);
      wrap.appendChild(stdinRow);
    }
    var btn = el("button", "btn", "Run");
    var out = null;
    btn.onclick = function () {
      btnLoading(btn, true);
      call("run_code", { code: src, stdin_text: stdinTa ? stdinTa.value : "" }).then(function (res) {
        btnLoading(btn, false, "Run");
        if (!out) {
          out = el("div", "code-output");
          wrap.appendChild(out);
        }
        var html = "";
        if (res.stdout) html += escapeHtml(res.stdout);
        if (res.friendly) html += friendlyHtml(res.friendly);
        if (res.stderr) html += '<span class="err">' + escapeHtml(res.stderr) + "</span>";
        if (!html) html = "(no output)";
        out.innerHTML = html;
      });
    };
    wrap.appendChild(btn);
    pre.parentNode.insertBefore(wrap, pre.nextSibling);
  });
}

function escapeHtml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function renderLesson(v, item) {
  var d = el("div", "lesson");
  d.appendChild(el("h1", null, item.title));
  var body = el("div", "md");
  body.innerHTML = md(item.body);
  d.appendChild(body);
  attachRunButtons(body);

  var readRow = el("div", "read-btn-row");
  if (isDone(item.id)) {
    readRow.appendChild(el("span", "read-done", "✓ Read"));
  } else {
    var readBtn = el("button", "btn", "Mark as read - +20 XP");
    readBtn.onclick = function () {
      btnLoading(readBtn, true, "Saving...");
      call("mark_lesson_read", { item_id: item.id }).then(function (res) {
        btnLoading(readBtn, false);
        if (res.reward) showReward(res.reward);
        applyStats(res.stats);
        state.progress.completed[item.id] = new Date().toISOString();
        readRow.innerHTML = "";
        readRow.appendChild(el("span", "read-done", "✓ Read"));
        renderSidebar();
      });
    };
    readRow.appendChild(readBtn);
  }
  d.appendChild(readRow);
  v.appendChild(d);
}

/* ---------- quiz ---------- */
function renderQuiz(v, item) {
  var d = el("div", "quiz");
  d.appendChild(el("h1", null, item.title));
  var q = el("div", "question");
  q.innerHTML = md(item.question);
  d.appendChild(q);

  var selected = null;
  var locked = false;
  var prior = (state.progress.quiz || {})[item.id];

  var optsBox = el("div");
  var optEls = [];
  item.options.forEach(function (opt, i) {
    var o = el("label", "option" + (prior === i ? " selected" : ""));
    var r = document.createElement("input");
    r.type = "radio"; r.name = item.id; r.style.display = "none";
    o.appendChild(r);
    o.appendChild(document.createTextNode(opt));
    o.onclick = function () {
      if (locked) return;
      optEls.forEach(function (x) { x.classList.remove("selected"); });
      o.classList.add("selected");
      selected = i;
    };
    if (prior === i) selected = i;
    optEls.push(o);
    optsBox.appendChild(o);
  });
  d.appendChild(optsBox);

  var checkBtn = el("button", "btn btn-primary", "Check answer");
  var expl = el("div");
  checkBtn.onclick = function () {
    if (selected === null || locked) return;
    call("check_quiz", { item_id: item.id, choice: selected }).then(function (res) {
      if (res.error) { expl.textContent = res.error === "locked" ? res.message : res.error; return; }
      if (res.reward) showReward(res.reward);
      applyStats(res.stats);
      locked = true;
      optEls.forEach(function (o) { o.classList.add("locked"); });
      optEls[res.answer].classList.add("correct");
      if (!res.correct) optEls[selected].classList.add("incorrect");
      expl.innerHTML = "";
      var box = el("div", "explanation");
      box.innerHTML = md(res.explanation || (res.correct ? "Correct." : "Not quite."));
      expl.appendChild(box);
      if (res.correct) {
        state.progress.completed[item.id] = new Date().toISOString();
        renderSidebar();
        checkBtn.textContent = "Correct!";
        checkBtn.disabled = true;
        setTimeout(function () { locked = false; }, 0);
      } else {
        locked = false;
        optEls.forEach(function (o) { o.classList.remove("locked"); });
      }
    });
  };
  d.appendChild(checkBtn);
  d.appendChild(expl);
  v.appendChild(d);
}

/* ---------- task ---------- */
function renderTask(v, item) {
  var wrap = el("div", "task-wrap");
  var left = el("div", "task-left");
  var right = el("div", "task-right");

  var titleRow = el("div", "task-title-row");
  titleRow.appendChild(el("h1", null, item.title));
  if (item.boss) titleRow.appendChild(el("span", "boss-tag", "Boss"));
  if (item.xp) titleRow.appendChild(el("span", "xp-tag", item.xp + " XP"));
  left.appendChild(titleRow);
  left.appendChild(el("div", "difficulty", "Difficulty " + "●".repeat(item.difficulty || 1) + "○".repeat(3 - (item.difficulty || 1))));

  if (item.plain) {
    var plain = el("div", "plain-callout");
    plain.appendChild(el("span", "callout-title", "In plain words"));
    plain.appendChild(el("span", null, " " + item.plain));
    left.appendChild(plain);
  }

  var instr = el("div", "md");
  instr.innerHTML = md(item.instructions);
  left.appendChild(instr);

  if (item.tests && item.tests.length) {
    var det = el("details", "collapsible");
    det.appendChild(el("summary", null, "What is checked (" + item.tests.length + ")"));
    var inner = el("div", "inner");
    var ul = el("ul");
    item.tests.forEach(function (t) { ul.appendChild(el("li", null, t.desc || "test")); });
    inner.appendChild(ul);
    det.appendChild(inner);
    left.appendChild(det);
  }

  // gelöstes beispiel - kostet nix, gucken erlaubt
  if (item.example) {
    var exDet = el("details", "collapsible example-card");
    exDet.appendChild(el("summary", null, "Similar solved example"));
    var exInner = el("div", "inner");
    exInner.appendChild(el("div", "example-note",
      "Same idea, different numbers - no penalty for looking"));
    var exBody = el("div", "md");
    exBody.innerHTML = md(item.example);
    exInner.appendChild(exBody);
    exDet.appendChild(exInner);
    left.appendChild(exDet);
  }

  // hints (kommen einzeln vom backend - kosten ja xp)
  var hintCount = item.hint_count || 0;
  var hintDet = el("details", "collapsible");
  hintDet.open = true;
  hintDet.appendChild(el("summary", null, "Hints (" + hintCount + ")"));
  var hintInner = el("div", "inner");
  var hintList = el("ol", "hint-list");
  var hintBtn = el("button", "btn hint-btn", "Show hint 1 of " + hintCount);
  hintBtn.onclick = function () {
    if (state.hintLevel >= hintCount) return;
    var next = state.hintLevel + 1;
    hintBtn.disabled = true;
    call("use_hint", { task_id: item.id, level: next }).then(function (res) {
      hintBtn.disabled = false;
      if (res.error === "locked") { showToast(res.message); return; }
      if (res.error || !res.hint) return;
      var li = el("li");
      li.innerHTML = md(res.hint);
      hintList.appendChild(li);
      state.hintLevel = next;
      hintBtn.textContent = state.hintLevel < hintCount
        ? "Show hint " + (state.hintLevel + 1) + " of " + hintCount
        : "No more hints";
      if (state.hintLevel >= hintCount) hintBtn.disabled = true;
    });
  };
  hintInner.appendChild(hintList);
  if (hintCount) hintInner.appendChild(hintBtn);
  hintInner.appendChild(el("div", "hint-note", "Each hint -10% XP on this task"));
  hintDet.appendChild(hintInner);
  left.appendChild(hintDet);

  var solBtn = el("button", "btn", "Show solution");
  var showIt = function () {
      call("get_solution", { task_id: item.id }).then(function (res) {
        if (res.error === "locked") { showToast(res.message); return; }
        if (!res.solution) return;
        var card = el("div", "card sol-card");
        var head = el("div", "sol-head");
        head.appendChild(el("span", "sol-title", "Reference solution (read-only)"));
        var acts = el("div", "sol-actions");
        var copyBtn = el("button", "btn btn-mini", "Copy");
        copyBtn.onclick = function () {
          copyText(res.solution).then(function () { showToast("Copied"); });
        };
        var loadBtn = el("button", "btn btn-mini", "Load into editor");
        loadBtn.onclick = function () {
          var put = function () {
            cm.setValue(res.solution);
            call("save_draft", { task_id: item.id, code: res.solution });
            showToast("Solution loaded into the editor");
          };
          var cur = cm.getValue();
          if (cur.trim() && cur !== (item.starter || "")) {
            modal("Load solution?",
              "Replace your code with the reference solution?",
              "Replace").then(function (ok) { if (ok) put(); });
          } else put();
        };
        acts.appendChild(copyBtn);
        acts.appendChild(loadBtn);
        head.appendChild(acts);
        card.appendChild(head);
        var pre = el("pre", "sol-pre");
        var code = el("code", "language-python");
        code.textContent = res.solution;
        pre.appendChild(code);
        highlightCode(code);
        card.appendChild(pre);
        if (res.explanation) {
          var hw = el("div", "how-works");
          hw.innerHTML = '<div class="eyebrow">How it <span style="color:var(--red)">works</span></div>' + md(res.explanation);
          card.appendChild(hw);
        }
        left.appendChild(card);
        solBtn.disabled = true;
      });
    };
  solBtn.onclick = function () {
    if (!isDone(item.id)) {
      modal("Show solution?", "This task is not completed yet. Viewing the solution reduces this task's XP to 40%.", "Show anyway").then(function (ok) {
        if (ok) showIt();
      });
    } else showIt();
  };
  left.appendChild(solBtn);
  if (new URLSearchParams(location.search).get("solution")) showIt();

  // --- rechts: der editor ---
  var toolbar = el("div", "editor-toolbar");
  var checkBtn = el("button", "btn btn-primary", "Check (Ctrl+Shift+Enter)");
  var runBtn = el("button", "btn btn-outline", "Run (Ctrl+Enter)");
  var resetBtn = el("button", "btn btn-ghost", "Reset");
  var stdinToggle = el("button", "btn btn-ghost", "Program input");
  toolbar.appendChild(checkBtn);
  toolbar.appendChild(runBtn);
  toolbar.appendChild(resetBtn);
  toolbar.appendChild(el("span", "spacer"));
  toolbar.appendChild(stdinToggle);
  right.appendChild(toolbar);

  var editorBox = el("div", "editor-box");
  right.appendChild(editorBox);

  var stdinRow = el("div", "stdin-row hidden");
  stdinRow.appendChild(el("div", "stdin-label", "Program input"));
  var stdinTa = document.createElement("textarea");
  stdinTa.spellcheck = false;
  stdinTa.placeholder = "One line per input() call";
  stdinRow.appendChild(stdinTa);
  right.appendChild(stdinRow);
  stdinToggle.onclick = function () { stdinRow.classList.toggle("hidden"); };

  var panel = el("div", "bottom-panel");
  var tabs = el("div", "panel-tabs");
  var outTab = el("div", "panel-tab active", "Output");
  var resTab = el("div", "panel-tab", "Results");
  tabs.appendChild(outTab); tabs.appendChild(resTab);
  panel.appendChild(tabs);
  var body = el("div", "panel-body");
  var outPane = el("div", "output-pane");
  outPane.innerHTML = '<div class="panel-empty">Run or check your code to see output.</div>';
  var resPane = el("div", "results-pane");
  resPane.innerHTML = '<div class="panel-empty">No results yet - hit Check to run the tests.</div>';
  body.appendChild(outPane);
  panel.appendChild(body);
  outTab.onclick = function () { switchTab(0); };
  resTab.onclick = function () { switchTab(1); };
  function switchTab(i) {
    outTab.classList.toggle("active", i === 0);
    resTab.classList.toggle("active", i === 1);
    body.innerHTML = "";
    body.appendChild(i === 0 ? outPane : resPane);
  }
  right.appendChild(panel);
  wrap.appendChild(left);
  wrap.appendChild(right);
  v.appendChild(wrap);

  // codemirror-editor aufsetzen
  var saved = (state.progress.drafts || {})[item.id];
  var cm = CodeMirror(editorBox, {
    value: saved !== undefined ? saved : (item.starter || ""),
    mode: "python",
    lineNumbers: true,
    indentUnit: 4,
    tabSize: 4,
    indentWithTabs: false,
    autoCloseBrackets: true,
    matchBrackets: true,
    styleActiveLine: true,
    extraKeys: {
      "Ctrl-/": "toggleComment",
      "Ctrl-Enter": function () { doRun(); },
      "Ctrl-Shift-Enter": function () { doCheck(); },
      "Tab": function (cm) {
        if (cm.somethingSelected()) cm.indentSelection("add");
        else cm.replaceSelection("    ");
      },
    },
  });
  state.editor = cm;
  setTimeout(function () { cm.refresh(); }, 50);
  cm.on("change", function () {
    clearTimeout(state.draftTimer);
    state.draftTimer = setTimeout(function () {
      call("save_draft", { task_id: item.id, code: cm.getValue() });
    }, 800);
  });

  resetBtn.onclick = function () {
    modal("Reset code?", "Replace the editor content with the starter code? Your current draft will be lost.", "Reset").then(function (ok) {
      if (ok) { cm.setValue(item.starter || ""); call("save_draft", { task_id: item.id, code: item.starter || "" }); }
    });
  };

  function showRun(res) {
    var html = "";
    if (res.stdout) html += escapeHtml(res.stdout);
    if (res.friendly) html += friendlyHtml(res.friendly);
    if (res.stderr) html += '<span class="stderr">' + escapeHtml(res.stderr) + "</span>";
    if (!html) html = "(no output)";
    html += '<div class="output-meta">' + (res.timed_out ? "timed out" : "exit " + res.exit_code) + " - " + res.duration_ms + " ms</div>";
    outPane.innerHTML = html;
    switchTab(0);
  }

  function doRun() {
    if (state.running) return;
    state.running = true;
    btnLoading(runBtn, true);
    var stdin = stdinRow.classList.contains("hidden") ? "" : stdinTa.value;
    call("run_code", { code: cm.getValue(), stdin_text: stdin }).then(function (res) {
      state.running = false;
      btnLoading(runBtn, false, "Run (Ctrl+Enter)");
      showRun(res);
    });
  }

  function showResults(res) {
    resPane.innerHTML = "";
    if (res.error) {
      resPane.appendChild(el("div", "panel-empty",
        res.error === "locked" ? (res.message || "Chapter is locked.") : res.error));
      switchTab(1);
      return;
    }
    (res.results || []).forEach(function (r) {
      var row = el("div", "test-row");
      var head = el("div", "test-head");
      head.appendChild(el("span", "t-mark " + (r.passed ? "pass" : "fail"),
        r.passed ? "✓" : "✗"));
      head.appendChild(el("span", null, r.desc || ""));
      row.appendChild(head);
      if (!r.passed) {
        if (r.expected || r.actual) {
          var diff = el("div", "test-diff");
          var e = el("div"); e.appendChild(el("span", "cap", "Expected"));
          e.appendChild(document.createTextNode(r.expected || "(empty)"));
          var a = el("div"); a.appendChild(el("span", "cap", "Actual"));
          a.appendChild(document.createTextNode(r.actual || "(empty)"));
          diff.appendChild(e); diff.appendChild(a);
          row.appendChild(diff);
        }
        if (r.friendly) {
          var fr = el("div", "friendly-note");
          fr.innerHTML = friendlyHtml(r.friendly);
          row.appendChild(fr);
        }
        if (r.error) row.appendChild(el("div", "test-error", r.error));
      }
      resPane.appendChild(row);
    });
    switchTab(1);
  }

  function doCheck() {
    if (state.running) return;
    state.running = true;
    btnLoading(checkBtn, true, "Checking...");
    var stdin = stdinRow.classList.contains("hidden") ? "" : stdinTa.value;
    void stdin;
    call("check_task", { task_id: item.id, code: cm.getValue() }).then(function (res) {
      state.running = false;
      btnLoading(checkBtn, false, "Check (Ctrl+Shift+Enter)");
      showResults(res);
      if (res.reward) { showReward(res.reward); }
      applyStats(res.stats);
      if (res.passed) {
        state.progress.completed[item.id] = new Date().toISOString();
        renderSidebar();
        var ref = ITEM_MAP[item.id];
        var idx = ITEMS.indexOf(ref.item);
        var next = ITEMS[idx + 1];
        var banner = el("div", "success-banner");
        banner.appendChild(el("span", "grow", "All tests passed - well done!"));
        if (next) {
          var nb = el("button", "btn btn-success", "Next item ->");
          nb.onclick = function () { navigate(next.id); };
          banner.appendChild(nb);
        }
        right.insertBefore(banner, panel);
      }
    });
  }

  runBtn.onclick = doRun;
  checkBtn.onclick = doCheck;
}

/* ---------- boot ---------- */
function init() {
  document.getElementById("theme-toggle").onclick = toggleTheme;
  document.getElementById("prev-item").onclick = function () { stepItem(-1); };
  document.getElementById("next-item").onclick = function () { stepItem(1); };
  document.getElementById("sidebar-toggle").onclick = function () {
    document.getElementById("sidebar").classList.add("collapsed");
    document.getElementById("sidebar-open").classList.remove("hidden");
    if (state.editor) setTimeout(function () { state.editor.refresh(); }, 200);
  };
  document.getElementById("sidebar-open").onclick = function () {
    document.getElementById("sidebar").classList.remove("collapsed");
    document.getElementById("sidebar-open").classList.add("hidden");
    if (state.editor) setTimeout(function () { state.editor.refresh(); }, 200);
  };
  document.addEventListener("keydown", function (e) {
    if (e.altKey && e.key === "ArrowLeft") { e.preventDefault(); stepItem(-1); }
    if (e.altKey && e.key === "ArrowRight") { e.preventDefault(); stepItem(1); }
  });

  Promise.all([call("get_content"), call("get_progress"), call("get_stats")]).then(function (rs) {
    state.content = rs[0];
    document.getElementById("sidebar-version").textContent =
      "v" + (state.content.version || "?");
    state.progress = rs[1] || { completed: {}, drafts: {}, quiz: {} };
    state.locks = (rs[0] && rs[0].locks) || (rs[2] && rs[2].locks) || {};
    state.stats = rs[2] || null;
    flatten();
    renderPlayer();
    var qs = new URLSearchParams(location.search);
    var theme = qs.get("theme") || state.progress.theme || "dark";
    applyTheme(theme);
    if (qs.get("theme")) call("save_progress", { theme: theme });
    var itemId = qs.get("item");
    if (itemId && ITEM_MAP[itemId]) {
      navigate(itemId);
    } else {
      state.view = "dashboard";
      renderAll();
    }
    call("get_whats_new").then(showWhatsNew);
  });
}

document.addEventListener("DOMContentLoaded", init);
})();
