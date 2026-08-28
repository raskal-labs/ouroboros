const $ = id => document.getElementById(id);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const STORAGE_KEY = "ouroborosPoseEditor.ui.v1";

const defaults = {
  opacity: 0.62,
  floating: false,
  scale: 1,
  sheetHeight: null,
  floatingLeft: 14,
  floatingBottom: 14,
  floatingWidth: 390,
  floatingHeight: 540,
  menuLeft: null,
  menuTop: null,
  menuWidth: 210,
  menuHeight: null
};

let state = {...defaults};
try {
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
  if (saved && typeof saved === "object") state = {...state, ...saved};
} catch (_) {}

function save() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (_) {}
}

function applyState() {
  const root = document.documentElement;
  root.style.setProperty("--ui-panel-alpha", clamp(+state.opacity || defaults.opacity, .18, 1));
  root.style.setProperty("--ui-panel-scale", clamp(+state.scale || 1, .7, 1.35));
  document.body.classList.toggle("panel-floating", !!state.floating);

  const sheet = $("sheet");
  if (sheet) {
    if (!state.floating && Number.isFinite(state.sheetHeight)) {
      sheet.style.height = `${clamp(state.sheetHeight, 54, innerHeight - 90)}px`;
      sheet.classList.add("expanded");
    } else if (!state.floating) {
      sheet.style.height = "";
    }
    if (state.floating) {
      root.style.setProperty("--floating-left", `${clamp(state.floatingLeft, 0, Math.max(0, innerWidth - 100))}px`);
      root.style.setProperty("--floating-bottom", `${clamp(state.floatingBottom, 0, Math.max(0, innerHeight - 100))}px`);
      root.style.setProperty("--floating-width", `${clamp(state.floatingWidth, 260, Math.max(280, innerWidth - 10))}px`);
      root.style.setProperty("--floating-height", `${clamp(state.floatingHeight, 180, Math.max(220, innerHeight - 20))}px`);
      sheet.classList.add("expanded");
      const chevron = $("handleChevron");
      if (chevron) chevron.textContent = "⋮";
    }
  }

  const menu = $("menu");
  if (menu) {
    menu.style.width = `${clamp(state.menuWidth || 210, 190, Math.max(200, innerWidth - 12))}px`;
    if (Number.isFinite(state.menuHeight)) menu.style.height = `${clamp(state.menuHeight, 100, Math.max(120, innerHeight - 20))}px`;
    if (Number.isFinite(state.menuLeft) && Number.isFinite(state.menuTop)) {
      menu.style.left = `${clamp(state.menuLeft, 6, Math.max(6, innerWidth - 120))}px`;
      menu.style.top = `${clamp(state.menuTop, 6, Math.max(6, innerHeight - 80))}px`;
      menu.style.right = "auto";
    }
  }
}

function installInterfaceControls() {
  const body = $("sheetBody");
  if (!body || $("interfaceControls")) return;
  const section = document.createElement("div");
  section.id = "interfaceControls";
  section.className = "section";
  section.innerHTML = `
    <div class="sectionTitle">Interface</div>
    <div class="subtle">Panel opacity affects backgrounds, not control/text legibility.</div>
    <div class="uiCompactRow">
      <label for="uiOpacity">UI opacity</label>
      <input id="uiOpacity" type="range" min="0.18" max="1" step="0.01" value="${state.opacity}">
      <input id="uiOpacityNumber" type="number" min="0.18" max="1" step="0.01" value="${state.opacity.toFixed(2)}" aria-label="Exact UI opacity">
    </div>
    <div class="uiCompactRow">
      <label for="uiScale">Panel scale</label>
      <input id="uiScale" type="range" min="0.70" max="1.35" step="0.05" value="${state.scale}">
      <input id="uiScaleNumber" type="number" min="0.70" max="1.35" step="0.05" value="${state.scale.toFixed(2)}" aria-label="Exact panel scale">
    </div>
    <div class="uiButtonRow">
      <button id="panelModeToggle" type="button">${state.floating ? "Dock panel" : "Float panel"}</button>
      <button id="resetInterface" type="button">Reset UI</button>
    </div>`;
  body.appendChild(section);

  const opacity = $("uiOpacity"), opacityNum = $("uiOpacityNumber");
  const scale = $("uiScale"), scaleNum = $("uiScaleNumber");

  const setOpacity = value => {
    state.opacity = clamp(Number(value), .18, 1);
    opacity.value = state.opacity;
    opacityNum.value = state.opacity.toFixed(2);
    applyState(); save();
  };
  const setScale = value => {
    state.scale = clamp(Number(value), .7, 1.35);
    scale.value = state.scale;
    scaleNum.value = state.scale.toFixed(2);
    applyState(); save();
  };
  opacity.addEventListener("input", () => setOpacity(opacity.value));
  opacityNum.addEventListener("change", () => setOpacity(opacityNum.value));
  scale.addEventListener("input", () => setScale(scale.value));
  scaleNum.addEventListener("change", () => setScale(scaleNum.value));

  $("panelModeToggle").addEventListener("click", () => {
    const sheet = $("sheet");
    if (state.floating && sheet) {
      state.floatingWidth = sheet.offsetWidth;
      state.floatingHeight = sheet.offsetHeight;
    }
    state.floating = !state.floating;
    $("panelModeToggle").textContent = state.floating ? "Dock panel" : "Float panel";
    applyState(); save();
  });

  $("resetInterface").addEventListener("click", () => {
    state = {...defaults};
    opacity.value = state.opacity;
    opacityNum.value = state.opacity.toFixed(2);
    scale.value = state.scale;
    scaleNum.value = state.scale.toFixed(2);
    $("panelModeToggle").textContent = "Float panel";
    const sheet = $("sheet");
    const menu = $("menu");
    if (sheet) { sheet.style.height = ""; sheet.style.width = ""; }
    if (menu) { menu.style.height = ""; menu.style.left = ""; menu.style.top = ""; menu.style.right = ""; }
    applyState(); save();
  });
}

function installSheetResize() {
  const sheet = $("sheet");
  if (!sheet || $("sheetResizeHandle")) return;
  const handle = document.createElement("div");
  handle.id = "sheetResizeHandle";
  handle.setAttribute("aria-label", "Resize controls panel");
  sheet.appendChild(handle);
  let startY = 0, startHeight = 0, active = false;
  handle.addEventListener("pointerdown", e => {
    if (state.floating) return;
    active = true;
    startY = e.clientY;
    startHeight = sheet.getBoundingClientRect().height;
    sheet.classList.add("ui-resizing", "expanded");
    handle.setPointerCapture?.(e.pointerId);
    e.preventDefault(); e.stopPropagation();
  });
  handle.addEventListener("pointermove", e => {
    if (!active) return;
    const next = clamp(startHeight + (startY - e.clientY), 54, innerHeight - 90);
    sheet.style.height = `${next}px`;
    state.sheetHeight = next;
    e.preventDefault();
  });
  const end = e => {
    if (!active) return;
    active = false;
    sheet.classList.remove("ui-resizing");
    save();
    e?.preventDefault();
  };
  handle.addEventListener("pointerup", end);
  handle.addEventListener("pointercancel", end);
}

function installFloatingDrag() {
  const sheet = $("sheet"), handle = $("sheetHandle");
  if (!sheet || !handle) return;
  let drag = null;
  handle.addEventListener("pointerdown", e => {
    if (!state.floating || e.button !== 0) return;
    const r = sheet.getBoundingClientRect();
    drag = {x:e.clientX, y:e.clientY, left:r.left, top:r.top};
    handle.setPointerCapture?.(e.pointerId);
    e.preventDefault(); e.stopImmediatePropagation();
  }, true);
  handle.addEventListener("pointermove", e => {
    if (!drag || !state.floating) return;
    const scaledW = sheet.getBoundingClientRect().width;
    const scaledH = sheet.getBoundingClientRect().height;
    const left = clamp(drag.left + e.clientX - drag.x, 0, Math.max(0, innerWidth - Math.min(100, scaledW)));
    const top = clamp(drag.top + e.clientY - drag.y, 0, Math.max(0, innerHeight - 80));
    state.floatingLeft = left;
    state.floatingBottom = Math.max(0, innerHeight - top - scaledH);
    applyState();
    e.preventDefault();
  }, true);
  const end = e => {
    if (!drag) return;
    drag = null; save();
    e?.preventDefault(); e?.stopImmediatePropagation();
  };
  handle.addEventListener("pointerup", end, true);
  handle.addEventListener("pointercancel", end, true);
}

function installMenuDrag() {
  const menu = $("menu");
  if (!menu || $("menuDragHandle")) return;
  const handle = document.createElement("div");
  handle.id = "menuDragHandle";
  handle.textContent = "Menu — drag / resize";
  menu.prepend(handle);
  let drag = null;
  handle.addEventListener("pointerdown", e => {
    if (e.button !== 0) return;
    const r = menu.getBoundingClientRect();
    drag = {x:e.clientX, y:e.clientY, left:r.left, top:r.top};
    handle.setPointerCapture?.(e.pointerId);
    e.preventDefault(); e.stopPropagation();
  });
  handle.addEventListener("pointermove", e => {
    if (!drag) return;
    state.menuLeft = clamp(drag.left + e.clientX - drag.x, 6, Math.max(6, innerWidth - 120));
    state.menuTop = clamp(drag.top + e.clientY - drag.y, 6, Math.max(6, innerHeight - 80));
    applyState();
    e.preventDefault();
  });
  const end = e => { if (!drag) return; drag = null; save(); e?.preventDefault(); };
  handle.addEventListener("pointerup", end);
  handle.addEventListener("pointercancel", end);
}

function installResizePersistence() {
  if (!("ResizeObserver" in window)) return;
  const sheet = $("sheet"), menu = $("menu");
  if (sheet) new ResizeObserver(() => {
    if (!state.floating || sheet.offsetWidth <= 0 || sheet.offsetHeight <= 0) return;
    state.floatingWidth = sheet.offsetWidth;
    state.floatingHeight = sheet.offsetHeight;
    save();
  }).observe(sheet);
  if (menu) new ResizeObserver(() => {
    if (menu.offsetWidth <= 0 || menu.offsetHeight <= 0) return;
    state.menuWidth = menu.offsetWidth;
    state.menuHeight = menu.offsetHeight;
    save();
  }).observe(menu);
}

applyState();
installInterfaceControls();
installSheetResize();
installFloatingDrag();
installMenuDrag();
installResizePersistence();
addEventListener("resize", applyState);
