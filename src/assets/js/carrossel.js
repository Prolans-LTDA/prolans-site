/* Vitrine de soluções: rolagem lateral com setas (o arraste e o toque já funcionam sozinhos). */
(function () {
  "use strict";
  document.querySelectorAll("[data-carrossel]").forEach(function (c) {
    var trilho = c.querySelector(".trilho");
    var setas = c.querySelectorAll(".carrossel-setas button");
    if (!trilho) return;
    function passo() {
      var item = trilho.querySelector("li");
      return item ? item.getBoundingClientRect().width + 20 : 300;
    }
    function atualizar() {
      var max = trilho.scrollWidth - trilho.clientWidth - 4;
      setas.forEach(function (b) {
        b.disabled = b.getAttribute("data-dir") === "-1" ? trilho.scrollLeft <= 4 : trilho.scrollLeft >= max;
      });
    }
    setas.forEach(function (b) {
      b.addEventListener("click", function () {
        trilho.scrollBy({ left: passo() * Number(b.getAttribute("data-dir")), behavior: "smooth" });
      });
    });
    trilho.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); trilho.scrollBy({ left: passo(), behavior: "smooth" }); }
      if (e.key === "ArrowLeft") { e.preventDefault(); trilho.scrollBy({ left: -passo(), behavior: "smooth" }); }
    });
    trilho.addEventListener("scroll", atualizar, { passive: true });
    window.addEventListener("resize", atualizar);
    atualizar();
  });
})();
