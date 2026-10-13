/* Vitrine de soluções: passa sozinha, devagar, e em loop.
   Para quando a pessoa passa o mouse, toca, arrasta, usa as setas ou o
   teclado, e volta a andar alguns segundos depois. Quem pediu ao sistema
   menos movimento (prefers-reduced-motion) vê o carrossel parado. */
(function () {
  "use strict";
  var semMovimento = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var VELOCIDADE = 28;      // pixels por segundo
  var ESPERA = 4000;        // quanto tempo parado depois de mexer

  document.querySelectorAll("[data-carrossel]").forEach(function (c) {
    var trilho = c.querySelector(".trilho");
    var setas = c.querySelectorAll(".carrossel-setas button");
    if (!trilho) return;
    var originais = Array.prototype.slice.call(trilho.children);

    function passo() {
      var item = trilho.querySelector("li");
      return item ? item.getBoundingClientRect().width + 20 : 300;
    }

    /* Cópias no fim para o loop não ter emenda. Ficam fora do leitor de
       tela e do Tab: a lista "de verdade" continua sendo uma só. */
    if (!semMovimento && originais.length > 1) {
      originais.forEach(function (li) {
        var copia = li.cloneNode(true);
        copia.setAttribute("aria-hidden", "true");
        copia.querySelectorAll("a, button").forEach(function (el) { el.setAttribute("tabindex", "-1"); });
        trilho.appendChild(copia);
      });
    }
    function voltaInteira() {
      var primeiraCopia = trilho.children[originais.length];
      return primeiraCopia ? primeiraCopia.offsetLeft - trilho.children[0].offsetLeft : 0;
    }

    var parado = semMovimento, retomar = null, visivel = true, pos = trilho.scrollLeft, antes = 0;

    function pausar() {
      parado = true;
      clearTimeout(retomar);
    }
    function soltar() {
      if (semMovimento) return;
      clearTimeout(retomar);
      retomar = setTimeout(function () {
        pos = trilho.scrollLeft;
        parado = false;
      }, ESPERA);
    }

    function quadro(t) {
      var dt = antes ? Math.min(t - antes, 64) : 0;
      antes = t;
      if (!parado && visivel && !document.hidden) {
        pos += VELOCIDADE * dt / 1000;
        var volta = voltaInteira();
        if (volta > 0 && pos >= volta) pos -= volta;
        trilho.scrollLeft = pos;
      }
      requestAnimationFrame(quadro);
    }

    if (!semMovimento) {
      ["mouseenter", "pointerdown", "touchstart", "focusin", "wheel"].forEach(function (ev) {
        c.addEventListener(ev, pausar, { passive: true });
      });
      ["mouseleave", "pointerup", "touchend", "focusout"].forEach(function (ev) {
        c.addEventListener(ev, soltar, { passive: true });
      });
      c.addEventListener("wheel", soltar, { passive: true });
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (e) { visivel = e[0].isIntersecting; }).observe(c);
      }
      c.classList.add("andando");
      parado = false;
      requestAnimationFrame(quadro);
    }

    function atualizar() {
      if (!semMovimento) return;   // em loop não existe começo nem fim
      var max = trilho.scrollWidth - trilho.clientWidth - 4;
      setas.forEach(function (b) {
        b.disabled = b.getAttribute("data-dir") === "-1" ? trilho.scrollLeft <= 4 : trilho.scrollLeft >= max;
      });
    }
    setas.forEach(function (b) {
      b.addEventListener("click", function () {
        pausar();
        trilho.scrollBy({ left: passo() * Number(b.getAttribute("data-dir")), behavior: "smooth" });
        soltar();
      });
    });
    trilho.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); pausar(); trilho.scrollBy({ left: passo(), behavior: "smooth" }); }
      if (e.key === "ArrowLeft") { e.preventDefault(); pausar(); trilho.scrollBy({ left: -passo(), behavior: "smooth" }); }
    });
    trilho.addEventListener("scroll", atualizar, { passive: true });
    window.addEventListener("resize", atualizar);
    atualizar();
  });
})();
