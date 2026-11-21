"use strict";

(() => {
  const config = window.LEANWAM_CONFIG || {};
  const safeUrl = (value) => {
    if (typeof value !== "string" || !value.trim()) return null;
    try {
      const url = new URL(value, document.baseURI);
      // file: supports a local preview; javascript: and data: are never links.
      if (["https:", "http:"].includes(url.protocol) ||
          (location.protocol === "file:" && url.protocol === "file:")) return url.href;
    } catch (_) { /* Leave invalid or empty links unavailable. */ }
    return null;
  };

  document.querySelectorAll("[data-resource]").forEach((link) => {
    const value = config.links?.[link.dataset.resource];
    const url = safeUrl(value === undefined ? link.getAttribute("href") : value);
    if (url) {
      link.href = url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.removeAttribute("aria-disabled");
      link.querySelector(".coming-soon")?.remove();
    } else {
      link.removeAttribute("href");
      link.setAttribute("aria-disabled", "true");
      link.title = "Link coming soon";
    }
  });

  document.querySelectorAll("[data-author]").forEach((link) => {
    const url = safeUrl(config.authors?.[link.dataset.author]);
    if (url) {
      link.href = url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    } else {
      link.title = "Personal homepage coming soon";
    }
  });

  // All three tables are ordinary HTML and remain visible without JavaScript.
  const tablist = document.querySelector(".benchmark-tabs");
  const tabs = Array.from(tablist.querySelectorAll("button"));
  const panels = Array.from(document.querySelectorAll(".benchmark-panel"));
  const selectBenchmark = (key, updateHash = false) => {
    if (!panels.some((panel) => panel.id === `benchmark-${key}`)) return;
    tabs.forEach((tab) => {
      const active = tab.dataset.benchmark === key;
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
    });
    panels.forEach((panel) => { panel.hidden = panel.id !== `benchmark-${key}`; });
    if (updateHash) {
      try { history.replaceState(null, "", `#benchmark-${key}`); } catch (_) { /* file preview */ }
    }
  };
  if (panels.length === tabs.length) {
    tablist.hidden = false;
    tablist.setAttribute("role", "tablist");
    tabs.forEach((tab, index) => {
      tab.setAttribute("role", "tab");
      tab.setAttribute("aria-controls", `benchmark-${tab.dataset.benchmark}`);
      tab.addEventListener("click", () => selectBenchmark(tab.dataset.benchmark, true));
      tab.addEventListener("keydown", (event) => {
        let next;
        if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
        if (event.key === "ArrowLeft") next = (index + tabs.length - 1) % tabs.length;
        if (event.key === "Home") next = 0;
        if (event.key === "End") next = tabs.length - 1;
        if (next === undefined) return;
        event.preventDefault();
        selectBenchmark(tabs[next].dataset.benchmark, true);
        tabs[next].focus();
      });
    });
    panels.forEach((panel) => {
      panel.setAttribute("role", "tabpanel");
      panel.setAttribute("aria-labelledby", `tab-${panel.dataset.benchmark}`);
    });
    const syncHash = () => {
      const key = location.hash.replace("#benchmark-", "");
      if (tabs.some((tab) => tab.dataset.benchmark === key)) selectBenchmark(key);
    };
    selectBenchmark("libero");
    syncHash();
    window.addEventListener("hashchange", syncHash);
    document.body.classList.add("js-enhanced");
  }

  const dialog = document.getElementById("figure-dialog");
  const dialogImage = document.getElementById("dialog-image");
  const imageWrap = dialog.querySelector(".dialog-image-wrap");
  if (typeof dialog.showModal === "function") {
    document.querySelectorAll("[data-figure]").forEach((link) => {
      link.addEventListener("click", (event) => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        document.getElementById("dialog-title").textContent = link.dataset.title;
        document.getElementById("dialog-pdf").href = link.href;
        dialogImage.src = `assets/figures/${link.dataset.figure}.webp`;
        dialogImage.alt = link.querySelector("img").alt;
        imageWrap.classList.remove("zoomed");
        imageWrap.scrollTo(0, 0);
        dialog.showModal();
        document.body.classList.add("dialog-open");
        document.getElementById("dialog-close").focus();
      });
    });
    document.getElementById("dialog-close").addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", (event) => {
      const bounds = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right ||
          event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
    });
    dialog.addEventListener("close", () => document.body.classList.remove("dialog-open"));
    dialogImage.addEventListener("click", () => imageWrap.classList.toggle("zoomed"));
  }

  const bibtex = typeof config.bibtex === "string" ? config.bibtex.trim() : "";
  if (bibtex) {
    document.getElementById("bibtex").textContent = bibtex;
    document.getElementById("citation-pre").hidden = false;
    document.getElementById("citation-pending").hidden = true;
    document.querySelector(".citation-actions").hidden = false;
    const bibUrl = URL.createObjectURL(new Blob([`${bibtex}\n`], {type: "text/plain;charset=utf-8"}));
    document.getElementById("download-bibtex").href = bibUrl;
    const copyButton = document.getElementById("copy-citation");
    copyButton.addEventListener("click", async () => {
      let copied = false;
      try {
        if (navigator.clipboard?.writeText) {
          await navigator.clipboard.writeText(bibtex);
          copied = true;
        }
      } catch (_) { /* Try the local/HTTP preview fallback below. */ }
      if (!copied) {
        const textarea = document.createElement("textarea");
        textarea.value = bibtex;
        textarea.style.cssText = "position:fixed;left:-9999px;top:0";
        textarea.setAttribute("readonly", "");
        document.body.append(textarea);
        textarea.select();
        try { copied = document.execCommand("copy"); } catch (_) { /* Manual copy remains available. */ }
        textarea.remove();
        copyButton.focus();
      }
      document.getElementById("copy-status").textContent = copied
        ? "BibTeX copied to clipboard."
        : "Select the BibTeX above to copy it, or download the .bib file.";
    });
  }

  const navLinks = Array.from(document.querySelectorAll("nav a"));
  let navFramePending = false;
  const updateNavigation = () => {
    navFramePending = false;
    let active = null;
    navLinks.forEach((link) => {
      if (document.querySelector(link.hash).getBoundingClientRect().top <= 180) active = link;
    });
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 3) {
      active = navLinks[navLinks.length - 1];
    }
    navLinks.forEach((link) => {
      if (link === active) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  };
  window.addEventListener("scroll", () => {
    if (!navFramePending) {
      navFramePending = true;
      requestAnimationFrame(updateNavigation);
    }
  }, {passive: true});
  updateNavigation();
})();
