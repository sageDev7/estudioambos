"""Páginas internas de Ambos & Asociados: estudio.html y areas.html (con anclas por área).
Toma del index el <head>, el header/menú y el footer y arma cada página con el contenido como datos.
Textos: los de estudioambos.com, sin agregar datos. Idempotente: volver a correrlo si cambia el index.
Uso: python _scripts/generar_paginas.py"""
import re
from pathlib import Path

D = Path(__file__).resolve().parent.parent
idx = (D / "index.html").read_text(encoding="utf8")

head_tpl = idx[:idx.index("<title>")]
links_head = idx[idx.index('<link rel="preconnect"'):idx.index("</head>")]
links_head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", links_head, flags=re.S)
top = idx[idx.index("<!-- ============ HEADER ============ -->"):idx.index("<main>")]
f0 = idx.index("<!-- ============ FOOTER ============ -->")
foot = idx[f0:idx.index('<a class="wa-float', f0)]
cola = idx[idx.index('<a class="wa-float', f0):idx.index('<script src="./main.js')]
cola = re.sub(r'<div class="modal".*?</div>\s*</div>\s*', "", cola, flags=re.S)  # sin formulario: sin modal
JS_TAG = re.search(r'<script src="\./main\.js[^"]*"></script>', idx).group(0)

def interna(s):
    s = re.sub(r'href="#(?!")', 'href="./index.html#', s)
    return s.replace('href="./index.html#inicio"', 'href="./index.html"')
top, foot = interna(top), interna(foot)

def page(name, title, desc, body):
    html = (head_tpl + f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            + '<link rel="icon" type="image/png" href="./favicon.png">\n<link rel="apple-touch-icon" href="./favicon.png">\n'
            + links_head + "</head>\n<body>\n\n" + top + "<main>\n" + body + "\n\n</main>\n\n" + foot + cola + JS_TAG + "\n</body>\n</html>\n")
    (D / name).write_text(html, encoding="utf8", newline="\n"); print("ok", name)

def cabecera(foto, ruta, h1, intro):
    return f'''
<!-- ============ CABECERA DE PÁGINA (foto + ruta) ============ -->
<section class="ph">
  <div class="ph-bg" style="background-image:url(img/{foto})" aria-hidden="true"></div>
  <div class="wrap ph-in">
    <nav class="ruta rise" aria-label="Ruta"><a href="./index.html">Inicio</a><i class="ti ti-chevron-right" aria-hidden="true"></i><span>{ruta}</span></nav>
    <h1 class="ph-h1 rise d1">{h1}</h1>
    <p class="ph-lead rise d2">{intro}</p>
  </div>
</section>'''

CTA = '''
<!-- ============ CTA claro (no pega oscuro con el footer oscuro) ============ -->
<section class="cta-c">
  <div class="wrap cta-c-in reveal">
    <img src="./img/logo.png" alt="" width="900" height="651" aria-hidden="true">
    <div>
      <h2>Contanos tu consulta.</h2>
      <p>Te respondemos a la brevedad. Todas las consultas son confidenciales.</p>
    </div>
    <div class="cta-c-btns">
      <a class="btn btn-vino js-wa" href="#" data-msg="{wa}">Consultar por WhatsApp</a>
      <a class="btn btn-vino-line" href="./index.html#contacto">Completar el formulario</a>
    </div>
  </div>
</section>'''

# ---------- áreas (ítems literales de la web actual) ----------
AREAS = [
    ("civil", "I", "Civil y Comercial", "sala-reuniones.jpg",
     "Contratos, bienes, sucesiones y reclamos de salud y riesgos del trabajo.",
     ["Contratos: asesoramiento y elaboración de compraventas, locaciones, fianzas y créditos",
      "Desalojos y recupero de bienes", "Juicios de escrituración y usucapión",
      "Sucesiones, testamentos y planificación patrimonial", "Amparos de salud contra prepagas y obras sociales",
      "Reclamos contra Aseguradoras de Riesgos del Trabajo (ART)"],
     "Hola, quisiera hacer una consulta de derecho civil y comercial."),
    ("danos", "II", "Daños y Perjuicios", "calle.jpg",
     "Reclamos por responsabilidad contractual y extracontractual, de empresas, del Estado y de profesionales.",
     ["Responsabilidad contractual y extracontractual", "Responsabilidad de empresas y del Estado",
      "Responsabilidad profesional y mala praxis", "Accidentes y siniestros en general"],
     "Hola, quisiera hacer una consulta por daños y perjuicios."),
    ("familia", "III", "Derecho de Familia", "sala-espera.jpg",
     "Acompañamiento en los procesos que involucran a la familia y a los hijos.",
     ["Divorcios y uniones convivenciales", "Alimentos", "Cuidado personal y planes de parentalidad",
      "Régimen de comunicación con hijos, abuelos, tíos y otros familiares",
      "Filiación: acciones de reclamación e impugnación", "Adopción",
      "Responsabilidad parental: extinción, privación, suspensión y rehabilitación"],
     "Hola, quisiera hacer una consulta de derecho de familia."),
    ("consumidor", "IV", "Derecho del Consumidor", "oficina.jpg",
     "Representación de consumidores y de empresas, en sede administrativa y judicial.",
     ["Representación de consumidores y de empresas", "Reclamos en sede administrativa y judicial",
      "Reclamos por prácticas abusivas de bancos, aseguradoras y entidades de crédito",
      "Asesoramiento preventivo a empresas",
      "Defensa de terminales automotrices y de sus sociedades de planes de ahorro y compañías financieras"],
     "Hola, quisiera hacer una consulta de derecho del consumidor."),
]
indice = "".join(f'<a href="#{k}"><span>{n}</span>{t}</a>' for k, n, t, *_ in AREAS)
bloques = ""
for i, (k, n, t, foto, intro, items, wa) in enumerate(AREAS):
    lis = "".join(f"<li>{x}</li>" for x in items)
    bloques += f'''
<section class="sec {'sec-2' if i % 2 == 0 else 'sec-3'} area-b" id="{k}">
  <div class="wrap area-b-grid{' area-b-inv' if i % 2 else ''}">
    <figure class="area-b-foto reveal"><img src="./img/{foto}" alt="" width="2000" height="1500" loading="lazy"></figure>
    <div class="area-b-txt reveal">
      <span class="area-b-n">{n}</span>
      <h2 class="h2">{t}</h2>
      <p class="lead">{intro}</p>
      <ul class="area-b-lista">{lis}</ul>
      <a class="btn btn-vino js-wa" href="#" data-msg="{wa}">Consultar por WhatsApp</a>
    </div>
  </div>
</section>'''
body = cabecera("biblioteca.jpg", "Áreas de práctica", "Asesoramiento y representación <em>en cuatro áreas.</em>",
                "Para personas y empresas, en sede administrativa y judicial, ante todos los fueros del Departamento Judicial de Mar del Plata.") + f'''

<nav class="indice" aria-label="Áreas"><div class="wrap indice-in">{indice}</div></nav>
{bloques}
''' + CTA.format(wa="Hola, quisiera hacer una consulta.")
page("areas.html", "Áreas de práctica | Estudio Jurídico Ambos & Asociados",
     "Derecho civil y comercial, daños y perjuicios, familia y consumidor en Mar del Plata. Estudio Jurídico Ambos & Asociados, Av. Luro 2681.", body)

# ---------- el estudio ----------
ABOG = [("LEA", "Luis Ernesto Ambos", "Fundador · Civil y Comercial", "luisambos@gmail.com"),
        ("JPA", "Juan Pablo Ambos", "Civil y Comercial", "juanambos@gmail.com"),
        ("MPB", "María Paz Ballarino", "Derecho de Familia", "pazballarino@gmail.com")]
cards = "".join(f'''
      <article class="abogado reveal">
        <span class="abogado-ini" aria-hidden="true">{ini}</span>
        <h3>{n}</h3>
        <p class="abogado-rol">{r}</p>
        <a href="mailto:{m}"><i class="ti ti-mail" aria-hidden="true"></i>{m}</a>
      </article>''' for ini, n, r, m in ABOG)
GAL = [("sala-reuniones.jpg", "Sala de reuniones"), ("oficina.jpg", "Despacho"), ("biblioteca.jpg", "Biblioteca"),
       ("sala-espera.jpg", "Sala de espera"), ("edificio.jpg", "Av. Luro 2681")]
gal = "".join(f'<figure class="g-{i}"><img src="./img/{f}" alt="{t} del estudio" loading="lazy"><figcaption>{t}</figcaption></figure>' for i, (f, t) in enumerate(GAL))
body = cabecera("pasillo.jpg", "El estudio", "Cuatro décadas <em>en Mar del Plata.</em>",
                "Un estudio fundado por el Dr. Luis Ernesto Ambos, con actuación ante todos los fueros del Departamento Judicial.") + f'''

<!-- ============ HISTORIA ============ -->
<section class="sec sec-2 historia">
  <div class="wrap historia-grid">
    <div class="historia-txt reveal">
      <p class="eyebrow">Trayectoria</p>
      <h2 class="h2">Más de cuarenta años <em>de ejercicio profesional.</em></h2>
      <p>Fundado por el Dr. Luis Ernesto Ambos, el estudio cuenta con más de cuarenta años de ejercicio profesional en Mar del Plata, con actuación ante todos los fueros del Departamento Judicial.</p>
      <p>Cada asunto es atendido directamente por los abogados del estudio, desde la consulta inicial hasta su resolución.</p>
      <p>Representamos a empresas nacionales e internacionales y trabajamos junto a reconocidos estudios jurídicos de la Ciudad de Buenos Aires en los asuntos que tramitan en la región.</p>
    </div>
    <ul class="principios reveal">
      <li><i class="ti ti-user-check" aria-hidden="true"></i><div><b>Atención directa</b><span>Los abogados del estudio llevan cada caso, de la consulta a la resolución.</span></div></li>
      <li><i class="ti ti-shield-check" aria-hidden="true"></i><div><b>Compromiso</b><span>Defendemos los intereses de nuestros clientes, cuidando su patrimonio y sus negocios.</span></div></li>
      <li><i class="ti ti-lock" aria-hidden="true"></i><div><b>Confidencialidad</b><span>Un valor fundamental, en el asesoramiento y en la actuación profesional.</span></div></li>
    </ul>
  </div>
</section>

<!-- ============ EL ESTUDIO POR DENTRO (fotos reales) ============ -->
<section class="sec sec-3 galeria-sec">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow eyebrow-c">Av. Luro 2681, 3° B</p>
      <h2 class="h2">El estudio <em>por dentro.</em></h2>
    </div>
    <div class="galeria reveal">{gal}</div>
  </div>
</section>

<!-- ============ ABOGADOS ============ -->
<section class="sec sec-2" id="abogados">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow eyebrow-c">Abogados</p>
      <h2 class="h2">El equipo <em>del estudio.</em></h2>
    </div>
    <div class="equipo">{cards}
    </div>
  </div>
</section>
''' + CTA.format(wa="Hola, quisiera hacer una consulta.")
page("estudio.html", "El estudio y sus abogados | Estudio Jurídico Ambos & Asociados",
     "Más de cuarenta años en Mar del Plata. Fundado por el Dr. Luis Ernesto Ambos; abogados Juan Pablo Ambos y María Paz Ballarino. Av. Luro 2681.", body)

# ---------- CSS de las páginas internas (una sola vez) ----------
css_p = D / "styles.css"; c = css_p.read_text(encoding="utf8")
if "/* ---------- páginas internas" not in c:
    c += '''
/* ---------- páginas internas (generar_paginas.py) ---------- */
.ph{position:relative;min-height:clamp(440px,62vh,620px);display:flex;align-items:flex-end;overflow:hidden;background:var(--bg)}
.ph-bg{position:absolute;inset:0;background-size:cover;background-position:center;filter:grayscale(.4)}
.ph-bg::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(22,7,9,.72),rgba(22,7,9,.6) 40%,rgba(22,7,9,.96)),linear-gradient(135deg,rgba(95,34,37,.45),transparent 55%)}
.ph-in{position:relative;z-index:1;padding-top:calc(var(--hdr) + 4rem);padding-bottom:4.2rem}
.ruta{display:flex;align-items:center;flex-wrap:wrap;gap:.6rem;margin-bottom:1.5rem;font-size:.72rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
.ruta a:hover{color:var(--arena)}
.ruta i{font-size:.9rem;color:var(--arena)}
.ruta span{color:var(--arena)}
.ph-h1{max-width:50rem;font-size:clamp(2.6rem,5vw,4.2rem);line-height:1.05}
.ph-h1 em{display:block;font-style:italic;color:var(--arena)}
.ph-lead{max-width:40rem;margin-top:1.3rem;font-size:1.1rem;color:var(--text)}
/* índice de áreas, fijo debajo del navbar */
.indice{position:sticky;top:var(--hdr);z-index:30;background:rgba(16,4,5,.94);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.indice-in{display:flex;justify-content:center;gap:2.6rem;overflow-x:auto}
.indice a{display:flex;align-items:center;gap:.6rem;padding:1.15rem 0;white-space:nowrap;font-size:.74rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--text);transition:color .3s}
.indice a span{font-family:var(--f-head);font-style:italic;letter-spacing:0;font-size:1rem;color:var(--arena)}
.indice a:hover{color:var(--arena)}
.area-b{scroll-margin-top:calc(var(--hdr) + 60px)}
.area-b-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:5rem;align-items:center}
.area-b-inv .area-b-foto{order:2}
.area-b-foto{position:relative}
.area-b-foto img{width:100%;aspect-ratio:4/5;object-fit:cover;filter:saturate(.7) contrast(1.05)}
.area-b-foto::after{content:"";position:absolute;inset:14px;border:1px solid rgba(246,236,234,.4);pointer-events:none}
.area-b-n{font-family:var(--f-head);font-style:italic;font-size:1.6rem;color:var(--arena)}
.area-b-txt .h2{margin:.2rem 0 1rem}
.area-b-lista{margin:2rem 0 2.4rem}
.area-b-lista li{position:relative;padding:.85rem 0 .85rem 1.6rem;color:var(--text)}
.area-b-lista li+li{border-top:1px solid var(--line)}
.area-b-lista li::before{content:"";position:absolute;left:0;top:1.55em;width:.8rem;height:1px;background:var(--arena)}
/* historia + principios */
.historia-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:5rem;align-items:center}
.historia-txt .h2{margin-bottom:1.6rem}
.historia-txt p:not(.eyebrow){color:var(--muted)}
.historia-txt p+p{margin-top:1rem}
.principios{padding:.6rem 2.4rem;background:rgba(246,236,234,.03);border:1px solid var(--line);border-top:2px solid var(--vino-2)}
.principios li{display:flex;gap:1.1rem;padding:1.5rem 0}
.principios li+li{border-top:1px solid var(--line)}
.principios i{flex:none;font-size:1.5rem;color:var(--arena)}
.principios b{display:block;font-family:var(--f-head);font-weight:400;font-size:1.35rem;color:var(--head)}
.principios span{font-size:.94rem;color:var(--muted)}
/* galería de fotos reales */
.galeria{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:220px;gap:1rem}
.galeria figure{position:relative;overflow:hidden}
.galeria img{width:100%;height:100%;object-fit:cover;filter:saturate(.75);transition:transform 1s var(--ease),filter .6s}
.galeria figure:hover img{transform:scale(1.04);filter:saturate(1)}
.galeria figcaption{position:absolute;left:0;right:0;bottom:0;padding:2.4rem 1rem .9rem;background:linear-gradient(180deg,transparent,rgba(22,7,9,.85));font-size:.7rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--crema)}
.galeria .g-0{grid-column:span 2;grid-row:span 2}
/* CTA claro (crema + logo bordó) */
.cta-c{background:var(--crema);color:var(--ink)}
.cta-c-in{display:flex;align-items:center;justify-content:center;gap:3rem;padding-top:4rem;padding-bottom:4rem}
.cta-c-in img{width:110px;flex:none}
.cta-c h2{font-size:clamp(2rem,3.4vw,2.8rem);color:var(--vino)}
.cta-c p{margin-top:.4rem;color:#5b4446}
.cta-c-btns{display:grid;gap:.8rem}
.cta-c-btns .btn{width:100%}
.btn-vino-line{border-color:var(--vino);color:var(--vino)}
.btn-vino-line:hover{background:var(--vino);color:var(--crema)}
.cta-c .btn-vino:hover{border-color:var(--vino);color:var(--vino)}
@media (max-width:1024px){
  .area-b-grid,.historia-grid{grid-template-columns:1fr;gap:3rem}
  .area-b-inv .area-b-foto{order:0}
  .area-b-foto{max-width:520px}
  .area-b-foto img{aspect-ratio:16/10}
  .galeria{grid-template-columns:repeat(2,1fr);grid-auto-rows:200px}
  .galeria .g-0{grid-column:span 2;grid-row:span 1}
  .galeria .g-4{grid-column:span 2}
  .cta-c-in{flex-direction:column;gap:1.6rem;text-align:center}
  .indice-in{justify-content:flex-start;gap:2rem}
}
@media (max-width:768px){
  .ph{min-height:auto}
  .ph-in{padding-top:calc(var(--hdr) + 3rem);padding-bottom:3.2rem;text-align:center}
  .ruta{justify-content:center}
  .ph-h1{font-size:clamp(2.1rem,9vw,2.8rem)}
  .ph-lead{margin-left:auto;margin-right:auto;font-size:1rem}
  .indice{display:none}
  .area-b-foto{max-width:none}
  .area-b-txt,.historia-txt{display:flex;flex-direction:column;align-items:center;text-align:center}
  .area-b-lista{width:100%}
  .area-b-lista li{padding-left:0}
  .area-b-lista li::before{display:none}
  .area-b-txt .btn{width:100%;max-width:300px}
  .principios{padding:.4rem 1.3rem}
  .principios li{flex-direction:column;align-items:center;gap:.4rem;text-align:center}
  .galeria{grid-template-columns:1fr;grid-auto-rows:220px}
  .galeria .g-0,.galeria .g-1,.galeria .g-4{grid-column:auto}
  .cta-c-btns{width:100%;justify-items:center}
  .cta-c-btns .btn{max-width:300px}
}
'''
    css_p.write_text(c, encoding="utf8"); print("css ok")
