/* YC.RUNTIME — interactions */

(() => {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  /* ───────── Boot sequence ───────── */
  const boot = $("#boot");
  const bootLog = $("#boot-log");
  const bootFill = $("#boot-fill");
  const lines = [
    { t: "> boot youngchan.runtime", c: "hi", d: 120 },
    { t: "loading kernel modules…", d: 180 },
    { t: "  ✓ identity          이영찬 / Lee Young-chan", c: "ok", d: 140 },
    { t: "  ✓ path              chem → product → security", c: "ok", d: 140 },
    { t: "  ✓ services          threat-hunt · edu-sim · labs", c: "ok", d: 140 },
    { t: "  ✓ public_repos      50+", c: "ok", d: 120 },
    { t: "  ✓ focus             backend · AppSec · ML interest", c: "ok", d: 160 },
    { t: "mounting portfolio filesystem…", d: 150 },
    { t: "ready. press any key or wait.", c: "warn", d: 80 },
  ];

  function sleep(ms) {
    return new Promise((r) => setTimeout(r, ms));
  }

  async function runBoot() {
    document.body.classList.add("booting");
    let progress = 0;
    for (let i = 0; i < lines.length; i++) {
      const { t, c, d } = lines[i];
      const span = document.createElement("span");
      if (c) span.className = c;
      span.textContent = t + "\n";
      bootLog.appendChild(span);
      progress = Math.round(((i + 1) / lines.length) * 100);
      bootFill.style.width = progress + "%";
      await sleep(d);
    }
    await sleep(420);
    finishBoot();
  }

  function finishBoot() {
    if (!boot || boot.classList.contains("is-done")) return;
    boot.classList.add("is-done");
    document.body.classList.remove("booting");
    // stagger hero reveals immediately after boot
    requestAnimationFrame(() => {
      $$(".hero .reveal").forEach((el, i) => {
        setTimeout(() => el.classList.add("is-in"), 80 + i * 90);
      });
    });
  }

  // skip on click / key
  function skipBoot() {
    if (boot && !boot.classList.contains("is-done")) finishBoot();
  }

  /* ───────── Year ───────── */
  const y = $("#y");
  if (y) y.textContent = String(new Date().getFullYear());

  /* ───────── Nav solid on scroll ───────── */
  const nav = $("#nav");
  function onScrollNav() {
    if (!nav) return;
    nav.classList.toggle("is-solid", window.scrollY > 24);
  }

  /* ───────── Cursor glow ───────── */
  const glow = $("#cursor-glow");
  let glowRaf = null;
  let gx = 0, gy = 0, tx = 0, ty = 0;

  function moveGlow(e) {
    tx = e.clientX;
    ty = e.clientY;
    if (!glowRaf) glowRaf = requestAnimationFrame(tickGlow);
  }

  function tickGlow() {
    gx += (tx - gx) * 0.12;
    gy += (ty - gy) * 0.12;
    if (glow) glow.style.transform = `translate(${gx}px, ${gy}px) translate(-50%, -50%)`;
    if (Math.abs(tx - gx) > 0.3 || Math.abs(ty - gy) > 0.3) {
      glowRaf = requestAnimationFrame(tickGlow);
    } else {
      glowRaf = null;
    }
  }

  /* ───────── Scroll reveal ───────── */
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          en.target.classList.add("is-in");
          io.unobserve(en.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  function observeReveals() {
    $$(".reveal").forEach((el) => {
      if (el.closest(".hero")) return; // hero handled after boot
      io.observe(el);
    });
  }

  /* ───────── Type swap words ───────── */
  const swapEl = $("#type-swap");
  const words = ["서버", "코드", "제품", "방어", "도구"];
  let wi = 0;

  function cycleWord() {
    if (!swapEl) return;
    wi = (wi + 1) % words.length;
    swapEl.style.opacity = "0";
    swapEl.style.transform = "translateY(6px)";
    setTimeout(() => {
      swapEl.textContent = words[wi];
      swapEl.style.opacity = "1";
      swapEl.style.transform = "none";
    }, 220);
  }

  if (swapEl) {
    swapEl.style.transition = "opacity 0.22s ease, transform 0.22s ease";
    setInterval(cycleWord, 2600);
  }

  /* ───────── Hero canvas network ───────── */
  const canvas = $("#hero-canvas");
  let ctx, particles = [], animId, w = 0, h = 0, dpr = 1;

  function resizeCanvas() {
    if (!canvas) return;
    const parent = canvas.parentElement;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = parent.clientWidth;
    h = parent.clientHeight;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = w + "px";
    canvas.style.height = h + "px";
    ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    seedParticles();
  }

  function seedParticles() {
    const count = Math.min(70, Math.floor((w * h) / 14000));
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      r: Math.random() * 1.6 + 0.6,
    }));
  }

  function drawNetwork() {
    if (!ctx) return;
    ctx.clearRect(0, 0, w, h);
    const linkDist = 130;

    for (const p of particles) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > w) p.vx *= -1;
      if (p.y < 0 || p.y > h) p.vy *= -1;
    }

    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const a = particles[i], b = particles[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const dist = Math.hypot(dx, dy);
        if (dist < linkDist) {
          const alpha = (1 - dist / linkDist) * 0.28;
          ctx.strokeStyle = `rgba(61, 224, 255, ${alpha})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    for (const p of particles) {
      ctx.beginPath();
      ctx.fillStyle = "rgba(139, 124, 255, 0.75)";
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }

    animId = requestAnimationFrame(drawNetwork);
  }

  /* ───────── Command palette ───────── */
  const cmd = $("#cmd");
  const cmdInput = $("#cmd-input");
  const cmdList = $("#cmd-list");
  const cmdOut = $("#cmd-out");
  let cmdIndex = 0;

  const COMMANDS = [
    { key: "whoami", desc: "소개 한 줄", run: () => printOut("이영찬 — 현장의 문제를 서버·제품·방어로 푸는 엔지니어\nGitHub: JimProKing · 국세청 전산직 · Flutter 10+ 출시") },
    { key: "projects", desc: "프로젝트 섹션으로", run: () => { closeCmd(); location.hash = "#work"; } },
    { key: "story", desc: "스토리 섹션으로", run: () => { closeCmd(); location.hash = "#story"; } },
    { key: "stack", desc: "기술 스택", run: () => { closeCmd(); location.hash = "#stack"; } },
    { key: "github", desc: "GitHub 열기", run: () => window.open("https://github.com/JimProKing", "_blank", "noopener") },
    { key: "email", desc: "메일 보내기", run: () => { location.href = "mailto:caramel2516@naver.com"; } },
    { key: "aegis", desc: "Aegis Cortex 저장소", run: () => window.open("https://github.com/JimProKing/aegis-cortex", "_blank", "noopener") },
    { key: "contact", desc: "연락처 섹션", run: () => { closeCmd(); location.hash = "#contact"; } },
    { key: "clear", desc: "출력 지우기", run: () => { cmdOut.textContent = ""; } },
    { key: "help", desc: "명령어 목록", run: () => printOut(COMMANDS.map((c) => c.key.padEnd(12) + c.desc).join("\n")) },
  ];

  function printOut(text) {
    cmdOut.textContent = text;
  }

  function openCmd() {
    if (!cmd) return;
    cmd.hidden = false;
    cmdInput.value = "";
    cmdOut.textContent = "";
    cmdIndex = 0;
    renderCmdList("");
    setTimeout(() => cmdInput.focus(), 10);
  }

  function closeCmd() {
    if (!cmd) return;
    cmd.hidden = true;
  }

  function filtered(q) {
    const s = q.trim().toLowerCase();
    if (!s) return COMMANDS;
    return COMMANDS.filter((c) => c.key.includes(s) || c.desc.includes(s));
  }

  function renderCmdList(q) {
    const items = filtered(q);
    cmdList.innerHTML = items
      .map(
        (c, i) =>
          `<li data-i="${i}" class="${i === cmdIndex ? "is-active" : ""}">
            <span class="cmd-key">${c.key}</span>
            <span class="cmd-desc">${c.desc}</span>
          </li>`
      )
      .join("");
    $$("#cmd-list li").forEach((li) => {
      li.addEventListener("mouseenter", () => {
        cmdIndex = Number(li.dataset.i);
        highlight();
      });
      li.addEventListener("click", () => runSelected());
    });
  }

  function highlight() {
    $$("#cmd-list li").forEach((li, i) => li.classList.toggle("is-active", i === cmdIndex));
  }

  function runSelected() {
    const items = filtered(cmdInput.value);
    const item = items[cmdIndex] || items.find((c) => c.key === cmdInput.value.trim().toLowerCase());
    if (item) item.run();
    else if (cmdInput.value.trim()) printOut(`command not found: ${cmdInput.value.trim()}\ntry: help`);
  }

  function onCmdKey(e) {
    if (cmd.hidden) return;
    const items = filtered(cmdInput.value);
    if (e.key === "Escape") {
      e.preventDefault();
      closeCmd();
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      cmdIndex = Math.min(cmdIndex + 1, items.length - 1);
      highlight();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      cmdIndex = Math.max(cmdIndex - 1, 0);
      highlight();
    } else if (e.key === "Enter") {
      e.preventDefault();
      runSelected();
    }
  }

  /* ───────── Global shortcuts ───────── */
  function onKey(e) {
    const meta = e.metaKey || e.ctrlKey;
    if (meta && e.key.toLowerCase() === "k") {
      e.preventDefault();
      if (cmd.hidden) openCmd();
      else closeCmd();
      return;
    }
    if (document.body.classList.contains("booting")) {
      skipBoot();
    }
  }

  /* ───────── Init ───────── */
  function init() {
    // reduced motion: skip long boot
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) {
      finishBoot();
    } else {
      runBoot();
      boot?.addEventListener("click", skipBoot);
    }

    window.addEventListener("scroll", onScrollNav, { passive: true });
    onScrollNav();

    window.addEventListener("mousemove", moveGlow, { passive: true });

    observeReveals();

    if (canvas && !reduce) {
      resizeCanvas();
      drawNetwork();
      window.addEventListener("resize", () => {
        cancelAnimationFrame(animId);
        resizeCanvas();
        drawNetwork();
      });
    }

    $("#cmd-open")?.addEventListener("click", openCmd);
    $("#hero-cmd")?.addEventListener("click", openCmd);
    cmd?.querySelector("[data-close]")?.addEventListener("click", closeCmd);
    cmdInput?.addEventListener("input", () => {
      cmdIndex = 0;
      renderCmdList(cmdInput.value);
    });
    window.addEventListener("keydown", onKey);
    window.addEventListener("keydown", onCmdKey);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
