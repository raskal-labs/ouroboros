const $ = id => document.getElementById(id);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const fit = (v, min, max) => Math.min(Math.max(v, min), max);
const STORAGE_KEY = "ouroborosPoseEditor.ui.v1";
const EDGE = 8;

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

function floatingBounds() {
  const scale = clamp(+state.scale || 1, .7, 1.35);
  const maxWidth = Math.max(180, (innerWidth - EDGE * 2) / scale);
  const maxHeight = Math.max(150, (innerHeight - EDGE * 2) / scale);
  const minWidth = Math.min(260, maxWidth);
  const minHeight = Math.min(180, maxHeight);
  const width = fit(Number.isFinite(+state.floatingWidth) ? +state.floatingWidth : defaults.floatingWidth, minWidth, maxWidth);
  const height = fit(Number.isFinite(+state.floatingHeight) ? +state.floatingHeight : defaults.floatingHeight, minHeight, maxHeight);
  const scaledWidth = width * scale;
  const scaledHeight = height * scale;
  const left = fit(Number.isFinite(+state.floatingLeft) ? +state.floatingLeft : defaults.floatingLeft, EDGE, Math.max(EDGE, innerWidth - scaledWidth - EDGE));
  const bottom = fit(Number.isFinite(+state.floatingBottom) ? +state.floatingBottom : defaults.floatingBottom, EDGE, Math.max(EDGE, innerHeight - scaledHeight - EDGE));
  return {scale, width, height, left, bottom};
}

function menuBounds(menu) {
  const maxWidth = Math.max(150, innerWidth - 12);
  const width = fit(Number.isFinite(+state.menuWidth) ? +state.menuWidth : defaults.menuWidth, Math.min(190, maxWidth), maxWidth);
  const measuredHeight = Number.isFinite(+state.menuHeight) ? +state.menuHeight : (menu?.offsetHeight || 240);
  const maxHeight = Math.max(100, innerHeight - 20);
  const height = fit(measuredHeight, Math.min(100, maxHeight), maxHeight);
  const left = Number.isFinite(+state.menuLeft) ? fit(+state.menuLeft, 6, Math.max(6, innerWidth - width - 6)) : null;
  const top = Number.isFinite(+state.menuTop) ? fit(+state.menuTop, 6, Math.max(6, innerHeight - height - 6)) : null;
  return {width, height, left, top};
}

function applyState() {
  const root = document.documentElement;
  root.style.setProperty("--ui-panel-alpha", clamp(+state.opacity || defaults.opacity, .18, 1));
  root.style.setProperty("--ui-panel-scale", clamp(+state.scale || 1, .7, 1.35));
  document.body.classList.toggle("panel-floating", !!state.floating);

  const sheet = $("sheet");
  if (sheet) {
    if (!state.floating && Number.isFinite(state.sheetHeight)) {
      state.sheetHeight = fit(+state.sheetHeight, 54, Math.max(54, innerHeight - 90));
      sheet.style.height = `${state.sheetHeight}px`;
      sheet.classList.add("expanded");
    } else if (!state.floating) {
      sheet.style.height = "";
    }
    if (state.floating) {
      const b = floatingBounds();
      state.floatingLeft = b.left;
      state.floatingBottom = b.bottom;
      state.floatingWidth = b.width;
      state.floatingHeight = b.height;
      root.style.setProperty("--floating-left", `${b.left}px`);
      root.style.setProperty("--floating-bottom", `${b.bottom}px`);
      root.style.setProperty("--floating-width", `${b.width}px`);
      root.style.setProperty("--floating-height", `${b.height}px`);
      sheet.classList.add("expanded");
      const chevron = $("handleChevron");
      if (chevron) chevron.textContent = "⋮";
    }
  }

  const menu = $("menu");
  if (menu) {
    const b = menuBounds(menu);
    state.menuWidth = b.width;
    if (Number.isFinite(state.menuHeight)) state.menuHeight = b.height;
    menu.style.width = `${b.width}px`;
    if (Number.isFinite(state.menuHeight)) menu.style.height = `${b.height}px`;
    if (b.left !== null && b.top !== null) {
      state.menuLeft = b.left;
      state.menuTop = b.top;
      menu.style.left = `${b.left}px`;
      menu.style.top = `${b.top}px`;
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
      const scaleNow = clamp(+state.scale || 1, .7, 1.35);
      const rect = sheet.getBoundingClientRect();
      state.floatingWidth = rect.width / scaleNow;
      state.floatingHeight = rect.height / scaleNow;
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
    const next = fit(startHeight + (startY - e.clientY), 54, Math.max(54, innerHeight - 90));
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
    drag = {x:e.clientX, y:e.clientY, left:r.left, top:r.top, width:r.width, height:r.height};
    handle.setPointerCapture?.(e.pointerId);
    e.preventDefault(); e.stopImmediatePropagation();
  }, true);
  handle.addEventListener("pointermove", e => {
    if (!drag || !state.floating) return;
    const left = fit(drag.left + e.clientX - drag.x, EDGE, Math.max(EDGE, innerWidth - drag.width - EDGE));
    const top = fit(drag.top + e.clientY - drag.y, EDGE, Math.max(EDGE, innerHeight - drag.height - EDGE));
    state.floatingLeft = left;
    state.floatingBottom = Math.max(EDGE, innerHeight - top - drag.height);
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
    drag = {x:e.clientX, y:e.clientY, left:r.left, top:r.top, width:r.width, height:r.height};
    handle.setPointerCapture?.(e.pointerId);
    e.preventDefault(); e.stopPropagation();
  });
  handle.addEventListener("pointermove", e => {
    if (!drag) return;
    state.menuLeft = fit(drag.left + e.clientX - drag.x, 6, Math.max(6, innerWidth - drag.width - 6));
    state.menuTop = fit(drag.top + e.clientY - drag.y, 6, Math.max(6, innerHeight - drag.height - 6));
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
    const scaleNow = clamp(+state.scale || 1, .7, 1.35);
    const r = sheet.getBoundingClientRect();
    state.floatingWidth = r.width / scaleNow;
    state.floatingHeight = r.height / scaleNow;
    save();
  }).observe(sheet);
  if (menu) new ResizeObserver(() => {
    if (menu.offsetWidth <= 0 || menu.offsetHeight <= 0) return;
    state.menuWidth = menu.offsetWidth;
    state.menuHeight = menu.offsetHeight;
    save();
  }).observe(menu);
}

function handleViewportChange() {
  applyState();
  save();
}

addEventListener("ouroboros:collapse-sheet", () => {
  if (state.floating) return;
  state.sheetHeight = null;
  const sheet = $("sheet"), chevron = $("handleChevron");
  if (sheet) { sheet.style.height = ""; sheet.classList.remove("expanded"); }
  if (chevron) chevron.textContent = "︿";
  save();
});

applyState();
installInterfaceControls();
installSheetResize();
installFloatingDrag();
installMenuDrag();
installResizePersistence();
addEventListener("resize", handleViewportChange);
addEventListener("orientationchange", () => requestAnimationFrame(handleViewportChange));
window.visualViewport?.addEventListener("resize", handleViewportChange);