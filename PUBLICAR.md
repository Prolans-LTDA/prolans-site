# Colocar o novo site no ar

Ordem pensada para o site nunca ficar fora do ar. O domínio está no
**Registro.br** (DNS a.sec.dns.br / b.sec.dns.br).

## 1. Repositório na Prolans-LTDA

1. Criar o repositório **Prolans-LTDA/prolans-site** (pode ser privado só se a
   organização tiver plano pago; no plano grátis o Pages exige público).
2. Enviar estes arquivos para a `main`.
3. Em **Settings › Pages**, em *Source*, escolher **GitHub Actions**.
4. Esperar a primeira publicação (aba *Actions*, uns 40 s).

## 2. Trocar o domínio de repositório

Um domínio só pode estar ligado a um repositório do Pages por vez.

1. No repositório antigo **rodrigostuart94-del/SiteProlans**: *Settings ›
   Pages › Custom domain* → **Remove**.
2. No novo **Prolans-LTDA/prolans-site**: *Settings › Pages › Custom domain* →
   `prolans.com.br` → **Save**. Marcar **Enforce HTTPS** quando liberar
   (o certificado leva de minutos a algumas horas).
3. No Registro.br, os quatro registros A de `prolans.com.br` (185.199.108–111.153)
   já são do GitHub Pages e ficam como estão. **Só o `www` muda:** hoje ele é
   um CNAME para `rodrigostuart94-del.github.io`; troque para
   `prolans-ltda.github.io`.

Entre o passo 1 e o 2 o site pode passar um ou dois minutos com erro. Faça os
dois em seguida.

## 3. O sistema em sistema.prolans.com.br

1. **Vercel** › projeto `prolans-erp` › *Settings › Domains* → **Add** →
   `sistema.prolans.com.br` → ambiente **Production**. A Vercel mostra o valor
   do registro CNAME (normalmente `cname.vercel-dns.com`, às vezes um endereço
   próprio do projeto; use o que ela mostrar).
2. **Registro.br** › prolans.com.br › *DNS* › *Editar zona* → **Nova entrada**:
   - Tipo: `CNAME`
   - Nome: `sistema`
   - Dados: o valor mostrado pela Vercel
   - Salvar e esperar a Vercel marcar *Valid Configuration* (alguns minutos).
3. Não mexer nos registros MX e TXT: são do e-mail (Zoho) e do SPF/DKIM.
4. `prolans-erp.vercel.app` continua funcionando: links antigos de nota
   fiscal e de WhatsApp não quebram. Na primeira vez no endereço novo, cada
   pessoa da equipe precisa entrar de novo (a sessão é por endereço).

Opcional: `homologacao.prolans.com.br` apontando para o ramo `homologacao`,
pelo mesmo caminho (na Vercel, escolher *Preview* e o ramo).

## 4. Desligar o Supabase antigo

Depois que o site novo estiver no ar:

1. **Trocar a senha do admin** que ficou escrita no `SUPABASE-SETUP.md` do
   repositório antigo, e em qualquer outro lugar onde ela se repita.
2. Arquivar o repositório antigo (*Settings › Archive*) ou apagar o
   `SUPABASE-SETUP.md` dele. A senha continua no histórico do git, por isso
   trocar é o passo que importa.
3. No painel do Supabase, pausar o projeto `onsdzldigpqsbvlbgvqb`. Antes de
   apagar, conferir se algum cliente chegou a ser cadastrado lá.

## Antes de publicar, conferir

- [ ] `sistema.prolans.com.br` respondendo (o rodapé tem "Acesso da equipe"
      apontando para ele)
- [ ] Área do cliente do sistema publicada (enquanto não estiver, o formulário
      mostra a mensagem que manda pedir o acesso pelo WhatsApp)
- [ ] Textos revisados pelo Stuart, principalmente garantia, prazo de 36 h e
      marcas atendidas
