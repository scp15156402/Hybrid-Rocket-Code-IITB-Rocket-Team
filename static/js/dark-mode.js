// static/js/dark-mode.js
document.addEventListener("DOMContentLoaded", function() {
  const toggleButton = document.getElementById("dark-mode-toggle");
  const darkIcon = document.getElementById("dark-mode-icon");
  const lightLink = document.getElementById("light-style");
  const darkLink = document.getElementById("dark-style");
  const html = document.documentElement;

  // Add smooth transitions
  const styleSheet = document.createElement("style");
  styleSheet.textContent = `
    .theme-transition * {
      transition: background-color 0.3s ease, 
                  color 0.3s ease, 
                  border-color 0.3s ease,
                  box-shadow 0.3s ease,
                  filter 0.3s ease !important;
    }
  `;
  document.head.appendChild(styleSheet);

  function applyTheme(theme, withTransition = true) {
    const isDark = theme === "dark";
    
    if (withTransition) {
      html.classList.add("theme-transition");
      setTimeout(() => html.classList.remove("theme-transition"), 300);
    }

    // Toggle stylesheets
    if (darkLink && lightLink) {
      darkLink.disabled = !isDark;
      lightLink.disabled = isDark;
    }

    // Set data attribute for CSS variable fallback
    html.setAttribute("data-color-scheme", theme);

    // Update icon
    if (darkIcon) {
      darkIcon.className = isDark ? "bi bi-sun" : "bi bi-moon";
      darkIcon.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
    }

    // Update meta theme color
    updateMetaThemeColor(isDark);
    
    // Recolor images if needed
    recolorImagesToMatchTheme(isDark);
  }

  function updateMetaThemeColor(isDark) {
    let metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (!metaThemeColor) {
      metaThemeColor = document.createElement("meta");
      metaThemeColor.name = "theme-color";
      document.head.appendChild(metaThemeColor);
    }
    metaThemeColor.content = isDark ? "#0f172a" : "#ffffff";
  }

  function recolorImagesToMatchTheme(darkMode) {
    const bg = [38, 40, 40]; // RGB of #262828
    const threshold = 240;

    document.querySelectorAll('img:not(.no-invert)').forEach(img => {
      const original = img.dataset.originalSrc || img.src;

      if (!darkMode) {
        if (img.dataset.originalSrc) {
          img.src = original;
          img.classList.remove("processed");
        }
        return;
      }

      if (!img.complete) {
        img.onload = () => recolorImagesToMatchTheme(true);
        return;
      }

      if (img.classList.contains("processed")) return;

      img.dataset.originalSrc = original;

      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      ctx.drawImage(img, 0, 0);

      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;

      for (let i = 0; i < data.length; i += 4) {
        const r = data[i], g = data[i+1], b = data[i+2], a = data[i+3];
        if (a === 0) continue;

        if (r > threshold && g > threshold && b > threshold) {
          data[i] = bg[0];
          data[i+1] = bg[1];
          data[i+2] = bg[2];
        } else {
          data[i] = 255 - r;
          data[i+1] = 255 - g;
          data[i+2] = 255 - b;
        }
      }

      ctx.putImageData(imageData, 0, 0);
      img.src = canvas.toDataURL();
      img.classList.add("processed");
    });
  }

  // Event listeners
  toggleButton.addEventListener("click", () => {
    const currentTheme = darkLink.disabled ? "light" : "dark";
    const nextTheme = currentTheme === "light" ? "dark" : "light";
    applyTheme(nextTheme, true);
    localStorage.setItem("color-scheme", nextTheme);
  });

  // System preference detection
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
    if (!localStorage.getItem("color-scheme")) {
      applyTheme(e.matches ? "dark" : "light", true);
    }
  });

  // Initial load
  const stored = localStorage.getItem("color-scheme");
  const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const initialTheme = stored || (systemPrefersDark ? "dark" : "light");
  applyTheme(initialTheme, false);
});