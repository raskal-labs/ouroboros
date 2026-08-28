const $ = id => document.getElementById(id);

function nextCheckpointName() {
  let names = [];
  try {
    const raw = localStorage.getItem("ouroborosPoseEditor.autosave.v9");
    const data = raw ? JSON.parse(raw) : null;
    names = Object.keys(data?.checkpoints || {});
  } catch (_) {}
  const used = new Set(
    names
      .map(name => /^Checkpoint\s+(\d+)$/i.exec(name)?.[1])
      .filter(Boolean)
      .map(Number)
  );
  let n = 1;
  while (used.has(n)) n++;
  return `Checkpoint ${String(n).padStart(3, "0")}`;
}

function installCheckpointNumbering() {
  const button = $("saveCheckpoint");
  if (!button || typeof button.onclick !== "function") return;
  const original = button.onclick;
  button.onclick = () => {
    const oldPrompt = window.prompt;
    window.prompt = (message, defaultValue) => oldPrompt(message, nextCheckpointName());
    try { return original(); }
    finally { window.prompt = oldPrompt; }
  };
}

function keepEndpointControlsVisible() {
  const wrapper = $("endpointControls"), head = $("headControls"), tail = $("tailControls");
  if (!wrapper || !head || !tail) return;
  wrapper.classList.add("v1-always-visible");

  if (!head.querySelector(".v1EndpointHeading")) {
    const h = document.createElement("div");
    h.className = "v1EndpointHeading";
    h.textContent = "Head & gaze";
    head.prepend(h);
  }
  if (!tail.querySelector(".v1EndpointHeading")) {
    const h = document.createElement("div");
    h.className = "v1EndpointHeading";
    h.textContent = "Tail";
    tail.prepend(h);
  }

  const enforce = () => {
    wrapper.classList.add("v1-always-visible");
    wrapper.classList.remove("hidden");
    head.classList.remove("hidden");
    tail.classList.remove("hidden");
  };
  enforce();
  const observer = new MutationObserver(enforce);
  observer.observe(wrapper, {attributes:true, attributeFilter:["class"]});
  observer.observe(head, {attributes:true, attributeFilter:["class"]});
  observer.observe(tail, {attributes:true, attributeFilter:["class"]});
}

function clarifyPerspective() {
  const range = $("perspective");
  const row = range?.closest(".controlRow");
  const label = row?.querySelector("label");
  if (!row || !label) return;
  label.textContent = "Perspective strength";
  if (!row.nextElementSibling?.classList.contains("v1PerspectiveHelp")) {
    const note = document.createElement("div");
    note.className = "v1PerspectiveHelp";
    note.textContent = "Depth / Z: FAR ← 6.5 neutral → NEAR. Perspective strength controls how strongly depth changes apparent scale.";
    row.after(note);
  }
}

function installResetButtons() {
  for (const row of document.querySelectorAll(".numericRow")) {
    if (row.querySelector(".v1ResetButton")) continue;
    const range = row.querySelector('input[type="range"]');
    const num = row.querySelector(".numericInput");
    if (!range || !num || range.id === "viewZoom") continue;
    const reset = document.createElement("button");
    reset.type = "button";
    reset.className = "v1ResetButton";
    reset.textContent = "↺";
    reset.title = "Reset to default";
    reset.setAttribute("aria-label", `Reset ${range.id} to default`);
    row.classList.add("v1HasReset");
    row.insertBefore(reset, row.querySelector(".controlValue"));
    reset.addEventListener("click", () => {
      if (range.disabled) return;
      const value = range.defaultValue;
      range.dispatchEvent(new KeyboardEvent("keydown", {bubbles:true, key:"Home"}));
      range.value = value;
      range.dispatchEvent(new Event("input", {bubbles:true}));
      range.dispatchEvent(new Event("change", {bubbles:true}));
    });
  }
}

function installRedoShortcut() {
  addEventListener("keydown", event => {
    const target = event.target;
    const editable = target instanceof HTMLElement && (
      target.tagName === "INPUT" || target.tagName === "TEXTAREA" ||
      target.tagName === "SELECT" || target.isContentEditable
    );
    if (editable) return;
    const mod = event.ctrlKey || event.metaKey;
    if (mod && !event.shiftKey && event.key.toLowerCase() === "y") {
      event.preventDefault();
      $("redoBtn")?.click();
    }
  }, true);
}

installCheckpointNumbering();
keepEndpointControlsVisible();
clarifyPerspective();
installResetButtons();
installRedoShortcut();
