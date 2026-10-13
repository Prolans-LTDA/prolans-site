/* A planta da página inicial: a legenda acende os pontos daquele tipo. */
(function () {
  "use strict";
  var planta = document.getElementById("planta");
  var nota = document.getElementById("planta-nota");
  if (!planta || !nota) return;

  /* a planta se desenha uma vez, quando aparece na tela */
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var obs = new IntersectionObserver(function (itens) {
      itens.forEach(function (i) {
        if (i.isIntersecting) { planta.classList.add("desenhar"); obs.disconnect(); }
      });
    }, { threshold: 0.35 });
    obs.observe(planta);
  }

  var textos = {
    camera: "<b>Câmeras:</b> quatro pontos cobrindo garagem, frente, lateral e fundos. A área sombreada é o que cada uma enxerga.",
    alarme: "<b>Alarme:</b> sensores nas entradas mais vulneráveis, ligados à central e com aviso no celular.",
    fechadura: "<b>Fechadura digital:</b> na porta da frente, com senha, digital e abertura pelo aplicativo.",
    portao: "<b>Portão:</b> motor na garagem, aberto pelo controle ou pelo celular.",
    interfone: "<b>Videoporteiro:</b> no muro, para atender o portão de dentro de casa ou de onde estiver.",
    rede: "<b>Wi-Fi:</b> roteador no centro da casa, que é onde o sinal chega igual em todos os cômodos.",
    acesso: "<b>Controle de acesso:</b> no escritório, com registro de quem entrou e quando.",
    automacao: "<b>Automação:</b> iluminação da sala e da cozinha comandada pelo celular ou por voz."
  };
  var padrao = nota.innerHTML;
  var botoes = Array.prototype.slice.call(document.querySelectorAll(".legenda button[data-k]"));
  var marcados = Array.prototype.slice.call(planta.querySelectorAll("[data-k]"));
  var atual = null;
  var fixo = false; // escolhido na legenda: não some ao tirar o mouse

  function mostrar(k) {
    atual = k;
    planta.classList.toggle("filtrando", !!k);
    marcados.forEach(function (el) {
      el.classList.toggle("ativo", el.getAttribute("data-k") === k);
    });
    botoes.forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-k") === k ? "true" : "false");
    });
    nota.innerHTML = k ? textos[k] : padrao;
  }

  botoes.forEach(function (b) {
    b.addEventListener("click", function () {
      var k = b.getAttribute("data-k");
      fixo = atual !== k;
      mostrar(fixo ? k : null);
    });
  });
  planta.querySelectorAll(".ponto").forEach(function (p) {
    var k = p.getAttribute("data-k");
    p.addEventListener("mouseenter", function () { mostrar(k); });
    p.addEventListener("focus", function () { mostrar(k); });
    p.addEventListener("click", function () { fixo = true; mostrar(k); });
  });
  planta.addEventListener("mouseleave", function () { if (!fixo) mostrar(null); });
})();
