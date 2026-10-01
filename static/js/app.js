document.addEventListener("click", async (event) => {
  const btn = event.target.closest(".js-attalica-verify");
  if (!btn) return;

  const id = btn.getAttribute("data-id");
  if (!id) return;

  btn.disabled = true;
  btn.textContent = "Updating...";

  try {
    const res = await fetch("/attlicaver", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ nid: Number(id) }),
    });

    const payload = await res.json();
    if (res.ok && payload.ok) {
      window.location.reload();
      return;
    }
  } catch (err) {
    // Ignore and fall through to reset button
  }

  btn.disabled = false;
  btn.textContent = "Verify";
  alert("Verification failed. Please retry.");
});

(() => {
  const machineMenus = document.querySelectorAll(".machine-menu");
  machineMenus.forEach((menu) => {
    menu.addEventListener("toggle", () => {
      if (!menu.open) return;
      const panel = menu.closest(".menu-panel");
      if (!panel) return;
      panel.querySelectorAll(".machine-menu").forEach((node) => {
        if (node !== menu) node.open = false;
      });
    });
  });
})();

(() => {
  const input = document.getElementById("usernameInput");
  const list = document.getElementById("usernameSuggestions");
  if (!input || !list) return;

  let items = [];
  let activeIndex = -1;
  let debounceTimer = null;
  let controller = null;

  function hideList() {
    items = [];
    activeIndex = -1;
    list.hidden = true;
    list.innerHTML = "";
  }

  function highlightActive() {
    const nodes = list.querySelectorAll(".auth-suggest-item");
    nodes.forEach((node, index) => {
      node.classList.toggle("active", index === activeIndex);
    });
  }

  function selectItem(value) {
    input.value = value;
    hideList();
    input.focus();
  }

  function renderSuggestions(values) {
    items = values;
    activeIndex = -1;
    list.innerHTML = "";

    if (!items.length) {
      hideList();
      return;
    }

    const fragment = document.createDocumentFragment();
    items.forEach((value) => {
      const row = document.createElement("div");
      row.className = "auth-suggest-item";
      row.textContent = value;
      row.addEventListener("mousedown", (event) => {
        event.preventDefault();
        selectItem(value);
      });
      fragment.appendChild(row);
    });

    list.appendChild(fragment);
    list.hidden = false;
  }

  async function fetchSuggestions(query) {
    if (controller) controller.abort();
    controller = new AbortController();

    const res = await fetch(`/api/login-suggestions?q=${encodeURIComponent(query)}`, {
      signal: controller.signal,
    });
    if (!res.ok) return [];

    const data = await res.json();
    if (!Array.isArray(data)) return [];
    return data
      .map((value) => String(value || "").trim())
      .filter((value) => value.length > 0);
  }

  input.addEventListener("input", () => {
    const query = input.value.trim();
    if (debounceTimer) clearTimeout(debounceTimer);

    if (!query) {
      hideList();
      return;
    }

    debounceTimer = setTimeout(async () => {
      try {
        const values = await fetchSuggestions(query);
        if (input.value.trim() !== query) return;
        renderSuggestions(values);
      } catch (error) {
        hideList();
      }
    }, 180);
  });

  input.addEventListener("keydown", (event) => {
    if (list.hidden || !items.length) return;

    if (event.key === "ArrowDown") {
      event.preventDefault();
      activeIndex = (activeIndex + 1) % items.length;
      highlightActive();
      return;
    }

    if (event.key === "ArrowUp") {
      event.preventDefault();
      activeIndex = activeIndex <= 0 ? items.length - 1 : activeIndex - 1;
      highlightActive();
      return;
    }

    if (event.key === "Enter" && activeIndex >= 0) {
      event.preventDefault();
      selectItem(items[activeIndex]);
      return;
    }

    if (event.key === "Escape") {
      hideList();
    }
  });

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".auth-suggest-wrap")) {
      hideList();
    }
  });
})();

(() => {
  const field = document.querySelector(".js-sample-scan-format");
  if (!field) return;

  let timer = null;

  const parseTokens = (rawValue) => {
    const raw = String(rawValue || "").trim();
    if (!raw) return [];

    const barcodeRegex = /\d+?-\d(?=\d|$)/g;
    const chunks = raw
      .replaceAll(",", " ")
      .split(/[\s,;\n\r\t]+/g)
      .map((v) => v.trim())
      .filter(Boolean);

    const out = [];
    for (const chunk of chunks) {
      const full = chunk.match(/^\d+-\d$/);
      if (full) {
        out.push(chunk);
        continue;
      }

      const matches = chunk.match(barcodeRegex) || [];
      if (matches.length && matches.join("") === chunk) {
        out.push(...matches);
        continue;
      }

      out.push(chunk);
    }

    return out;
  };

  const normalize = () => {
    const tokens = parseTokens(field.value);
    field.value = tokens.join(", ");
  };

  field.addEventListener("input", () => {
    if (timer) clearTimeout(timer);
    // Small delay helps scanner bursts settle before normalization.
    timer = setTimeout(normalize, 60);
  });

  field.addEventListener("blur", normalize);
})();

document.addEventListener("click", (event) => {
  const btn = event.target.closest(".js-discard-see-more");
  if (!btn) return;

  const cell = btn.closest(".discard-samples-cell");
  const hiddenPart = cell?.querySelector(".discard-samples-more");
  if (!cell || !hiddenPart) return;

  const isExpanded = !hiddenPart.hidden;
  hiddenPart.hidden = isExpanded;
  btn.textContent = isExpanded ? "See more" : "See less";
});
