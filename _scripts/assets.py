"""Assets de Ambos & Asociados a partir del material real (logo PNG 2048 de la web Wix + fotos del estudio).
Uso: python _scripts/assets.py <carpeta con las fotos originales de Wix>"""
import sys, os
from PIL import Image, ImageOps
D = os.path.join(os.path.dirname(__file__), '..')
SRC = sys.argv[1]
CREMA, VINO = (239, 228, 214), (95, 34, 37)

logo = Image.open(os.path.join(D, 'logo-original.png')).convert('RGBA')
logo = logo.crop(logo.getbbox())
A = logo.getchannel('A')
def tinte(col, a):
    im = Image.new('RGBA', a.size, col + (255,)); im.putalpha(a); return im
tinte(VINO, A).save(os.path.join(D, 'img/logo.png'), optimize=True)
tinte(CREMA, A).save(os.path.join(D, 'img/logo-crema.png'), optimize=True)   # monocolor: la variante clara es el mismo dibujo en crema
W, H = logo.size
# ramas de laurel (izquierda y derecha) para enmarcar el H1 del hero
from PIL import ImageDraw
sin_letras = A.copy(); dr = ImageDraw.Draw(sin_letras)
dr.rectangle((int(W * .26), int(H * .12), int(W * .74), int(H * .735)), fill=0)  # balanza (triángulo y cruz)
dr.rectangle((int(W * .18), int(H * .30), int(W * .82), int(H * .735)), fill=0)  # las dos «A»
izq = sin_letras.crop((0, 0, W // 2, H)); der = sin_letras.crop((W // 2, 0, W, H))
for n, a in (('laurel-izq', izq), ('laurel-der', der)):
    a = a.crop(a.getbbox()); tinte(CREMA, a).save(os.path.join(D, f'img/{n}.png'), optimize=True)
# monograma (balanza + AA) sin laureles
mono = A.crop((int(W * .27), 0, int(W * .73), H)); mono = mono.crop(mono.getbbox())
tinte(CREMA, mono).save(os.path.join(D, 'img/monograma-crema.png'), optimize=True)

FOTOS = {'oficina.jpg': '497c49_b1cebaa14331471482eac71f3d04716f_mv2_d_3264_2448_s_4_2.jpg',
         'biblioteca.jpg': '497c49_8fe1f81ea8384de580a674fba9a43248_mv2_d_4008_2770_s_4_2.jpg',
         'sala-reuniones.jpg': '497c49_712ef24e51ef434c8cd028e3111c5ad6_mv2.jpg',
         'sala-espera.jpg': '497c49_7675a0807309409eadd024720b0223ec_mv2.jpg',
         'edificio.jpg': '497c49_90555217273d427199a93b3c94980a8b_mv2.jpg',
         'pasillo.jpg': '497c49_0a7e7e04e8bb48528aa905c6f87838fa_mv2.jpg',
         'calle.jpg': '497c49_677c2d42dbd440e789e7adc818c3d1a3_mv2.jpg'}
for dst, src in FOTOS.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, src))).convert('RGB')
    im.thumbnail((2000, 2000), Image.LANCZOS)
    im.save(os.path.join(D, 'img', dst), quality=80, optimize=True, progressive=True)
for f in sorted(os.listdir(os.path.join(D, 'img'))):
    p = os.path.join(D, 'img', f); print(f, os.path.getsize(p) // 1024, 'KB', Image.open(p).size)
