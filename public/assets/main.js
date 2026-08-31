/* ── THREE.JS PARTICLE HERO ── */
function initHero() {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas || typeof THREE === 'undefined') return;

  const W = canvas.clientWidth, H = canvas.clientHeight;
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setSize(W, H); renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, W / H, 0.1, 1000);
  camera.position.z = 5;

  /* ── particles ── */
  const count = window.innerWidth < 768 ? 600 : 1800;
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const sizes = new Float32Array(count);

  const purple = new THREE.Color(0x814ac8);
  const purpleLight = new THREE.Color(0xdf7afe);
  const white = new THREE.Color(0xffffff);

  for (let i = 0; i < count; i++) {
    const r = 8 + Math.random() * 6;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    positions[i*3]   = r * Math.sin(phi) * Math.cos(theta);
    positions[i*3+1] = r * Math.sin(phi) * Math.sin(theta);
    positions[i*3+2] = r * Math.cos(phi);

    const t = Math.random();
    const c = t < 0.4 ? purple : t < 0.7 ? purpleLight : white;
    colors[i*3] = c.r; colors[i*3+1] = c.g; colors[i*3+2] = c.b;
    sizes[i] = 0.5 + Math.random() * 2.5;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

  const mat = new THREE.ShaderMaterial({
    uniforms: { uTime: { value: 0 }, uMouse: { value: new THREE.Vector2(0, 0) } },
    vertexShader: `
      attribute float size;
      attribute vec3 color;
      varying vec3 vColor;
      varying float vAlpha;
      uniform float uTime;
      uniform vec2 uMouse;
      void main() {
        vColor = color;
        vec3 pos = position;
        float angle = uTime * 0.08 + pos.y * 0.05;
        pos.x += sin(angle + pos.z * 0.3) * 0.15;
        pos.y += cos(angle + pos.x * 0.3) * 0.12;
        pos.x += uMouse.x * (pos.z / 14.0) * 0.6;
        pos.y += uMouse.y * (pos.z / 14.0) * 0.6;
        vec4 mvPos = modelViewMatrix * vec4(pos, 1.0);
        gl_PointSize = size * (280.0 / -mvPos.z);
        gl_Position = projectionMatrix * mvPos;
        vAlpha = 0.2 + 0.7 * smoothstep(0.0, 3.0, -mvPos.z * 0.15);
      }
    `,
    fragmentShader: `
      varying vec3 vColor;
      varying float vAlpha;
      void main() {
        float d = length(gl_PointCoord - vec2(0.5));
        if (d > 0.5) discard;
        float alpha = vAlpha * (1.0 - smoothstep(0.2, 0.5, d));
        gl_FragColor = vec4(vColor, alpha);
      }
    `,
    transparent: true, depthWrite: false, vertexColors: false
  });

  const particles = new THREE.Points(geo, mat);
  scene.add(particles);

  /* ── central glow orb ── */
  const orbGeo = new THREE.SphereGeometry(1.4, 32, 32);
  const orbMat = new THREE.ShaderMaterial({
    uniforms: { uTime: { value: 0 } },
    vertexShader: `varying vec3 vNormal; void main(){ vNormal=normalize(normalMatrix*normal); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }`,
    fragmentShader: `
      varying vec3 vNormal;
      uniform float uTime;
      void main(){
        float f = dot(vNormal, vec3(0.0,0.0,1.0));
        float glow = pow(1.0 - abs(f), 3.5);
        vec3 col = mix(vec3(0.5, 0.29, 0.78), vec3(0.87, 0.48, 1.0), glow + sin(uTime*0.5)*0.1);
        gl_FragColor = vec4(col, glow * 0.55);
      }
    `,
    transparent: true, side: THREE.BackSide, depthWrite: false
  });
  const orb = new THREE.Mesh(orbGeo, orbMat);
  scene.add(orb);

  /* ── black void ── */
  const voidGeo = new THREE.SphereGeometry(1.05, 32, 32);
  const voidMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
  scene.add(new THREE.Mesh(voidGeo, voidMat));

  /* ── mouse (RAF-throttled) ── */
  let mouseX = 0, mouseY = 0;
  let targetX = 0, targetY = 0;
  let mousePending = false;
  window.addEventListener('mousemove', e => {
    if (mousePending) return;
    mousePending = true;
    requestAnimationFrame(() => {
      mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
      mouseY = -(e.clientY / window.innerHeight - 0.5) * 2;
      mousePending = false;
    });
  }, { passive: true });

  /* ── resize ── */
  window.addEventListener('resize', () => {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    renderer.setSize(w, h);
    camera.aspect = w / h; camera.updateProjectionMatrix();
  });

  /* ── animate ── */
  const clock = new THREE.Clock();
  function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    mat.uniforms.uTime.value = t;
    orbMat.uniforms.uTime.value = t;

    targetX += (mouseX - targetX) * 0.04;
    targetY += (mouseY - targetY) * 0.04;
    mat.uniforms.uMouse.value.set(targetX, targetY);

    particles.rotation.y = t * 0.025;
    particles.rotation.x = Math.sin(t * 0.015) * 0.1;
    orb.scale.setScalar(1 + Math.sin(t * 0.8) * 0.04);

    renderer.render(scene, camera);
  }
  animate();
}

/* ── NAVIGATION ── */
/* ── NAVIGATION ── */
function initNav() {
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
      hamburger.classList.toggle('active'); // animated X
    });
    mobileMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        hamburger.classList.remove('active');
      });
    });
  }

  // active link
  let current = pageKey(location.pathname);

  const portfolioPages = [
  "portfolio",
  "arvr",
  "games",
  "apps",
  "websites",
  "project-detail"
  ];

if (portfolioPages.includes(current)) {
  current = "portfolio";
}
  document.querySelectorAll('.nav-links a, .mobile-menu a').forEach(a => {
    if (pageKey(a.getAttribute('href')) === current) {
      a.classList.add('active');
    }
  });

  initNavIndicator(current);
}

/* Normalise a path or href to a bare page name.
   Handles Netlify Pretty URLs ("/about"), trailing slashes and "/" itself. */
function pageKey(value) {
  if (!value) return 'index';
  const last = value.split('?')[0].split('#')[0].split('/').filter(Boolean).pop();
  if (!last) return 'index';
  return last.replace(/\.html$/i, '').toLowerCase();
}

/* Sliding Nav Indicator */
function initNavIndicator(current) {
  const indicator = document.querySelector('.nav-indicator');
  const navLinks = document.querySelectorAll('.nav-links a');
  const navList = document.querySelector('.nav-links');
  if (!indicator || !navLinks.length || !navList) return;

  const activeLink =
    [...navLinks].find(link => pageKey(link.getAttribute('href')) === current) || navLinks[0];
  activeLink.classList.add('active');

  function moveIndicator(link) {
    indicator.style.width = link.offsetWidth + 'px';
    indicator.style.left = link.offsetLeft + 'px';
  }

  moveIndicator(activeLink);
  // Re-measure once webfonts land, otherwise widths are computed against the fallback font.
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(() => moveIndicator(activeLink));
  }
  window.addEventListener('resize', () => moveIndicator(activeLink));

  navLinks.forEach(link => {
    link.addEventListener('mouseenter', () => moveIndicator(link));
  });

  navList.addEventListener('mouseleave', () => moveIndicator(activeLink));
}

/* ── FAQ ACCORDION ── */
function initFAQ() {
  document.querySelectorAll('.faq-item').forEach(item => {

    if (item.dataset.initialized) return;
    item.dataset.initialized = "true";

    item.querySelector('.faq-q').addEventListener('click', () => {
      const open = item.classList.contains('open');

      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));

      if (!open) item.classList.add('open');
    });

  });
}

/* ── SCROLL REVEAL — enhanced: blur + scale + direction variants ── */
function initReveal() {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => {
    if (prefersReduced) {
      el.classList.add('visible');
    } else {
      obs.observe(el);
    }
  });
}

/* ── FORM ── */
function initForms() {
  document.querySelectorAll('form[data-contact]').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const btn = form.querySelector('[type=submit]');
      const orig = btn.textContent;
      btn.textContent = 'Sending…'; btn.disabled = true;
      setTimeout(() => {
        btn.textContent = 'Sent ✓'; btn.style.background = '#2a9d4a';
        form.reset();
        setTimeout(() => { btn.textContent = orig; btn.style.background = ''; btn.disabled = false; }, 3000);
      }, 1200);
    });
  });
}

/* ── COUNTER ANIMATION ── */
function initCounters() {
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseInt(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    const obs = new IntersectionObserver(entries => {
      if (!entries[0].isIntersecting) return;
      obs.disconnect();
      const dur = 1800;
      const t0 = performance.now();
      function step(now) {
        const progress = Math.min((now - t0) / dur, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(ease * target) + suffix;
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }, { threshold: 0.5 });
    obs.observe(el);
  });
}

/* ── CURSOR GLOW ORB ── */
function initCursorGlow() {
  if (window.matchMedia('(pointer: coarse)').matches) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const orb = document.createElement('div');
  orb.id = 'cursor-glow';
  document.body.appendChild(orb);

  let cx = -999, cy = -999;
  let tx = -999, ty = -999;

  window.addEventListener('mousemove', e => {
    tx = e.clientX;
    ty = e.clientY;
  }, { passive: true });

  document.addEventListener('mouseleave', () => { orb.style.opacity = '0'; });
  document.addEventListener('mouseenter', () => { orb.style.opacity = '1'; });

  function loop() {
    cx += (tx - cx) * 0.1;
    cy += (ty - cy) * 0.1;
    orb.style.transform = `translate(${cx - 180}px, ${cy - 180}px)`;
    requestAnimationFrame(loop);
  }
  loop();
}

/* ── SCROLL PROGRESS BAR + NAV SCROLL STATE ── */
function initScrollProgress() {
  const bar = document.createElement('div');
  bar.id = 'scroll-progress';
  bar.style.transformOrigin = 'left';
  document.body.appendChild(bar);

  const nav = document.querySelector('.nav');
  let ticking = false;

  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const pct = docHeight > 0 ? (scrollTop / docHeight) : 0;
        bar.style.transform = `scaleX(${pct})`;
        if (nav) nav.classList.toggle('scrolled', scrollTop > 20);
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
}

/* ── 3D CARD TILT ── */
function initCardTilt() {
  if (window.matchMedia('(pointer: coarse)').matches) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const TILT = 7;

  document.querySelectorAll('.card:not(.testi-card), .p-card:not(.p-card), .service-showcase').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const cx = rect.width / 2;
      const cy = rect.height / 2;
      const rotX = ((y - cy) / cy) * -TILT;
      const rotY = ((x - cx) / cx) * TILT;
      card.style.transform = `perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-6px) scale(1.012)`;
      card.style.transition = 'transform 0.1s linear, box-shadow 0.4s, border-color 0.4s';
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
      card.style.transition = '';
    });
  });
}

/* ── MAGNETIC BTN RADIAL HIGHLIGHT ── */
function initMagneticButtons() {
  if (window.matchMedia('(pointer: coarse)').matches) return;

  document.querySelectorAll('.btn-primary').forEach(btn => {
    btn.addEventListener('mousemove', e => {
      const rect = btn.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      btn.style.setProperty('--mx', x + '%');
      btn.style.setProperty('--my', y + '%');
    });
  });
}

/* ── STAGGERED SECTION TITLE WORD SPLIT ── */
function initTitleSplit() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const titleObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      titleObs.unobserve(el);

      if (el.dataset.split) return;
      el.dataset.split = '1';

      // Only split plain-text section titles (no child elements like <br>)
      if (el.children.length === 0) {
        const words = el.textContent.split(' ');
        el.innerHTML = words.map((w, i) =>
          `<span class="split-word" style="
            display:inline-block;
            opacity:0;
            transform:translateY(28px);
            filter:blur(4px);
            transition:
              opacity 0.65s cubic-bezier(0.16,1,0.3,1) ${(i * 0.08).toFixed(2)}s,
              transform 0.75s cubic-bezier(0.175,0.885,0.32,1.075) ${(i * 0.08).toFixed(2)}s,
              filter 0.55s ease ${(i * 0.08).toFixed(2)}s;
          ">${w}</span>`
        ).join(' ');

        // Trigger in next frame so transitions fire
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            el.querySelectorAll('.split-word').forEach(span => {
              span.style.opacity = '1';
              span.style.transform = 'translateY(0)';
              span.style.filter = 'blur(0)';
            });
          });
        });
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll('.section-title').forEach(el => titleObs.observe(el));
}

/* ── PREMIUM LINE-BY-LINE HERO TITLES ── */
function initPremiumHeroTitles() {
  const titles = document.querySelectorAll('.premium-hero-title');
  if (!titles.length) return;

  // Reduced-motion: just show immediately, skip all animation
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    titles.forEach(el => el.classList.add('is-premium-ready'));
    return;
  }

  function splitAndAnimate() {
    titles.forEach(el => {
      // Store original markup once; restore before each re-split
      if (!el.dataset.originalHtml) {
        el.dataset.originalHtml = el.innerHTML;
      } else {
        el.innerHTML = el.dataset.originalHtml;
      }

      el.classList.remove('is-premium-ready');

      // Wrap every word (preserving <br> tags) in a measurable inline span
      el.innerHTML = el.innerHTML.replace(
        /(<br\s*\/?>)|([^\s<]+)/gi,
        (match, br, word) => br ? match : `<span class="temp-measure" style="display:inline">${word}</span>`
      );

      const wordSpans = Array.from(el.querySelectorAll('.temp-measure'));
      if (!wordSpans.length) {
        el.classList.add('is-premium-ready');
        return;
      }

      // Group words that share the same offsetTop into lines
      const lines = [];
      let currentLine = [];
      let currentTop = null;

      wordSpans.forEach(span => {
        const top = span.offsetTop;
        if (currentTop === null || Math.abs(top - currentTop) > 4) {
          if (currentLine.length) lines.push(currentLine);
          currentLine = [];
          currentTop = top;
        }
        currentLine.push(span.textContent);
      });
      if (currentLine.length) lines.push(currentLine);

      // Replace content with block-level line spans carrying staggered delays
      el.innerHTML = lines.map((words, i) => {
        const delay = (i * 0.15).toFixed(2);
        return `<span class="premium-line" style="animation-delay:${delay}s">${words.join(' ')}</span>`;
      }).join('');

      // Reveal the container on the very next paint — lines hold opacity:0 via
      // animation-fill-mode:both, so there is zero flash between the two frames.
      requestAnimationFrame(() => el.classList.add('is-premium-ready'));
    });
  }

  splitAndAnimate();

  // Debounced resize: re-measure and re-wrap so responsive reflow never breaks
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(splitAndAnimate, 200);
  }, { passive: true });
}

/* ── IMAGE CLICK ZOOM ── */
function initImageZoom() {
  document.querySelectorAll('.service-image').forEach(container => {
    container.style.cursor = 'pointer';
    container.addEventListener('click', () => {
      const img = container.querySelector('img');
      if (img) {
        img.classList.remove('click-zoom');
        void img.offsetWidth; // trigger reflow
        img.classList.add('click-zoom');
      }
    });
  });
}

/* ── INIT ── */
document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initFAQ();
  initReveal();
  initForms();
  initCounters();
  initCursorGlow();
  initScrollProgress();
  initCardTilt();
  initMagneticButtons();
  initTitleSplit();
  initPremiumHeroTitles();
  initImageZoom();

  // Three.js loads async — init after
  if (typeof THREE !== 'undefined') {
    initHero();
  } else {
    const script = document.querySelector('script[data-three]');
    if (script) script.addEventListener('load', initHero);
  }
});
/* ===== Zoho CRM Popup Form Logic ===== */
function validateEmail1382244000000462509() {
  var form = document.forms['WebToLeads1382244000000462509'];
  var emailFld = form.querySelectorAll('[ftype=email]');
  for (var i = 0; i < emailFld.length; i++) {
    var emailVal = emailFld[i].value;
    if ((emailVal.replace(/^\s+|\s+$/g, '')).length != 0) {
      var atpos = emailVal.indexOf('@');
      var dotpos = emailVal.lastIndexOf('.');
      if (atpos < 1 || dotpos < atpos + 2 || dotpos + 2 >= emailVal.length) {
        alert('Please enter a valid email address.');
        emailFld[i].focus();
        return false;
      }
    }
  }
  return true;
}

function checkMandatory1382244000000462509() {
  var mndFields = ['First Name', 'Last Name', 'Mobile', 'LEADCF1'];
  var fldLangVal = ['First Name', 'Last Name', 'Mobile', 'Interested In'];
  for (var i = 0; i < mndFields.length; i++) {
    var fieldObj = document.forms['WebToLeads1382244000000462509'][mndFields[i]];
    if (fieldObj) {
      if ((fieldObj.value.replace(/^\s+|\s+$/g, '')).length == 0) {
        alert(fldLangVal[i] + ' cannot be empty.');
        fieldObj.focus();
        return false;
      } else if (fieldObj.nodeName == 'SELECT') {
        if (fieldObj.options[fieldObj.selectedIndex].value == '-None-') {
          alert(fldLangVal[i] + ' cannot be none.');
          fieldObj.focus();
          return false;
        }
      }
    }
  }
  if (!validateEmail1382244000000462509()) {
    return false;
  }
  document.querySelector('#formsubmit').setAttribute('disabled', true);
  window.crmFormSubmitting = true;
  return true;
}

document.addEventListener('DOMContentLoaded', function () {
  var overlay = document.getElementById('crm-overlay');
  var closeBtn = document.getElementById('crm-close');
  if (!overlay || !closeBtn) return;

  var lastFocused = null;

  function openModal() {
    lastFocused = document.activeElement;
    overlay.classList.add('visible');
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  }

  function closeModal() {
    if (!overlay.classList.contains('visible')) return;
    overlay.classList.remove('visible');
    document.body.style.overflow = '';
    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }

  window.addEventListener('load', function () {
    setTimeout(openModal, 5000);
  });

  closeBtn.addEventListener('click', closeModal);

  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeModal();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeModal();
  });
});
/* ===== Show thank-you message instead of leaving the site ===== */
window.crmFormSubmitting = false;

document.addEventListener('DOMContentLoaded', function () {
  var hiddenIframe = document.getElementById('hidden_iframe');
  var form = document.getElementById('webform1382244000000462509');
  var thankYou = document.getElementById('crm-thankyou');

  if (hiddenIframe && form && thankYou) {
    hiddenIframe.addEventListener('load', function () {
      if (window.crmFormSubmitting) {
        form.style.display = 'none';
        thankYou.classList.add('visible');
        window.crmFormSubmitting = false;
      }
    });
  }
});