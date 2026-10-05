#!/usr/bin/env python3
"""Gera as páginas de cada área (uma pasta por página), o sitemap.xml e o robots.txt.

Uso: python3 scripts/gerar-paginas.py   (rodar na raiz do projeto)
Para mudar um texto, edite o dicionário AREAS abaixo e rode de novo.
"""
import json
import urllib.parse
from datetime import date
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITE = "https://resendepericias.com.br"
WHATSAPP = "5531971087909"

AREAS = [
    {
        "slug": "assistente-tecnico-pericia-medica",
        "menu": "Assistente técnico",
        "titulo_seo": "Assistente Técnico em Perícia Médica | Resende Perícias Médicas",
        "descricao": "Assistente técnica médica para advogados em todo o Brasil: análise de viabilidade, quesitos, acompanhamento da perícia e parecer técnico para impugnar o laudo.",
        "sobretitulo": "Assistência técnica médica",
        "h1": "Assistente técnico em <em>perícia médica.</em>",
        "lead": "Em processo com prova médica, o laudo pericial costuma decidir o resultado. A assistente técnica é a médica do seu lado: traduz o prontuário, direciona a perícia e sustenta a impugnação.",
        "quando": [
            "Antes de ajuizar, para saber se a tese se sustenta do ponto de vista médico.",
            "Logo após a nomeação do perito: o prazo para indicar assistente e apresentar quesitos é de 15 dias (CPC, art. 465, § 1º).",
            "No dia do exame pericial, para acompanhar a perícia e fazer perguntas ao periciado.",
            "Depois do laudo: o parecer do assistente técnico deve ser apresentado em 15 dias da intimação (CPC, art. 477, § 1º).",
        ],
        "pontos": [
            ("Quesitos que conduzem", "Perguntas objetivas levam o perito ao ponto que decide a causa, em vez de respostas genéricas."),
            ("Presença no exame", "O acompanhamento garante que sintomas, limitações e documentos sejam efetivamente considerados."),
            ("Parecer fundamentado", "Análise crítica do laudo com literatura médica, normas e prontuário: a base técnica da impugnação."),
        ],
        "faq": [
            ("O que faz um assistente técnico em perícia médica?", "É o médico indicado pela parte para acompanhar a perícia judicial. Ele formula quesitos, acompanha o exame, analisa o laudo do perito e apresenta parecer técnico próprio, que serve de base para a manifestação do advogado."),
            ("Qual a diferença entre perito e assistente técnico?", "O perito é nomeado pelo juiz e deve ser imparcial. O assistente técnico é escolhido pela parte e atua na defesa técnica da tese, sempre com fundamento científico."),
            ("A assistência técnica pode ser feita a distância?", "Sim. Análise de documentos, quesitos e pareceres são feitos a distância, para processos de todo o Brasil. O acompanhamento presencial do exame é combinado conforme a cidade."),
        ],
    },
    {
        "slug": "pericia-inss-bpc",
        "menu": "INSS e BPC",
        "titulo_seo": "Assistente Técnico em Perícia do INSS e BPC/LOAS | Resende Perícias",
        "descricao": "Assistência técnica médica em ações previdenciárias: auxílio por incapacidade, aposentadoria por incapacidade, auxílio-acidente e BPC/LOAS. Quesitos, acompanhamento e parecer.",
        "sobretitulo": "Previdenciário",
        "h1": "Perícia do INSS e <em>BPC/LOAS.</em>",
        "lead": "Nas ações contra o INSS, a perícia judicial define se há incapacidade, desde quando e por quanto tempo. Uma análise técnica bem feita evita laudos que ignoram documentos ou a realidade do trabalho do segurado.",
        "quando": [
            "Benefício por incapacidade negado ou cessado: auxílio-doença, aposentadoria por incapacidade permanente.",
            "Auxílio-acidente, quando há sequela que reduz a capacidade para o trabalho habitual.",
            "BPC/LOAS da pessoa com deficiência, em que a avaliação considera impedimentos de longo prazo.",
            "Divergência sobre a data de início da incapacidade (DII), decisiva para o direito e para os atrasados.",
        ],
        "pontos": [
            ("Data de início da incapacidade", "Os documentos médicos precisam sustentar a DII pretendida; é onde muitas ações se perdem."),
            ("Atividade habitual", "A incapacidade é avaliada em relação ao trabalho que a pessoa de fato exerce, não a um trabalho qualquer."),
            ("Doenças que oscilam", "Quadros psiquiátricos, reumatológicos e dores crônicas exigem leitura cuidadosa do histórico, não só do dia do exame."),
        ],
        "faq": [
            ("Vale a pena ter assistente técnico em perícia do INSS?", "Sim, especialmente quando o caso depende de documentos extensos, de doenças que oscilam ou da data de início da incapacidade. Quesitos bem formulados e um parecer técnico aumentam as chances de o laudo refletir o quadro real."),
            ("O assistente técnico pode acompanhar a perícia na Justiça Federal?", "Sim. As partes podem indicar assistente técnico e apresentar quesitos; o acompanhamento do exame segue as regras do juízo."),
            ("O que preciso enviar para a análise?", "Relatórios médicos, exames, histórico de afastamentos, a decisão do INSS e, se já houver, o laudo pericial e os quesitos do processo."),
        ],
    },
    {
        "slug": "pericia-erro-medico",
        "menu": "Erro médico",
        "titulo_seo": "Perícia em Erro Médico: Assistente Técnico | Resende Perícias Médicas",
        "descricao": "Assistência técnica em ações de erro médico e responsabilidade civil em saúde: nexo entre conduta e dano, falha de diagnóstico, dano estético e óbito. Atuação em todo o Brasil.",
        "sobretitulo": "Responsabilidade civil em saúde",
        "h1": "Perícia em <em>erro médico.</em>",
        "lead": "Ações de erro médico são decididas pela prova técnica: o que era esperado naquele atendimento, o que foi feito e se existe nexo entre a conduta e o dano. Cada detalhe do prontuário conta.",
        "quando": [
            "Antes da ação, para avaliar se o prontuário sustenta a tese de falha, de qualquer das partes.",
            "Casos com mais de uma especialidade, hospital ou plano de saúde envolvidos.",
            "Óbito, internações prolongadas e UTI, em que a cronologia do atendimento é decisiva.",
            "Dano estético, com necessidade de quantificação e registro fotográfico.",
        ],
        "pontos": [
            ("Cronologia do atendimento", "Reconstruir hora a hora o que aconteceu revela atrasos, omissões ou condutas adequadas."),
            ("Conduta esperada", "A análise compara o que foi feito com protocolos, diretrizes e a literatura vigente à época dos fatos."),
            ("Nexo causal", "Nem todo resultado ruim decorre de erro; o parecer demonstra, com fundamento, se a conduta causou ou agravou o dano."),
        ],
        "faq": [
            ("Quando contratar um assistente técnico em ação de erro médico?", "O ideal é antes do ajuizamento, com a análise de viabilidade do prontuário. Durante o processo, o assistente formula quesitos, acompanha a perícia e apresenta parecer sobre o laudo."),
            ("O assistente técnico atende só pacientes ou também médicos e hospitais?", "Atende qualquer das partes: pacientes e familiares, médicos, hospitais e operadoras. O trabalho é sempre técnico e fundamentado."),
            ("Como é definido o valor em casos de erro médico?", "Pelo volume de documentos, número de especialidades e de réus, e pela complexidade do caso. O orçamento é enviado por escrito, após a análise inicial."),
        ],
    },
    {
        "slug": "pericia-trabalhista",
        "menu": "Trabalhista",
        "titulo_seo": "Assistente Técnico em Perícia Médica Trabalhista | Resende Perícias",
        "descricao": "Assistência técnica médica em perícias trabalhistas: doença ocupacional, acidente de trabalho, nexo causal, incapacidade e visita ao local de trabalho.",
        "sobretitulo": "Trabalhista",
        "h1": "Perícia médica <em>trabalhista.</em>",
        "lead": "Na Justiça do Trabalho, a perícia médica define se a doença tem relação com o trabalho, qual a extensão do dano e se há incapacidade. O nexo causal costuma ser o centro da disputa.",
        "quando": [
            "Doença ocupacional: LER/DORT, coluna, perda auditiva, transtornos mentais relacionados ao trabalho.",
            "Acidente de trabalho com sequela ou afastamento.",
            "Discussão sobre nexo causal ou concausa entre a atividade e a doença.",
            "Necessidade de visita ao posto de trabalho para avaliar ergonomia e ambiente.",
        ],
        "pontos": [
            ("Nexo e concausa", "O trabalho não precisa ser a única causa; demonstrar a contribuição da atividade muda o resultado."),
            ("Posto de trabalho", "Quando o nexo depende da ergonomia ou do ambiente, a visita ao local dá base concreta ao parecer."),
            ("Grau de incapacidade", "A extensão da limitação influencia indenização e pensão; precisa ser medida com critério técnico."),
        ],
        "faq": [
            ("O que é nexo causal na perícia trabalhista?", "É a relação entre a atividade de trabalho e a doença ou lesão. A perícia avalia se o trabalho causou, agravou ou contribuiu (concausa) para o quadro."),
            ("A visita ao local de trabalho é sempre necessária?", "Não. Ela é indicada quando o nexo depende de ver o posto, a ergonomia ou o ambiente, e é combinada à parte."),
            ("O assistente técnico atende empregado e empresa?", "Sim. A assistência técnica pode ser contratada por qualquer das partes do processo."),
        ],
    },
    {
        "slug": "pericia-curatela-interdicao",
        "menu": "Curatela",
        "titulo_seo": "Perícia Médica em Curatela e Interdição | Resende Perícias Médicas",
        "descricao": "Perícia e assistência técnica em ações de curatela, interdição e tomada de decisão apoiada: avaliação do discernimento para os atos da vida civil. Também home care.",
        "sobretitulo": "Família e capacidade civil",
        "h1": "Curatela, interdição e <em>home care.</em>",
        "lead": "Nas ações de curatela, a perícia avalia o discernimento da pessoa para os atos da vida civil e os limites que a curatela deve ter. Nas ações de home care, avalia a indicação e a manutenção da internação domiciliar.",
        "quando": [
            "Ações de curatela (interdição) por demência, deficiência intelectual, transtornos mentais graves ou sequelas neurológicas.",
            "Tomada de decisão apoiada, quando a pessoa precisa de apoio sem perder a autonomia.",
            "Revisão ou levantamento de curatela já existente.",
            "Pedidos de home care e de manutenção de internação domiciliar contra planos de saúde.",
        ],
        "pontos": [
            ("Discernimento por tipo de ato", "A curatela atinge atos patrimoniais e negociais; o laudo precisa dizer o que a pessoa consegue ou não decidir."),
            ("Prognóstico", "Se o quadro é permanente, progressivo ou reversível muda a extensão e a revisão da curatela."),
            ("Indicação técnica do home care", "Critérios de complexidade e dependência sustentam ou afastam a necessidade de internação domiciliar."),
        ],
        "faq": [
            ("O que a perícia de curatela avalia?", "Avalia se a pessoa tem discernimento para os atos da vida civil, especialmente os de natureza patrimonial e negocial, e se a condição é permanente ou pode melhorar."),
            ("A perícia pode ser feita em casa ou no hospital?", "Sim, quando a pessoa não pode se deslocar. A forma do exame segue a determinação do juízo."),
            ("A perícia também serve para pedidos de home care?", "Sim. A análise técnica avalia se há indicação de internação domiciliar e quais recursos são necessários."),
        ],
    },
    {
        "slug": "dano-corporal-estetico",
        "menu": "Dano corporal",
        "titulo_seo": "Perícia de Dano Corporal e Dano Estético | Resende Perícias Médicas",
        "descricao": "Avaliação e quantificação do dano corporal e do dano estético em acidentes e lesões: sequelas, incapacidade e repercussões na vida da vítima. Assistência técnica em todo o Brasil.",
        "sobretitulo": "Acidentes e lesões",
        "h1": "Dano corporal e <em>dano estético.</em>",
        "lead": "Em acidentes de trânsito, de consumo ou lesões em geral, o valor da indenização depende de como o dano é descrito e quantificado. Um laudo vago tende a reduzir a reparação.",
        "quando": [
            "Acidentes de trânsito com sequelas físicas ou cicatrizes.",
            "Lesões em estabelecimentos, produtos ou serviços (relação de consumo).",
            "Seguros de pessoas e discussões sobre grau de invalidez.",
            "Cicatrizes, amputações e deformidades com repercussão estética.",
        ],
        "pontos": [
            ("Quantificação", "Escalas e tabelas reconhecidas transformam a sequela em medida objetiva, comparável e defensável."),
            ("Dano estético", "Localização, extensão e visibilidade da lesão precisam ser descritas e documentadas com precisão."),
            ("Repercussões", "Efeitos no trabalho, nas atividades diárias e na vida social completam o retrato do dano."),
        ],
        "faq": [
            ("Qual a diferença entre dano corporal e dano estético?", "Dano corporal é a lesão e suas consequências funcionais. Dano estético é a alteração na aparência, como cicatrizes e deformidades, e pode ser indenizado de forma autônoma."),
            ("Como o dano estético é medido?", "Por escalas reconhecidas em perícia, que consideram localização, tamanho, visibilidade e impacto, com registro fotográfico."),
            ("O assistente técnico ajuda em ações de seguro?", "Sim. Nas discussões sobre grau de invalidez, o parecer técnico confronta a tabela aplicada com a sequela real."),
        ],
    },
]


def cabecalho():
    return f'''  <a class="pular" href="#conteudo">Pular para o conteúdo</a>
  <header class="topo rolou" data-topo>
    <div class="topo__faixa envelope">
      <a class="topo__marca" href="/" aria-label="Resende Perícias Médicas, página inicial">
        <img src="/assets/marca/logo-claro.svg" alt="Resende Perícias Médicas" width="210" height="58">
      </a>
      <nav class="topo__nav" aria-label="Seções">
        <a href="/#sobre">Quem sou</a>
        <a href="/#atuacao">Atuação</a>
        <a href="/#areas">Áreas</a>
        <a href="/#convenio">Convênio OAB</a>
        <a href="/#duvidas">Dúvidas</a>
      </nav>
      <a class="botao botao--ouro botao--pequeno topo__cta" href="#contato">Fale sobre seu caso</a>
      <button class="topo__menu" type="button" aria-expanded="false" aria-controls="menu-movel" data-menu>
        <span></span><span></span><span class="sr">Abrir menu</span>
      </button>
    </div>
    <nav class="menu-movel" id="menu-movel" aria-label="Seções" hidden>
      <a href="/">Início</a>
      <a href="/#sobre">Quem sou</a>
      <a href="/#areas">Áreas</a>
      <a href="/#convenio">Convênio OAB</a>
      <a href="#contato" class="botao botao--ouro">Fale sobre seu caso</a>
    </nav>
  </header>'''


def rodape():
    return '''  <footer class="rodape">
    <div class="rodape__grade envelope">
      <img src="/assets/marca/logo-claro.svg" alt="Resende Perícias Médicas" width="190" height="52">
      <p>
        Responsável técnica: Dra. Priscila Cintra Campos Resende · Médica · CRM/MG 72810<br>
        Belo Horizonte, Minas Gerais · atuação em todo o Brasil<br>
        <a href="mailto:contato@resendepericias.com.br">contato@resendepericias.com.br</a> ·
        <a href="https://www.instagram.com/resendepericiasmedicas/" target="_blank" rel="noopener">Instagram</a> ·
        Conveniada OAB/MG · CAAMG
      </p>
      <p class="rodape__legal">
        Conteúdo de caráter informativo, conforme as normas de publicidade médica do Conselho Federal de Medicina.
        © <span data-ano>2026</span> Resende Perícias Médicas · Resende Soluções Médicas Ltda. · CNPJ 37.037.770/0001-19
      </p>
    </div>
  </footer>

  <a class="flutuante" href="https://wa.me/5531971087909" target="_blank" rel="noopener" aria-label="Conversar pelo WhatsApp">
    <svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3Zm0 23.6a10.6 10.6 0 0 1-5.4-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6Zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7a.6.6 0 0 0 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.7 3.7 0 0 0-1.1 2.7 6.4 6.4 0 0 0 1.3 3.4 14.6 14.6 0 0 0 5.6 5c2.1.9 2.9 1 4 .8a3.4 3.4 0 0 0 2.2-1.6 2.8 2.8 0 0 0 .2-1.6c-.1-.1-.3-.2-.6-.4Z"/></svg>
  </a>'''


def pagina(a):
    url = f"{SITE}/{a['slug']}/"
    texto_h1 = a["h1"].replace("<em>", "").replace("</em>", "")
    wa = f"https://wa.me/{WHATSAPP}?text=" + urllib.parse.quote(
        f"Olá, Dra. Priscila. Vim pelo site e gostaria de falar sobre um caso de {a['menu'].lower()}."
    )
    dados = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "name": texto_h1,
                "serviceType": a["sobretitulo"],
                "description": a["descricao"],
                "url": url,
                "areaServed": [{"@type": "State", "name": "Minas Gerais"}, {"@type": "Country", "name": "Brasil"}],
                "provider": {"@id": f"{SITE}/#empresa"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": texto_h1, "item": url},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}}
                    for p, r in a["faq"]
                ],
            },
        ],
    }
    quando = "\n".join(f"            <li>{escape(q)}</li>" for q in a["quando"])
    pontos = "\n".join(
        f'''          <li class="revelar">
            <h3>{escape(t)}</h3>
            <p>{escape(d)}</p>
          </li>''' for t, d in a["pontos"]
    )
    faq = "\n".join(
        f'''          <details class="revelar">
            <summary>{escape(p)}</summary>
            <p>{escape(r)}</p>
          </details>''' for p, r in a["faq"]
    )
    outras = "\n".join(
        f'          <li><a class="link-seta" href="/{o["slug"]}/">{o["menu"]}</a></li>'
        for o in AREAS if o["slug"] != a["slug"]
    )
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(a["titulo_seo"])}</title>
  <meta name="description" content="{escape(a["descricao"])}">
  <meta name="theme-color" content="#141A29">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="Resende Perícias Médicas">
  <meta property="og:title" content="{escape(a["titulo_seo"])}">
  <meta property="og:description" content="{escape(a["descricao"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/compartilhar.jpg">
  <link rel="icon" href="/assets/marca/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/marca/icone-180.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/site.css">
  <script type="application/ld+json">
{json.dumps(dados, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
{cabecalho()}

  <main id="conteudo">
    <section class="area-capa">
      <div class="envelope">
        <nav class="migalhas" aria-label="Você está em"><a href="/">Início</a> <span aria-hidden="true">/</span> <span>{escape(a["menu"])}</span></nav>
        <p class="sobretitulo revelar">{escape(a["sobretitulo"])}</p>
        <h1 class="titulo titulo--claro titulo--grande revelar">{a["h1"]}</h1>
        <p class="area-capa__lead revelar">{escape(a["lead"])}</p>
        <div class="capa__acoes area-capa__acoes revelar">
          <a class="botao botao--ouro" href="#contato">Fale sobre seu caso</a>
          <a class="botao botao--linha" href="/#metodo">Como trabalho</a>
        </div>
      </div>
    </section>

    <section class="secao secao--papel">
      <div class="area-texto envelope">
        <div>
          <p class="sobretitulo sobretitulo--escuro revelar">Quando faz diferença</p>
          <h2 class="titulo revelar">O momento certo de <em>chamar.</em></h2>
        </div>
        <ul class="area-lista revelar">
{quando}
        </ul>
      </div>
    </section>

    <section class="secao secao--noite">
      <div class="envelope">
        <div class="cabeca-secao">
          <p class="sobretitulo revelar">O que costuma decidir</p>
          <h2 class="titulo titulo--claro revelar">Pontos que merecem <em>atenção.</em></h2>
        </div>
        <ul class="area-pontos">
{pontos}
        </ul>
      </div>
    </section>

    <section class="secao secao--papel">
      <div class="duvidas envelope" style="padding-top:0;border-top:0">
        <div class="duvidas__cabeca">
          <p class="sobretitulo sobretitulo--escuro revelar">Dúvidas frequentes</p>
          <h2 class="titulo revelar">Perguntas sobre <em>{escape(a["menu"].lower())}.</em></h2>
        </div>
        <div class="duvidas__lista">
{faq}
        </div>
      </div>
    </section>

    <section class="contato" id="contato">
      <div class="envelope area-contato">
        <p class="sobretitulo revelar">Contato</p>
        <h2 class="titulo titulo--claro titulo--grande revelar">Fale sobre seu <em>caso.</em></h2>
        <p class="contato__lead revelar">Perita judicial em Minas Gerais e assistente técnica em todo o Brasil. Envie os documentos para uma primeira análise; o orçamento vem por escrito.</p>
        <div class="capa__acoes revelar">
          <a class="botao botao--ouro" href="{wa}" target="_blank" rel="noopener">Conversar pelo WhatsApp</a>
          <a class="botao botao--linha" href="mailto:contato@resendepericias.com.br">contato@resendepericias.com.br</a>
        </div>
        <div class="area-outras revelar">
          <p class="sobretitulo">Outras áreas</p>
          <ul>
{outras}
          </ul>
        </div>
      </div>
    </section>
  </main>

{rodape()}

  <script src="/assets/js/site.js" defer></script>
</body>
</html>
'''


def main():
    hoje = date.today().isoformat()
    urls = [f"{SITE}/"]
    for a in AREAS:
        pasta = RAIZ / a["slug"]
        pasta.mkdir(exist_ok=True)
        (pasta / "index.html").write_text(pagina(a), encoding="utf-8")
        urls.append(f"{SITE}/{a['slug']}/")
    mapa = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{hoje}</lastmod><priority>{'1.0' if u == SITE + '/' else '0.8'}</priority></url>"
        for u in urls
    )
    (RAIZ / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{mapa}\n</urlset>\n',
        encoding="utf-8",
    )
    (RAIZ / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"{len(AREAS)} páginas, sitemap com {len(urls)} endereços.")


if __name__ == "__main__":
    main()
