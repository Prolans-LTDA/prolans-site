/* Prolans — comportamento comum a todas as páginas */
(function () {
  "use strict";
  var raiz = document.documentElement;

  /* menu no celular */
  var topo = document.getElementById("topo");
  var botao = topo && topo.querySelector(".abre-menu");
  if (botao) {
    botao.addEventListener("click", function () {
      var aberto = topo.classList.toggle("aberto");
      botao.setAttribute("aria-expanded", aberto ? "true" : "false");
      botao.textContent = aberto ? "Fechar" : "Menu";
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && topo.classList.contains("aberto")) { botao.click(); botao.focus(); }
    });
  }

  /* tema claro / escuro: começa pelo do aparelho; o botão grava a escolha */
  var tema = document.querySelector(".tema");
  var escuroSistema = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  function atual() {
    var t = raiz.getAttribute("data-theme");
    if (t === "dark" || t === "light") return t;
    return escuroSistema && escuroSistema.matches ? "dark" : "light";
  }
  function rotular() {
    if (!tema) return;
    var t = atual();
    tema.setAttribute("aria-label", t === "dark" ? "Mudar para o tema claro" : "Mudar para o tema escuro");
    tema.title = tema.getAttribute("aria-label");
  }
  if (tema) {
    tema.addEventListener("click", function () {
      var novo = atual() === "dark" ? "light" : "dark";
      raiz.setAttribute("data-theme", novo);
      try { localStorage.setItem("prolans-tema", novo); } catch (e) {}
      rotular();
    });
    if (escuroSistema && escuroSistema.addEventListener) escuroSistema.addEventListener("change", rotular);
    rotular();
  }
})();
