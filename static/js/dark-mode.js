document.addEventListener('DOMContentLoaded', () => {
  const toggleButton = document.getElementById('dark-mode-toggle');
  const icon = document.getElementById('dark-mode-icon');
  const html = document.documentElement;

  // Add transition styles globally
  const transitionStyles = `
    .theme-transition * {
      transition: background-color 0.3s ease,
                  border-color 0.3s ease,
                  color 0.3s ease,
                  box-shadow 0.3s ease !important,
                  filter 0.3s ease !important;
    }
  `;
  const styleSheet = document.createElement('style');
  styleSheet.textContent = transitionStyles;
  document.head.appendChild(styleSheet);

  const savedTheme = localStorage.getItem('darkMode');
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  let isDark = savedTheme !== null ? savedTheme === 'true' : systemPrefersDark;

  applyTheme(isDark, false);

  // Listen to system preference changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (localStorage.getItem('darkMode') === null) {
      applyTheme(e.matches, true);
    }
  });

  toggleButton.addEventListener('click', () => {
    const currentlyDark = html.getAttribute('data-color-scheme') === 'dark';
    const nextState = !currentlyDark;
    applyTheme(nextState, true);
    localStorage.setItem('darkMode', String(nextState));
  });

  function applyTheme(darkMode, withTransition = true) {
    if (withTransition) {
      html.classList.add('theme-transition');
      setTimeout(() => html.classList.remove('theme-transition'), 300);
    }

    html.setAttribute('data-color-scheme', darkMode ? 'dark' : 'light');

    if (icon) {
      icon.className = darkMode ? 'bi bi-sun' : 'bi bi-moon';
      icon.setAttribute('aria-label', darkMode ? 'Switch to light mode' : 'Switch to dark mode');
    }

    updateMetaThemeColor(darkMode);
    recolorImagesToMatchTheme(darkMode);
  }

  function updateMetaThemeColor(isDark) {
    let metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (!metaThemeColor) {
      metaThemeColor = document.createElement('meta');
      metaThemeColor.name = 'theme-color';
      document.head.appendChild(metaThemeColor);
    }
    metaThemeColor.content = isDark ? '#0f172a' : '#ffffff';
  }

  function recolorImagesToMatchTheme(darkMode) {
    const bg = [38, 40, 40]; // RGB of #262828
    const threshold = 240;   // anything > this is "white-ish"

    document.querySelectorAll('img:not(.no-invert)').forEach(img => {
      const original = img.dataset.originalSrc || img.src;

      if (!darkMode) {
        img.src = original;
        img.classList.remove('processed');
        return;
      }

      if (!img.complete) {
        img.onload = () => recolorImagesToMatchTheme(true);
        return;
      }

      if (img.classList.contains('processed')) return;

      img.dataset.originalSrc = original;

      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
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
        // alpha unchanged
      }

      ctx.putImageData(imageData, 0, 0);
      img.src = canvas.toDataURL();
      img.classList.add('processed');
    });
  }
});
