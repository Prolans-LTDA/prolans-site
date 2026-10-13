# Site da Prolans

Site institucional de **prolans.com.br**. HTML e CSS puros, montados por um
script Python sem dependências e publicados pelo GitHub Pages.

## Onde mexer

| Quero mudar…                         | Arquivo                                  |
|--------------------------------------|------------------------------------------|
| Texto de uma página                  | `src/paginas/<página>.html`              |
| Telefone, e-mail, endereço, links    | topo do `build.py` (um lugar só)         |
| Menu e rodapé                        | `build.py` (`MENU`, `topo()`, `RODAPE`)  |
| Avaliações do Google                 | `src/dados/avaliacoes.json`              |
| Cores, fontes, espaçamentos          | `src/assets/css/site.css`                |
| Ícones                               | `src/partials/icones.svg`                |

A primeira linha de cada página é um comentário JSON com caminho, título e
descrição (o que aparece no Google). Links entre páginas usam
`{{link:servicos/}}`, e o WhatsApp com mensagem pronta usa
`{{zap:texto da mensagem}}`.

## Ver no computador

```
python build.py
python -m http.server 8080 --directory dist
```

Abra http://localhost:8080.

## Publicar

Todo push na `main` monta e publica sozinho (`.github/workflows/pages.yml`).
O passo a passo do domínio está em `PUBLICAR.md`.

## Regras do site

- **Sem preço, promoção ou condição de pagamento.** O site apresenta o serviço
  pelo que ele resolve e leva para o orçamento.
- **Nenhum número que não se possa provar.** Quantidade de clientes, anos de
  experiência e cursos só entram com a fonte do número.
- **Nenhum dado de cliente mora no site.** A área do cliente é servida pelo
  sistema (sistema.prolans.com.br); o site só pede o link de acesso.
- **Nenhuma senha, chave ou token neste repositório.**
- Fontes hospedadas aqui mesmo, sem chamar o Google Fonts.
