#!/usr/bin/env python3
"""Monta o site da Prolans.

    python3 build.py            -> dist/     (o que vai para o GitHub Pages)
    python3 build.py --previa   -> previa/   (mesmas páginas, links com index.html)

Cada página mora em src/paginas/*.html. A primeira linha é um comentário
com os dados da página, em JSON:

    <!-- {"caminho": "servicos/", "titulo": "...", "descricao": "...", "menu": "servicos"} -->

Dentro do HTML das páginas:
    {{link:servicos/}}   endereço de outra página (relativo, funciona em qualquer pasta)
    {{raiz}}             prefixo até a raiz, para assets ("../" numa subpágina)
    {{zap}}              link do WhatsApp sem mensagem
    {{zap:texto}}        link do WhatsApp com a mensagem já escrita
    {{sistema}}          endereço do sistema (ERP)
"""
import json, re, shutil, sys, urllib.parse
from pathlib import Path

RAIZ = Path(__file__).parent
SRC = RAIZ / "src"
PREVIA = "--previa" in sys.argv
SAIDA = RAIZ / ("previa" if PREVIA else "dist")

# ----- dados da empresa (um lugar só) -----
SITE = "https://prolans.com.br"
SISTEMA = "https://sistema.prolans.com.br"   # domínio próprio do ERP (ver PUBLICAR.md)
WHATS = "5521997112008"
TEL = "(21) 99711-2008"
EMAIL = "contato@prolans.com.br"
ENDERECO = "Praça Baltazar da Silveira, 90, Várzea, Teresópolis (RJ)"
CNPJ = "38.408.286/0001-11"
GOOGLE = "https://g.page/r/CXIW2HENczCJEBM"
GOOGLE_AVALIAR = "https://g.page/r/CXIW2HENczCJEBM/review"
MAPA = "https://www.google.com/maps/search/?api=1&query=Prolans+Seguran%C3%A7a+e+Tecnologia+Teres%C3%B3polis"
INSTAGRAM = "https://www.instagram.com/contato.prolans"
FACEBOOK = "https://www.facebook.com/contato.prolans"

MENU = [
    ("solucoes", "solucoes/", "Soluções"),
    ("servicos", "servicos/", "Serviços"),
    ("planos", "planos/", "Signature+"),
    ("sobre", "sobre/", "Sobre"),
    ("avaliacoes", "avaliacoes/", "Avaliações"),
    ("faq", "faq/", "Perguntas"),
    ("contato", "contato/", "Contato"),
]

# Aplica o tema antes de pintar a página, para não piscar claro no modo escuro.
TEMA_JS = ("<script>try{var t=localStorage.getItem('prolans-tema');"
           "if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>")


def zap(texto=""):
    base = f"https://wa.me/{WHATS}"
    return base + ("?text=" + urllib.parse.quote(texto) if texto else "")


def rel(de, para):
    """Link relativo da página `de` para `para` (os dois no formato 'servicos/' ou '')."""
    if de == "404":   # a 404 aparece em qualquer endereço: links absolutos
        return "/" + para
    prof = de.count("/")
    pre = "../" * prof
    alvo = para
    if PREVIA:
        alvo = (para + "index.html") if (para == "" or para.endswith("/")) else para
    return (pre + alvo) or "./"


def substituir(html, caminho):
    raiz = "/" if caminho == "404" else "../" * caminho.count("/")
    html = re.sub(r"\{\{link:([^}]*)\}\}", lambda m: rel(caminho, m.group(1)), html)
    html = re.sub(r"\{\{zap:([^}]*)\}\}", lambda m: zap(m.group(1)), html)
    return (html.replace("{{zap}}", zap()).replace("{{raiz}}", raiz)
                .replace("{{sistema}}", SISTEMA).replace("{{tel}}", TEL)
                .replace("{{email}}", EMAIL).replace("{{google}}", GOOGLE)
                .replace("{{google_avaliar}}", GOOGLE_AVALIAR).replace("{{mapa}}", MAPA)
                .replace("{{endereco}}", ENDERECO).replace("{{cnpj}}", CNPJ))


def topo(menu_atual):
    itens = "".join(
        f'<a href="{{{{link:{c}}}}}"{" aria-current=\"page\"" if k == menu_atual else ""}>{t}</a>'
        for k, c, t in MENU)
    return f'''<header class="topo faixa" id="topo">
  <div class="miolo">
    <a class="marca" href="{{{{link:}}}}" aria-label="Prolans, página inicial">
      <img src="{{{{raiz}}}}assets/img/logo-96.webp" width="40" height="40" alt="">
      <span>Prolans<small>Segurança e Tecnologia</small></span>
    </a>
    <nav class="menu" id="menu" aria-label="Principal">{itens}<a class="so-celular" href="{{{{link:area-cliente/}}}}">Área do cliente</a></nav>
    <button class="abre-menu" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
    <div class="topo-acoes">
      <button class="tema" type="button" aria-label="Alternar entre tema claro e escuro" title="Tema claro ou escuro"><svg class="sol"><use href="#i-sol"/></svg><svg class="lua"><use href="#i-lua"/></svg></button>
      <a class="link-cliente" href="{{{{link:area-cliente/}}}}">Área do cliente</a>
      <a class="botao botao-principal" href="{{{{link:orcamento/}}}}">Pedir orçamento</a>
    </div>
  </div>
</header>'''


RODAPE = '''<footer class="rodape faixa">
  <div class="miolo">
    <div class="grade">
      <div>
        <a class="marca" href="{{link:}}"><img src="{{raiz}}assets/img/logo-96.webp" width="40" height="40" alt=""><span>Prolans<small>Segurança e Tecnologia</small></span></a>
        <p>Projeto, instalação e manutenção de segurança eletrônica, redes e automação em Teresópolis, na Região Serrana e no Rio de Janeiro.</p>
      </div>
      <div>
        <h4>Serviços</h4>
        <ul class="limpa">
          <li><a href="{{link:servicos/}}#cftv">Câmeras</a></li>
          <li><a href="{{link:servicos/}}#alarme">Alarmes</a></li>
          <li><a href="{{link:servicos/}}#acesso">Controle de acesso</a></li>
          <li><a href="{{link:servicos/}}#rede">Redes e Wi-Fi</a></li>
          <li><a href="{{link:servicos/}}#automacao">Automação</a></li>
          <li><a href="{{link:planos/}}">Manutenção Signature+</a></li>
        </ul>
      </div>
      <div>
        <h4>Empresa</h4>
        <ul class="limpa">
          <li><a href="{{link:solucoes/}}">Soluções por imóvel</a></li>
          <li><a href="{{link:sobre/}}">Sobre a Prolans</a></li>
          <li><a href="{{link:avaliacoes/}}">Avaliações</a></li>
          <li><a href="{{link:faq/}}">Perguntas frequentes</a></li>
          <li><a href="{{link:area-cliente/}}">Área do cliente</a></li>
          <li><a href="{{sistema}}" rel="nofollow">Acesso da equipe</a></li>
        </ul>
      </div>
      <div>
        <h4>Atendimento</h4>
        <ul class="limpa">
          <li><a href="{{zap}}">WhatsApp {{tel}}</a></li>
          <li><a href="mailto:{{email}}">{{email}}</a></li>
          <li><a href="{{mapa}}">{{endereco}}</a></li>
          <li>Segunda a sexta, 8h às 18h. Sábado, 9h às 13h.</li>
          <li><a href="''' + INSTAGRAM + '''">Instagram</a> e <a href="''' + FACEBOOK + '''">Facebook</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>Prolans Soluções em Tecnologia e Serviços Ltda. CNPJ {{cnpj}}</span>
      <span>Equipamentos das principais marcas</span>
    </div>
  </div>
</footer>
<a class="zap-flutuante" href="{{zap:Olá, vim pelo site da Prolans.}}" aria-label="Conversar no WhatsApp"><svg><use href="#i-zap"/></svg></a>'''

DADOS_EMPRESA = {
    "@context": "https://schema.org", "@type": "LocalBusiness",
    "name": "Prolans Segurança e Tecnologia", "url": SITE,
    "image": SITE + "/assets/img/og.jpg", "logo": SITE + "/assets/img/logo-180.png",
    "telephone": "+55 21 99711-2008", "email": EMAIL,
    "address": {"@type": "PostalAddress", "streetAddress": "Praça Baltazar da Silveira, 90",
                "addressLocality": "Teresópolis", "addressRegion": "RJ", "addressCountry": "BR"},
    "areaServed": ["Teresópolis", "Região Serrana do Rio de Janeiro", "Rio de Janeiro"],
    "openingHours": ["Mo-Fr 08:00-18:00", "Sa 09:00-13:00"],
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "21"},
    "sameAs": [INSTAGRAM, FACEBOOK, GOOGLE],
}


def html_avaliacoes():
    import html as h
    d = json.loads((SRC / "dados" / "avaliacoes.json").read_text(encoding="utf-8"))
    itens = []
    for r in d["reviews"]:
        servico = h.escape(r.get("service") or "Avaliação no Google")
        itens.append(f'<figure><blockquote>“{h.escape(r["text"])}”</blockquote>'
                     f'<figcaption><b>{h.escape(r["name"])}</b>{servico}, {h.escape(r["when"])}</figcaption></figure>')
    return '<div class="depoimentos muitos">' + "".join(itens) + "</div>"


# ---------------- soluções por tipo de imóvel (src/dados/solucoes.json) ----------------
# Regra: só o que a Prolans faz. Nada de obra, cliente, número ou prazo inventado.
import html as _h
ICONE = {"cftv": "camera", "alarme": "alarme", "acesso": "acesso", "fechadura": "fechadura",
         "interfone": "interfone", "portao": "portao", "rede": "rede", "automacao": "automacao",
         "manutencao": "manutencao"}
NOME_SERVICO = {"cftv": "Câmeras", "alarme": "Alarme", "acesso": "Controle de acesso", "fechadura": "Fechadura digital",
                "interfone": "Interfone e videoporteiro", "portao": "Portão eletrônico", "rede": "Redes e Wi-Fi",
                "automacao": "Automação", "manutencao": "Manutenção"}


def dados_solucoes():
    d = json.loads((SRC / "dados" / "solucoes.json").read_text(encoding="utf-8"))
    pasta = SRC / "assets" / "img" / "fotos"
    for n in d["nichos"]:
        n["fotos"] = [f for f in n["fotos"] if (pasta / f"{f['arquivo']}.webp").exists()]
    d["nichos"] = [n for n in d["nichos"] if n["fotos"]]
    return d


def foto(arquivo, alt, lazy=True, w=1200, h=800, cls=""):
    carga = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{{{{raiz}}}}assets/img/fotos/{arquivo}.webp" alt="{_h.escape(alt)}" '
            f'width="{w}" height="{h}"{carga}>')


def html_carrossel():
    d = dados_solucoes()
    itens = []
    for n in d["nichos"]:
        f = n["fotos"][0]
        icones = "".join(f'<svg aria-hidden="true"><use href="#i-{ICONE[s["id"]]}"/></svg>' for s in n["servicos"][:5])
        itens.append(
            f'<li><a class="vitrine" href="{{{{link:solucoes/{n["id"]}/}}}}">{foto(f["arquivo"], f["legenda"])}'
            f'<span class="vitrine-texto"><b>{n["nome"]}</b><span>{_h.escape(n["titulo"])}</span>'
            f'<span class="vitrine-icones">{icones}</span></span></a></li>')
    return ('<div class="carrossel" data-carrossel><ul class="limpa trilho" tabindex="0" aria-label="Soluções por tipo de imóvel">'
            + "".join(itens) + '</ul><div class="carrossel-setas"><button type="button" data-dir="-1" aria-label="Anterior">'
            '<svg><use href="#i-seta"/></svg></button><button type="button" data-dir="1" aria-label="Próximo">'
            '<svg><use href="#i-seta"/></svg></button></div></div>')


def html_grade_solucoes():
    d = dados_solucoes()
    out = []
    for n in d["nichos"]:
        f = n["fotos"][0]
        out.append(f'<a class="vitrine vitrine-grade" href="{{{{link:solucoes/{n["id"]}/}}}}">{foto(f["arquivo"], f["legenda"])}'
                   f'<span class="vitrine-texto"><b>{n["nome"]}</b><span>{_h.escape(n["titulo"])}</span></span></a>')
    return '<div class="grade-solucoes">' + "".join(out) + "</div>"


def html_veja(servico):
    ns = [n for n in dados_solucoes()["nichos"] if any(s["id"] == servico for s in n["servicos"])][:4]
    if not ns:
        return ""
    links = ", ".join(f'<a href="{{{{link:solucoes/{n["id"]}/}}}}">{n["nome"].lower()}</a>' for n in ns)
    return f'<p class="no-projeto"><b>Veja a solução para</b> {links}.</p>'


def paginas_de_solucao():
    d = dados_solucoes()
    ns = d["nichos"]
    for i, n in enumerate(ns):
        ant, prox = ns[i - 1], ns[(i + 1) % len(ns)]
        f0 = n["fotos"][0]
        resto = n["fotos"][1:]
        galeria = ""
        if resto:
            galeria = ('<section class="secao faixa" style="padding-top:0"><div class="miolo galeria">' + "".join(
                f'<figure>{foto(f["arquivo"], f["legenda"])}<figcaption>{_h.escape(f["legenda"])}</figcaption></figure>'
                for f in resto) + "</div></section>")
        importa = "".join(f'<li><svg><use href="#i-ok"/></svg><span>{_h.escape(x)}</span></li>' for x in n["importa"])
        servs = "".join(
            f'<li><svg class="anel"><use href="#i-{ICONE[s["id"]]}"/></svg><div><h3><a href="{{{{link:servicos/}}}}#{s["id"]}">{NOME_SERVICO[s["id"]]}</a></h3>'
            f'<p>{_h.escape(s["texto"])}</p></div></li>' for s in n["servicos"])
        perg = "".join(f'<details><summary>{_h.escape(q)}</summary><div><p>{_h.escape(r)}</p></div></details>'
                       for q, r in n.get("perguntas", []))
        perg_html = f'<section><h2>Perguntas comuns</h2><div class="perguntas">{perg}</div></section>' if perg else ""
        corpo = f'''<section class="capa capa-interna">
  {foto(f0["arquivo"], f0["legenda"], lazy=False, cls="capa-foto")}
  <div class="capa-veu"></div>
  <div class="capa-conteudo faixa"><div class="miolo">
    <nav class="trilha" aria-label="Você está em"><a href="{{{{link:}}}}">Início</a> / <a href="{{{{link:solucoes/}}}}">Soluções</a> / {n["nome"]}</nav>
    <span class="selo-nicho">{n["nome"]}</span>
    <h1>{_h.escape(n["titulo"])}</h1>
    <p>{_h.escape(n["frase"])}</p>
    <div class="acoes"><a class="botao botao-claro" href="{{{{zap:Olá, vim pelo site. Quero um orçamento para {n["nome"].lower()}.}}}}"><svg><use href="#i-zap"/></svg>Pedir orçamento</a></div>
  </div></div>
  <svg class="serra" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><use href="#serra-forma"/></svg>
</section>
<section class="secao faixa">
  <div class="miolo solucao-corpo">
    <div class="texto">
      <section><h2>O que costuma importar</h2><ul class="limpa lista-check">{importa}</ul></section>
      <section><h2>O que a Prolans instala</h2><ul class="limpa lista-servicos">{servs}</ul></section>
      {perg_html}
    </div>
    <aside class="cartao-cta" aria-label="Pedir orçamento">
      <h2>Vamos ver o seu caso?</h2>
      <p>A visita técnica para projetos não tem custo. Você recebe a proposta com cada equipamento e a posição de cada ponto.</p>
      <a class="botao botao-zap" href="{{{{zap:Olá, vim pela página de {n["nome"].lower()} e quero agendar uma visita técnica.}}}}"><svg><use href="#i-zap"/></svg>Agendar visita</a>
      <a class="botao botao-linha" href="{{{{link:orcamento/}}}}">Pedir orçamento pelo site</a>
      <p class="ilustrativo">{_h.escape(f0["legenda"])}</p>
    </aside>
  </div>
</section>
{galeria}
<section class="secao faixa alt">
  <div class="miolo" style="display:grid;gap:1.5rem">
    <h2 style="font-size:var(--t-4)">Outros tipos de imóvel</h2>
    <nav class="vizinhos" aria-label="Outras soluções">
      <a href="{{{{link:solucoes/{ant["id"]}/}}}}"><small>Anterior</small><b>{ant["nome"]}</b></a>
      <a href="{{{{link:solucoes/{prox["id"]}/}}}}"><small>Próximo</small><b>{prox["nome"]}</b></a>
    </nav>
  </div>
</section>'''
        yield ({"caminho": f"solucoes/{n['id']}/", "titulo": f"{n['nome']}: {n['titulo']} | Prolans",
                "descricao": n["frase"], "menu": "solucoes"}, corpo)


def pagina(meta, corpo, sprite):
    for tok, fn in (("{{carrossel}}", html_carrossel), ("{{grade_solucoes}}", html_grade_solucoes)):
        if tok in corpo:
            corpo = corpo.replace(tok, fn())
    if 'class="titulo-pagina' in corpo:   # a serra fecha o título de toda página interna
        i = corpo.index("</section>")
        corpo = corpo[:i] + '<svg class="serra" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><use href="#serra-forma"/></svg>' + corpo[i:]
    corpo = re.sub(r"\{\{veja:(\w+)\}\}", lambda m: html_veja(m.group(1)), corpo)
    if "{{avaliacoes}}" in corpo:
        corpo = corpo.replace("{{avaliacoes}}", html_avaliacoes())
    caminho = meta["caminho"]
    titulo = meta["titulo"]
    if PREVIA and caminho == "":
        titulo = "Novo site Prolans"   # nome da prévia na galeria de artefatos
    desc = meta["descricao"]
    url = SITE + "/" + ("" if caminho == "404" else caminho)
    extra = ""
    if caminho == "":
        extra = '<script type="application/ld+json">' + json.dumps(DADOS_EMPRESA, ensure_ascii=False) + "</script>"
    if meta.get("noindex"):
        extra += '<meta name="robots" content="noindex">'
    if "redireciona" in meta:
        extra += f'<meta http-equiv="refresh" content="0; url={{{{link:{meta["redireciona"]}}}}}">'
    scripts = "".join(f'<script src="{{{{raiz}}}}assets/js/{s}" defer></script>' for s in meta.get("scripts", []))
    cabeca = f'''<title>{titulo}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{titulo}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/img/og.jpg">
<meta name="theme-color" content="#0B2545">
<meta name="color-scheme" content="light dark">
{TEMA_JS}
<link rel="icon" href="{{{{raiz}}}}assets/img/logo-64.png" sizes="64x64">
<link rel="apple-touch-icon" href="{{{{raiz}}}}assets/img/logo-180.png">
<link rel="preload" href="{{{{raiz}}}}assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{{{{raiz}}}}assets/css/site.css">
{extra}
<script src="{{{{raiz}}}}assets/js/site.js" defer></script>{scripts}'''
    corpo_todo = f'''{sprite}
<a class="sr" href="#conteudo">Pular para o conteúdo</a>
{topo(meta.get("menu"))}
<main id="conteudo">
{corpo}
</main>
{RODAPE}'''
    if PREVIA and caminho == "":
        # a página principal da prévia é embrulhada pelo próprio visualizador
        html = cabeca + "\n" + corpo_todo
    else:
        html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{cabeca}
</head>
<body>
{corpo_todo}
</body>
</html>'''
    return substituir(html, caminho)


def main():
    if SAIDA.exists():
        shutil.rmtree(SAIDA)
    shutil.copytree(SRC / "assets", SAIDA / "assets")
    sprite = (SRC / "partials" / "icones.svg").read_text(encoding="utf-8")
    mapa_site = []
    for arq in sorted((SRC / "paginas").glob("*.html")):
        texto = arq.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->\s*", texto, re.S)
        if not m:
            raise SystemExit(f"{arq.name}: falta o comentário com os dados da página")
        meta = json.loads(m.group(1))
        corpo = texto[m.end():]
        if meta["caminho"] == "404":
            if PREVIA:
                continue
            destino = SAIDA / "404.html"
            meta["noindex"] = True
        else:
            destino = SAIDA / meta["caminho"] / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina(meta, corpo, sprite), encoding="utf-8")
        if not meta.get("noindex") and "redireciona" not in meta:
            mapa_site.append(SITE + "/" + meta["caminho"])
    for meta, corpo in paginas_de_solucao():
        destino = SAIDA / meta["caminho"] / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina(meta, corpo, sprite), encoding="utf-8")
        mapa_site.append(SITE + "/" + meta["caminho"])
    if not PREVIA:
        (SAIDA / "CNAME").write_text("prolans.com.br\n")
        (SAIDA / ".nojekyll").write_text("")
        (SAIDA / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
        urls = "".join(f"<url><loc>{u}</loc></url>" for u in sorted(set(mapa_site)))
        (SAIDA / "sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print(f"ok: {SAIDA}  ({len(list((SRC / 'paginas').glob('*.html')))} páginas)")


if __name__ == "__main__":
    main()
