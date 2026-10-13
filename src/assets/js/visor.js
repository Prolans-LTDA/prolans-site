/* O visor da abertura mostra a hora de Teresópolis, como o carimbo de uma câmera. */
(function () {
  "use strict";
  var el = document.getElementById("visor-hora");
  if (!el) return;
  var fmt;
  try {
    fmt = new Intl.DateTimeFormat("pt-BR", { timeZone: "America/Sao_Paulo", day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit", second: "2-digit" });
  } catch (e) { return; }
  function tic() { el.textContent = "REC " + fmt.format(new Date()).replace(",", ""); }
  tic();
  setInterval(tic, 1000);
})();
