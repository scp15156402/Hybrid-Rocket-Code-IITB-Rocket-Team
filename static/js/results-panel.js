// static/js/results-panel.js

document.addEventListener("DOMContentLoaded", function () {
  const resultsPanel = document.getElementById("results-panel");
  const pinIcon = document.getElementById("results-pin");
  const toggleIcon = document.getElementById("results-toggle");
  const resultsTab = document.getElementById("results-tab");
  const tabChevron = resultsTab.querySelector("i");
  const summary = document.getElementById("results-summary"); // <pre id="results-summary">

  // LocalStorage keys
  const PINNED_KEY = "resultsPinned";
  const OPEN_KEY = "resultsOpen";

  // Load saved state or defaults
  let isPinned = localStorage.getItem(PINNED_KEY);
  let isOpen = localStorage.getItem(OPEN_KEY);

  isPinned = isPinned === null ? true : isPinned === "true";
  isOpen = isOpen === null ? true : isOpen === "true";

  function updateToggleIcons() {
    toggleIcon.classList.toggle("bi-chevron-down", isOpen);
    toggleIcon.classList.toggle("bi-chevron-up", !isOpen);

    tabChevron.classList.toggle("bi-chevron-up", !isOpen);
    tabChevron.classList.toggle("bi-chevron-down", isOpen);
  }

  function applyPanelState() {
    if (isPinned) {
      resultsPanel.classList.remove("collapsed");
      toggleIcon.style.display = "none";
      resultsTab.style.display = "none";

      pinIcon.classList.add("bi-pin-angle-fill");
      pinIcon.classList.remove("bi-pin-angle");
    } else {
      toggleIcon.style.display = "inline-block";
      pinIcon.classList.add("bi-pin-angle");
      pinIcon.classList.remove("bi-pin-angle-fill");

      if (isOpen) {
        resultsPanel.classList.remove("collapsed");
        resultsTab.style.display = "none";
      } else {
        resultsPanel.classList.add("collapsed");
        resultsTab.style.display = "flex"; // ensure tab is always accessible
      }

      updateToggleIcons();
    }
  }

  // Initial setup
  applyPanelState();

  // Toggle pin
  pinIcon.addEventListener("click", () => {
    isPinned = !isPinned;
    isOpen = true; // always open when pinning

    localStorage.setItem(PINNED_KEY, isPinned);
    localStorage.setItem(OPEN_KEY, isOpen);

    applyPanelState();
  });

  // Chevron inside panel toggles open/close
  toggleIcon.addEventListener("click", () => {
    isOpen = !resultsPanel.classList.toggle("collapsed");
    resultsTab.style.display = isOpen ? "none" : "flex";

    localStorage.setItem(OPEN_KEY, isOpen);
    updateToggleIcons();
  });

  // Tab chevron restores panel
  resultsTab.addEventListener("click", () => {
    if (!isPinned) {
      isOpen = true;
      resultsPanel.classList.remove("collapsed");
      resultsTab.style.display = "none";

      localStorage.setItem(OPEN_KEY, isOpen);
      updateToggleIcons();
    }
  });

  // Force open if error is present and unpinned
  if (!isPinned && summary && summary.textContent.includes("Error:")) {
    isOpen = true;
    localStorage.setItem(OPEN_KEY, isOpen);
    resultsPanel.classList.remove("collapsed");
    resultsTab.style.display = "none";
    updateToggleIcons();
  }
});
