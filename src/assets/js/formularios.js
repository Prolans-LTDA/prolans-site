/* Formulários de contato e orçamento: montam a mensagem e abrem o WhatsApp.
   Nada é gravado no site; o atendimento continua no WhatsApp da Prolans. */
(function () {
  "use strict";
  var WHATS = "5521997112008";

  function abrir(texto) {
    window.location.href = "https://wa.me/" + WHATS + "?text=" + encodeURIComponent(texto);
  }
  function erro(caixa, msg, campo) {
    caixa.textContent = msg;
    caixa.hidden = false;
    if (campo) { campo.setAttribute("aria-invalid", "true"); campo.focus(); }
  }
  function limpar(form, caixa) {
    caixa.hidden = true;
    form.querySelectorAll("[aria-invalid]").forEach(function (c) { c.removeAttribute("aria-invalid"); });
  }

  var orc = document.getElementById("form-orcamento");
  if (orc) {
    var oErro = document.getElementById("o-erro");
    orc.addEventListener("submit", function (e) {
      e.preventDefault();
      limpar(orc, oErro);
      var imovel = (orc.querySelector("input[name=imovel]:checked") || {}).value || "";
      var servicos = Array.prototype.map.call(orc.querySelectorAll("input[name=servico]:checked"), function (c) { return c.value; });
      var cidade = orc.cidade.value.trim(), nome = orc.nome.value.trim(), detalhe = orc.detalhe.value.trim();
      if (!servicos.length) return erro(oErro, "Marque pelo menos um serviço para a equipe saber por onde começar.");
      if (!cidade) return erro(oErro, "Informe a cidade e o bairro: é o que define a visita técnica.", orc.cidade);
      if (!nome) return erro(oErro, "Informe seu nome.", orc.nome);
      var texto = "Olá, vim pelo site e gostaria de um orçamento.\n\n" +
        "Nome: " + nome + "\n" +
        "Imóvel: " + imovel + "\n" +
        "Local: " + cidade + "\n" +
        "Serviços: " + servicos.join(", ") +
        (detalhe ? "\n\n" + detalhe : "");
      abrir(texto);
    });
  }

  var cont = document.getElementById("form-contato");
  if (cont) {
    var cErro = document.getElementById("c-erro");
    cont.addEventListener("submit", function (e) {
      e.preventDefault();
      limpar(cont, cErro);
      var nome = cont.nome.value.trim(), fone = cont.fone.value.trim(), msg = cont.mensagem.value.trim();
      if (!nome) return erro(cErro, "Informe seu nome.", cont.nome);
      if (fone.replace(/\D/g, "").length < 10) return erro(cErro, "Informe o WhatsApp com DDD, para a equipe conseguir responder.", cont.fone);
      if (!msg) return erro(cErro, "Escreva a mensagem.", cont.mensagem);
      abrir("Olá, vim pelo site.\n\nNome: " + nome + "\nWhatsApp: " + fone + "\nAssunto: " + cont.assunto.value + "\n\n" + msg);
    });
  }
})();
