/* Carry a valid current section to the same article in another language. */
(() => {
  const links = Array.from(document.querySelectorAll('.language-switch a'));
  const base = links.map(link => link.getAttribute('href'));
  function update() {
    let fragment = '';
    try {
      if (location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)))) {
        fragment = location.hash;
      }
    } catch { /* Invalid percent encoding: keep the canonical article URL. */ }
    links.forEach((link, index) => link.setAttribute('href', base[index] + fragment));
  }
  update();
  window.addEventListener('hashchange', update);
})();
