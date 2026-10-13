/* Área do cliente: pede ao sistema da Prolans (ERP) um link de acesso.
   O site não guarda nada. Quem decide se o e-mail é de um cliente é o ERP,
   e a resposta é a mesma nos dois casos, para ninguém usar este formulário
   para descobrir quem é cliente da Prolans. */
(function () {
  "use strict";
  var form = document.getElementById("form-acesso");
  if (!form) return;
  var sistema = form.getAttribute("data-sistema");
  var retorno = document.getElementById("a-retorno");
  var botao = document.getElementById("a-enviar");
  var campo = form.email;

  function mostrar(tipo, html) {
    retorno.className = "aviso aviso-" + tipo;
    retorno.innerHTML = html;
    retorno.hidden = false;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    campo.removeAttribute("aria-invalid");
    var email = campo.value.trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      campo.setAttribute("aria-invalid", "true");
      campo.focus();
      return mostrar("erro", "Confira o e-mail: falta o @ ou o domínio.");
    }
    botao.disabled = true;
    botao.textContent = "Enviando…";
    fetch(sistema + "/api/portal/acesso", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email })
    }).then(function (r) {
      if (r.status === 429) {
        mostrar("erro", "Foram muitos pedidos seguidos. Espere alguns minutos e tente de novo.");
        return;
      }
      if (!r.ok) throw new Error("status " + r.status);
      mostrar("ok", "Pronto. Se <b>" + email.replace(/[<>&"]/g, "") + "</b> estiver cadastrado, o link chega em alguns minutos. Confira também a caixa de spam.");
      form.reset();
    }).catch(function () {
      mostrar("erro", "Não conseguimos falar com o sistema agora. Tente de novo em instantes ou peça o acesso pelo WhatsApp.");
    }).then(function () {
      botao.disabled = false;
      botao.textContent = "Enviar link de acesso";
    });
  });
})();
