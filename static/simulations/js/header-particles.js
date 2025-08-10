/*
  ================== Animated Header Canvas: Particle Effect ==================
  Decorative particle animation behind the header.
*/
(function () {
  const canvas = document.getElementById('headerCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let particles = [];

  function resizeCanvasToHeader() {
    const header = document.querySelector('.app-header');
    const rect = header.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
  }

  function initParticles() {
    const isMobile = window.innerWidth <= 768;
    const particleCount = isMobile ? 25 : 40;
    particles = [];

    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: isMobile ? Math.random() * 1.8 + 1.2 : Math.random() * 3.5 + 1.5,
        o: Math.random() * 0.25 + 0.3,
        vy: isMobile ? Math.random() * 0.3 + 0.15 : Math.random() * 0.4 + 0.2
      });
    }
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const p of particles) {
      p.y -= p.vy;
      if (p.y < -p.r) p.y = canvas.height + p.r;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.shadowColor = `rgba(0, 110, 220, ${p.o * 0.9})`;
      ctx.shadowBlur = 8;
      ctx.fillStyle = `rgba(0, 110, 220, ${p.o})`;
      ctx.fill();
    }
    requestAnimationFrame(animate);
  }

  function start() {
    resizeCanvasToHeader();
    initParticles();
    animate();
  }

  window.addEventListener('resize', () => {
    resizeCanvasToHeader();
    initParticles();
  });

  document.addEventListener('DOMContentLoaded', start);
})();
