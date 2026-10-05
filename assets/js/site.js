// Resende Perícias Médicas — comportamentos leves do site (sem dependências).
document.documentElement.classList.add('js');

// Cabeçalho ganha fundo depois de rolar
const topo = document.querySelector('[data-topo]');
const marcarRolagem = () => topo.classList.toggle('rolou', window.scrollY > 24);
marcarRolagem();
window.addEventListener('scroll', marcarRolagem, { passive: true });

// Menu do celular
const botaoMenu = document.querySelector('[data-menu]');
const menu = document.getElementById('menu-movel');
const fecharMenu = () => { botaoMenu.setAttribute('aria-expanded', 'false'); menu.hidden = true; topo.classList.toggle('rolou', window.scrollY > 24); };
botaoMenu.addEventListener('click', () => {
  const abrir = botaoMenu.getAttribute('aria-expanded') !== 'true';
  botaoMenu.setAttribute('aria-expanded', String(abrir));
  menu.hidden = !abrir;
  if (abrir) topo.classList.add('rolou');
});
menu.addEventListener('click', (e) => { if (e.target.closest('a')) fecharMenu(); });

// Títulos entram palavra por palavra (o texto continua legível para leitores de tela)
const semMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!semMovimento) {
  document.querySelectorAll('.titulo').forEach((titulo) => {
    let i = 0;
    const percorrer = (no) => {
      [...no.childNodes].forEach((filho) => {
        if (filho.nodeType === 3) {
          const frag = document.createDocumentFragment();
          filho.textContent.split(/(\s+)/).forEach((parte) => {
            if (!parte) return;
            if (/^\s+$/.test(parte)) { frag.append(' '); return; }
            const caixa = document.createElement('span');
            caixa.className = 'palavra';
            const interno = document.createElement('span');
            interno.style.setProperty('--i', i++);
            interno.textContent = parte;
            caixa.append(interno);
            frag.append(caixa);
          });
          filho.replaceWith(frag);
        } else if (filho.nodeType === 1) {
          percorrer(filho);
        }
      });
    };
    percorrer(titulo);
  });
}

// Revelação suave ao entrar na tela
const revelaveis = document.querySelectorAll('.revelar');
if ('IntersectionObserver' in window) {
  const observador = new IntersectionObserver((entradas) => {
    entradas.forEach((entrada) => {
      if (!entrada.isIntersecting) return;
      entrada.target.classList.add('visivel');
      observador.unobserve(entrada.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  revelaveis.forEach((el, i) => {
    // pequeno escalonamento entre irmãos
    const irmaos = [...el.parentElement.children].filter((c) => c.classList.contains('revelar'));
    const ordem = irmaos.indexOf(el);
    el.style.transitionDelay = el.closest('.capa') ? `${250 + ordem * 160}ms` : `${Math.min(ordem, 5) * 80}ms`;
    observador.observe(el);
  });
} else {
  revelaveis.forEach((el) => el.classList.add('visivel'));
}

// Formulário: monta a mensagem e abre o WhatsApp (o site não guarda nada)
const WHATSAPP = '5531971087909';
const formulario = document.querySelector('[data-formulario]');
formulario.addEventListener('submit', (e) => {
  e.preventDefault();
  const dados = new FormData(formulario);
  const nome = String(dados.get('nome') || '').trim();
  const campoNome = formulario.elements.nome;
  if (!nome) { campoNome.setAttribute('aria-invalid', 'true'); campoNome.focus(); return; }
  campoNome.removeAttribute('aria-invalid');
  const linhas = [
    `Olá, Dra. Priscila. Meu nome é ${nome}.`,
    `Sou: ${dados.get('perfil')}.`,
    `Área do caso: ${dados.get('area')}.`,
  ];
  const mensagem = String(dados.get('mensagem') || '').trim();
  if (mensagem) linhas.push('', mensagem);
  window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(linhas.join('\n'))}`, '_blank', 'noopener');
});

document.querySelectorAll('[data-ano]').forEach((el) => { el.textContent = new Date().getFullYear(); });

// Botões que já escolhem o perfil no formulário (ex.: parceria OAB → advogado)
document.querySelectorAll('[data-perfil]').forEach((botao) => {
  botao.addEventListener('click', () => { formulario.elements.perfil.value = botao.dataset.perfil; });
});

// O site sempre abre na capa (sem restaurar a rolagem anterior), exceto quando o link aponta uma seção
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
if (!location.hash) window.scrollTo(0, 0);

// ---------- Efeitos ----------

// Luz que segue o mouse (capa e cartões)
const capa = document.querySelector('.capa');
const luzCapa = document.querySelector('.capa__luz');
capa.addEventListener('pointermove', (e) => {
  const r = capa.getBoundingClientRect();
  luzCapa.style.setProperty('--mx', `${e.clientX - r.left}px`);
  luzCapa.style.setProperty('--my', `${e.clientY - r.top}px`);
});
document.querySelectorAll('[data-luz]').forEach((el) => {
  el.addEventListener('pointermove', (e) => {
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', `${e.clientX - r.left}px`);
    el.style.setProperty('--my', `${e.clientY - r.top}px`);
  });
});

// Contagem animada (~1.000)
const contadores = document.querySelectorAll('[data-contar]');
if (!semMovimento && 'IntersectionObserver' in window) {
  const formatar = (n) => `~${n.toLocaleString('pt-BR')}`;
  const obsContar = new IntersectionObserver((entradas) => {
    entradas.forEach((entrada) => {
      if (!entrada.isIntersecting) return;
      obsContar.unobserve(entrada.target);
      const el = entrada.target, alvo = Number(el.dataset.contar), inicio = performance.now(), dur = 1800;
      const passo = (agora) => {
        const t = Math.min((agora - inicio) / dur, 1);
        el.textContent = formatar(Math.round(alvo * (1 - Math.pow(1 - t, 4))));
        if (t < 1) requestAnimationFrame(passo);
      };
      el.textContent = formatar(0);
      requestAnimationFrame(passo);
    });
  }, { threshold: 0.6 });
  contadores.forEach((el) => obsContar.observe(el));
}

// Poeira dourada na capa: poucas partículas, lentas, só enquanto a capa está visível
const tela = document.querySelector('.capa__poeira');
if (tela && !semMovimento) {
  const ctx = tela.getContext('2d');
  let largura = 0, altura = 0, particulas = [], ativa = true, quadro = 0;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const montar = () => {
    largura = tela.clientWidth; altura = tela.clientHeight;
    tela.width = largura * dpr; tela.height = altura * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const total = Math.round(Math.min(70, largura * altura / 22000));
    particulas = Array.from({ length: total }, () => ({
      x: Math.random() * largura, y: Math.random() * altura,
      r: Math.random() * 1.4 + .3, v: Math.random() * .22 + .05,
      d: (Math.random() - .5) * .15, a: Math.random() * .5 + .15, f: Math.random() * Math.PI * 2,
    }));
  };
  const desenhar = () => {
    ctx.clearRect(0, 0, largura, altura);
    particulas.forEach((p) => {
      p.y -= p.v; p.x += p.d; p.f += .015;
      if (p.y < -5) { p.y = altura + 5; p.x = Math.random() * largura; }
      ctx.globalAlpha = p.a * (.6 + .4 * Math.sin(p.f));
      ctx.fillStyle = '#E4D3AC';
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
    });
    if (ativa) quadro = requestAnimationFrame(desenhar);
  };
  montar(); desenhar();
  window.addEventListener('resize', montar);
  new IntersectionObserver(([e]) => {
    ativa = e.isIntersecting;
    cancelAnimationFrame(quadro);
    if (ativa) desenhar();
  }).observe(capa);
}
