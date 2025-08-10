// features/dropdowns/generate_cad/static/dropdowns/export-cad.js

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("generateCadBtn");
  btn.addEventListener("click", async () => {
    const payload = {
      current_values: window.currentValues,  // assumes global variables set by your app
      results: window.lastResults
    };
    const res = await fetch("/dropdowns/generate_cad/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const json = await res.json();
    if (json.success) {
      showCADDownloads(json.files);
    } else {
      alert("CAD export failed.");
    }
  });
});

function showCADDownloads(files) {
  const container = document.getElementById("cadDownloads");
  let html = "<h4>Download CAD Parts:</h4><ul>";
  for (const [name, fns] of Object.entries(files)) {
    html += `
      <li>
        ${name}:
        <a href="/static/cad/${fns.step}" download>STEP</a> |
        <a href="/static/cad/${fns.stl}" download>STL</a>
      </li>`;
  }
  html += "</ul>";
  container.innerHTML = html;
}
