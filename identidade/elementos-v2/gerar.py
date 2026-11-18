# Elementos v2 — estrelas com brilho, ícones místicos e peças de colagem vintage.
# Gera um SVG por elemento (com textura de folha de ouro e brilho) em svg/<versão>/.
import math, random, os

HERE = os.path.dirname(os.path.abspath(__file__))
VERDE, ROXO, PERG, PETRO = '#11281A', '#3B2340', '#D6C2AA', '#2E4F4A'
GOLDS = {'metalico': ('#9E7B3E', '#CDAE6E', '#B8924F'), 'velho': ('#6E5523', '#A68844', '#85692B')}

def f(v): return f'{v:.2f}'.rstrip('0').rstrip('.')
def pt(x, y): return f'{f(x)} {f(y)}'
def poly(pts, close=True): return 'M' + ' L'.join(pt(*p) for p in pts) + ('Z' if close else '')
def pol(cx, cy, r, a): return cx + r*math.cos(a), cy + r*math.sin(a)

G = 'fill="url(#ouro)"'           # preenchimento dourado
GS = 'fill="none" stroke="url(#ouro)" stroke-linecap="round" stroke-linejoin="round"'

# ---------------- formas básicas ----------------
def ray(cx, cy, a, L, w, r0=0):
    """raio fino em forma de losango alongado, do centro para fora."""
    a = math.radians(a); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    b = (cx + dx*r0, cy + dy*r0); m = (cx + dx*(r0 + L*.12), cy + dy*(r0 + L*.12))
    tip = (cx + dx*(r0 + L), cy + dy*(r0 + L))
    return f'<path {G} d="{poly([b, (m[0]+nx*w, m[1]+ny*w), tip, (m[0]-nx*w, m[1]-ny*w)])}"/>'

def sparkle(cx, cy, r, thin=.13):
    t = r*thin
    return (f'<path {G} d="M{pt(cx, cy-r)}Q{pt(cx+t, cy-t)} {pt(cx+r, cy)}Q{pt(cx+t, cy+t)} {pt(cx, cy+r)}'
            f'Q{pt(cx-t, cy+t)} {pt(cx-r, cy)}Q{pt(cx-t, cy-t)} {pt(cx, cy-r)}Z"/>')

def dot(cx, cy, r, fill='url(#ouro)'):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}"/>'

def ring(cx, cy, r, sw=1.4, dash=None, stroke='url(#ouro)'):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{d}/>'

def crescent(cx, cy, r, k=.78, rot=0, fill='url(#ouro)'):
    """lua crescente: círculo menos círculo deslocado."""
    r2 = r*k; off = r*.42
    a = math.radians(rot)
    ox, oy = off*math.cos(a), off*math.sin(a)
    # interseções aproximadas via arcos
    return (f'<path fill="{fill}" fill-rule="evenodd" d="M{pt(cx-r, cy)}a{f(r)} {f(r)} 0 1 0 {f(2*r)} 0a{f(r)} {f(r)} 0 1 0 {f(-2*r)} 0Z'
            f'M{pt(cx+ox-r2, cy+oy)}a{f(r2)} {f(r2)} 0 1 0 {f(2*r2)} 0a{f(r2)} {f(r2)} 0 1 0 {f(-2*r2)} 0Z" '
            f'clip-path="url(#cl{abs(hash((cx, cy, r))) % 10**6})"/>'
            f'<clipPath id="cl{abs(hash((cx, cy, r))) % 10**6}"><circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}"/></clipPath>')

def faceted(cx, cy, R, r, n=8, rot=-90, light='#DCC08A', dark='#8E6E36'):
    out = ''
    for i in range(n):
        a = math.radians(rot + 360/n*i); a1 = math.radians(rot + 360/n*(i - .5)); a2 = math.radians(rot + 360/n*(i + .5))
        tip = pol(cx, cy, R, a); v1 = pol(cx, cy, r, a1); v2 = pol(cx, cy, r, a2)
        out += f'<path fill="{light}" d="{poly([(cx, cy), v1, tip])}"/><path fill="{dark}" d="{poly([(cx, cy), tip, v2])}"/>'
    return out

def leaf(x, y, ang, L, W, fill, bend=0.0):
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    tip = (x + dx*L + nx*bend*L, y + dy*L + ny*bend*L)
    c1 = (x + dx*.3*L + nx*W, y + dy*.3*L + ny*W); c2 = (x + dx*.78*L + nx*W*.6, y + dy*.78*L + ny*W*.6)
    c3 = (x + dx*.78*L - nx*W*.6, y + dy*.78*L - ny*W*.6); c4 = (x + dx*.3*L - nx*W, y + dy*.3*L - ny*W)
    return f'<path fill="{fill}" d="M{pt(x, y)}C{pt(*c1)} {pt(*c2)} {pt(*tip)}C{pt(*c3)} {pt(*c4)} {pt(x, y)}Z"/>'

def bez(p, t):
    u = 1 - t
    return (u**3*p[0][0] + 3*u*u*t*p[1][0] + 3*u*t*t*p[2][0] + t**3*p[3][0],
            u**3*p[0][1] + 3*u*u*t*p[1][1] + 3*u*t*t*p[2][1] + t**3*p[3][1])

def bez_ang(p, t):
    a, b = bez(p, max(t - .01, 0)), bez(p, min(t + .01, 1))
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))

def fern(p, n, Lmax, fill, sw=1.2, Wr=.24, spread=62):
    out = f'<path fill="none" stroke="{fill}" stroke-width="{sw}" stroke-linecap="round" d="M{pt(*p[0])}C{pt(*p[1])} {pt(*p[2])} {pt(*p[3])}"/>'
    for i in range(n):
        t = .05 + .92*i/(n - 1); x, y = bez(p, t); a = bez_ang(p, t)
        L = Lmax*(1 - t)**.75 + Lmax*.12
        for s in (1, -1): out += leaf(x, y, a + s*spread, L, L*Wr, fill, bend=-.07*s)
    x, y = p[3]; out += leaf(x, y, bez_ang(p, 1), Lmax*.22, Lmax*.06, fill)
    return out

def sprig(p, n, L, fill, sw=1.1, Wr=.42, spread=48):
    out = f'<path fill="none" stroke="{fill}" stroke-width="{sw}" stroke-linecap="round" d="M{pt(*p[0])}C{pt(*p[1])} {pt(*p[2])} {pt(*p[3])}"/>'
    for i in range(n):
        t = .15 + .8*i/max(n - 1, 1); x, y = bez(p, t); a = bez_ang(p, t)
        out += leaf(x, y, a + (spread if i % 2 else -spread), L*(1 - t*.4), L*(1 - t*.4)*Wr, fill)
    x, y = p[3]; out += leaf(x, y, bez_ang(p, 1), L*.7, L*.7*Wr, fill)
    return out

def flower(cx, cy, r, fill, center='url(#ouro)'):
    out = ''.join(leaf(cx, cy, k*72 - 90, r, r*.5, fill) for k in range(5))
    return out + dot(cx, cy, r*.22, center)

def spiral(cx, cy, r, turns=1.6, a0=0, cw=1):
    pts = []
    for i in range(60):
        t = i/59; rr = r*(1 - t*.92); a = a0 + cw*t*turns*2*math.pi
        pts.append(pol(cx, cy, rr, a))
    return 'M' + ' L'.join(pt(*q) for q in pts)

# ---------------- registro ----------------
E = []
def el(key, nome, desc, vb, cat, bg, gold='metalico', glow=0, foil=True, paper=False):
    def deco(fn):
        E.append(dict(key=key, nome=nome, desc=desc, vb=vb, cat=cat, bg=bg, gold=gold, glow=glow, foil=foil, paper=paper, fn=fn)); return fn
    return deco

# ================= ESTRELAS COM BRILHO =================
@el('brilho', 'Brilho', 'Estrela de quatro pontas longas, com brilho suave.', (200, 200), 'estrelas', ROXO, glow=5)
def _():
    out = ''.join(ray(100, 100, a, L, 4.2) for a, L in [(-90, 88), (90, 88), (0, 70), (180, 70)])
    out += ''.join(ray(100, 100, a, 26, 2) for a in (45, 135, 225, 315))
    rnd = random.Random(2)
    for _ in range(9): out += dot(rnd.uniform(30, 170), rnd.uniform(30, 170), rnd.uniform(.8, 2))
    return out

@el('explosao', 'Explosão estelar', 'Raios finos de tamanhos diferentes, como luz que se abre.', (200, 200), 'estrelas', VERDE, glow=4)
def _():
    rnd = random.Random(4); out = ''
    for k in range(32):
        a = k*11.25; L = (84 if k % 8 == 0 else 62 if k % 4 == 0 else rnd.uniform(30, 52))
        out += ray(100, 100, a, L, 2.2 if k % 4 == 0 else 1.2)
    out += dot(100, 100, 5)
    for _ in range(14): out += dot(100 + rnd.uniform(-85, 85), 100 + rnd.uniform(-85, 85), rnd.uniform(.6, 1.6))
    return out

@el('radiante', 'Radiante', 'Sol de luz com centro luminoso.', (200, 200), 'estrelas', PETRO, glow=7)
def _():
    out = '<circle cx="100" cy="100" r="46" fill="url(#luz)"/>'
    for k in range(48):
        a = k*7.5; L = 88 if k % 6 == 0 else (66 if k % 2 == 0 else 48)
        out += ray(100, 100, a, L, 1.6 if k % 6 == 0 else .9, r0=6)
    return out

@el('nautica', 'Estrela náutica', 'Oito pontas facetadas dentro de um anel pontilhado.', (200, 200), 'estrelas', ROXO, glow=3)
def _():
    out = ring(100, 100, 74, .9) + ring(100, 100, 80, 1.6, dash='0.1 6')
    out += faceted(100, 100, 50, 14, n=4, rot=-45)
    out += faceted(100, 100, 92, 16, n=4, rot=-90)
    return out

@el('constelacao-brilhos', 'Chuva de brilhos', 'Brilhos de vários tamanhos para espalhar no fundo.', (200, 200), 'estrelas', VERDE, glow=4)
def _():
    out = ''
    for x, y, r in [(70, 64, 34), (132, 104, 24), (88, 140, 18), (150, 48, 12), (40, 120, 9), (160, 160, 10), (118, 30, 7)]:
        out += sparkle(x, y, r)
    rnd = random.Random(8)
    for _ in range(22): out += dot(rnd.uniform(15, 185), rnd.uniform(15, 185), rnd.uniform(.6, 1.5))
    return out

@el('celeste', 'Lua e brilho', 'Crescente atravessada por um brilho longo.', (200, 200), 'estrelas', PETRO, glow=5)
def _():
    out = crescent(86, 100, 46, k=.82, rot=0)
    out += ''.join(ray(122, 100, a, L, 3.2) for a, L in [(-90, 84), (90, 84), (0, 58), (180, 58)])
    rnd = random.Random(9)
    for _ in range(10): out += dot(rnd.uniform(30, 180), rnd.uniform(25, 175), rnd.uniform(.7, 1.7))
    return out

@el('poeira-estrela', 'Estrela de poeira', 'Estrela formada por pontinhos de luz.', (200, 200), 'estrelas', ROXO, glow=3)
def _():
    P = [pol(100, 106, (86 if i % 2 == 0 else 36), math.radians(-90 + 36*i)) for i in range(10)]
    def inside(x, y):
        c = False; j = len(P) - 1
        for i in range(len(P)):
            xi, yi = P[i]; xj, yj = P[j]
            if (yi > y) != (yj > y) and x < (xj - xi)*(y - yi)/(yj - yi) + xi: c = not c
            j = i
        return c
    rnd = random.Random(12); out = ''; n = 0
    while n < 520:
        x, y = rnd.uniform(10, 190), rnd.uniform(10, 195)
        if inside(x, y):
            d = math.hypot(x - 100, y - 106)
            if rnd.random() < 1.15 - d/90:
                out += dot(x, y, rnd.uniform(.5, 1.9)); n += 1
    out += sparkle(100, 104, 14)
    return out

@el('galaxia', 'Redemoinho galáctico', 'Espiral de poeira estelar com brilhos.', (200, 200), 'estrelas', VERDE, glow=4)
def _():
    rnd = random.Random(5); out = ''
    for arm in (0, math.pi):
        for i in range(90):
            t = i/89; r = 8 + t*82; a = arm + t*3.4
            x, y = pol(100, 100, r, a)
            x += rnd.uniform(-4, 4)*t; y += rnd.uniform(-4, 4)*t
            out += dot(x, y, max(.5, 2.1 - t*1.5) * rnd.uniform(.6, 1.1))
    out += sparkle(100, 100, 20) + sparkle(48, 60, 9) + sparkle(150, 140, 8) + sparkle(160, 52, 6)
    return out

@el('vintage', 'Estrela vintage', 'Raios principais longos e secundários curtos, estilo gravura.', (200, 200), 'estrelas', PETRO, glow=3)
def _():
    out = faceted(100, 100, 94, 10, n=4, rot=-90)
    out += faceted(100, 100, 50, 7, n=4, rot=-45)
    out += ''.join(ray(100, 100, a, 34, 1.4) for a in range(0, 360, 15) if a % 45)
    return out

# ================= ÍCONES MÍSTICOS =================
@el('lua-orbita', 'Lua em órbita', 'Crescente com anel e pequena estrela.', (200, 200), 'misticos', ROXO, glow=2)
def _():
    out = f'<ellipse cx="100" cy="104" rx="86" ry="20" transform="rotate(-14 100 104)" {GS} stroke-width="1.4"/>'
    out += crescent(100, 100, 52, k=.8, rot=-10)
    out += dot(172, 74, 4) + sparkle(150, 40, 9) + sparkle(42, 160, 6)
    return out

@el('luas-gemeas', 'Luas gêmeas', 'Duas crescentes encaixadas: o consciente e o oculto.', (200, 200), 'misticos', VERDE, glow=2)
def _():
    out = crescent(96, 100, 64, k=.84, rot=0)
    out += crescent(112, 100, 30, k=.8, rot=0)
    out += dot(150, 100, 3) + sparkle(160, 50, 8)
    return out

@el('olho-raios', 'Olho radiante', 'Olho com íris de lua e raios ao redor.', (200, 200), 'misticos', PETRO, glow=2)
def _():
    out = f'<path {GS} stroke-width="2.2" d="M20 100C55 52 145 52 180 100C145 148 55 148 20 100Z"/>'
    out += f'<path {GS} stroke-width="1" d="M34 100C64 64 136 64 166 100C136 136 64 136 34 100Z"/>'
    out += ring(100, 100, 26, 1.6) + dot(100, 100, 17)
    out += crescent(100, 100, 12, k=.8, fill=PETRO)
    for k in range(-5, 6):
        a = math.radians(-90 + k*15); L = 22 if k % 2 == 0 else 12
        x0, y0 = pol(100, 100, 52, a); x1, y1 = pol(100, 100, 52 + L, a)
        out += f'<path {GS} stroke-width="1.6" d="M{pt(x0, y0)}L{pt(x1, y1)}"/>'
    for k in range(-4, 5):
        x = 100 + k*13; y = 140 - abs(k)*2.6
        out += f'<path {GS} stroke-width="1.2" d="M{pt(x, y)}L{pt(x, y+9)}"/>' + dot(x, y + 12, 1.6)
    return out

@el('sol-lua-v2', 'Sol com lua', 'Disco solar com raios e lua no centro.', (200, 200), 'misticos', ROXO, glow=3)
def _():
    out = ring(100, 100, 40, 2) + crescent(100, 100, 30, k=.8, rot=0)
    for k in range(16):
        a = k*22.5
        out += ray(100, 100, a, 40 if k % 2 == 0 else 24, 7 if k % 2 == 0 else 5, r0=46)
    for k in range(16):
        x, y = pol(100, 100, 94, math.radians(k*22.5 + 11.25)); out += dot(x, y, 1.6)
    return out

@el('pendulo', 'Pêndulo lunar', 'Talismã pendente com lua, gotas e pontos.', (160, 260), 'misticos', VERDE, glow=2)
def _():
    out = dot(80, 10, 4)
    out += f'<path {GS} stroke-width="1.3" stroke-dasharray="0.1 6" d="M80 18L80 70"/>'
    out += f'<path {G} d="M80 72L88 84L80 96L72 84Z"/>'
    out += f'<path {GS} stroke-width="1.3" d="M80 96L80 118"/>'
    out += f'<path {G} d="M48 122A32 32 0 0 0 112 122A26 26 0 0 1 48 122Z"/>' + dot(80, 128, 5)
    out += f'<path {GS} stroke-width="1.3" d="M80 160L80 196"/>'
    out += f'<path {G} d="M80 196C88 210 92 218 92 226A12 12 0 0 1 68 226C68 218 72 210 80 196Z"/>'
    for s in (-1, 1):
        x = 80 + s*30
        out += f'<path {GS} stroke-width="1.1" d="M{f(80+s*18)} 140Q{f(x)} 150 {f(x)} 180"/>' + dot(x, 184, 3) + dot(x, 194, 2)
    return out

@el('nuvem', 'Nuvem ornamental', 'Nuvem de espirais, delicada e mística.', (260, 130), 'misticos', ROXO, glow=2, foil=True)
def _():
    out = (f'<path {GS} stroke-width="1.8" d="M10 96C40 96 50 92 60 88'
           'C46 70 62 48 84 58C88 34 120 26 136 46C150 26 186 32 186 60C204 54 222 70 210 88'
           'C222 92 238 94 252 96C230 100 214 104 196 104L70 104C52 104 32 100 10 96Z"/>')
    for (cx, cy, r, a0, cw) in [(86, 76, 16, 3.6, 1), (132, 66, 20, 3.4, -1), (176, 76, 16, 4.2, 1), (110, 90, 10, 2, -1), (158, 92, 9, 2.6, 1)]:
        out += f'<path {GS} stroke-width="1.3" d="{spiral(cx, cy, r, 1.4, a0, cw)}"/>'
    out += f'<path {GS} stroke-width="1.1" d="M74 104C100 112 170 112 196 104"/>'
    return out

@el('arco-raios', 'Aurora', 'Meio sol de raios finos, como amanhecer.', (240, 140), 'misticos', PETRO, glow=2)
def _():
    out = f'<path {GS} stroke-width="1.6" d="M30 120L210 120"/>' + f'<path {GS} stroke-width="1.4" d="M84 120A36 36 0 0 1 156 120"/>'
    for k in range(0, 37):
        a = math.radians(180 + k*5); L = 40 if k % 3 == 0 else 26
        x0, y0 = pol(120, 120, 46, a); x1, y1 = pol(120, 120, 46 + L, a)
        out += f'<path {GS} stroke-width="{1.5 if k % 3 == 0 else .9}" d="M{pt(x0, y0)}L{pt(x1, y1)}"/>'
    out += sparkle(120, 98, 9)
    return out

@el('leque', 'Leque art déco', 'Raios em leque com pontas de gota.', (200, 200), 'misticos', VERDE, glow=2)
def _():
    out = f'<path {G} d="M80 186L120 186L112 176L88 176Z"/>'
    for k in range(-3, 4):
        a = math.radians(-90 + k*13); L = 150 - abs(k)*16
        x1, y1 = pol(100, 180, L, a)
        out += f'<path {GS} stroke-width="{2.6 if k == 0 else 1.6}" d="M100 180L{pt(x1, y1)}"/>'
        out += f'<path {G} d="M{pt(x1, y1-14)}C{pt(x1+5, y1-6)} {pt(x1+5, y1)} {pt(x1, y1+2)}C{pt(x1-5, y1)} {pt(x1-5, y1-6)} {pt(x1, y1-14)}Z" transform="rotate({k*13} {f(x1)} {f(y1)})"/>'
    out += f'<path {GS} stroke-width="1.2" d="M40 150A70 70 0 0 1 160 150"/>'
    return out

@el('talisma', 'Talismã vertical', 'Ornamento de linha com losango, lua e pontos.', (120, 260), 'misticos', ROXO, glow=2)
def _():
    out = f'<path {GS} stroke-width="1.4" d="M60 8L60 92M60 150L60 228"/>'
    out += f'<path {G} d="M60 92L76 120L60 148L44 120Z"/>' + f'<path fill="{ROXO}" d="M60 104L68 120L60 136L52 120Z"/>'
    out += dot(60, 120, 3)
    for y in (40, 56, 72): out += f'<path {GS} stroke-width="1.3" d="M{60-(80-y)*.3} {y}L60 {y-6}L{60+(80-y)*.3} {y}"/>'
    out += crescent(60, 182, 16, k=.82, rot=-90) + dot(60, 238, 4) + dot(60, 250, 2.2)
    for y in (166, 200): out += dot(44, y, 1.8) + dot(76, y, 1.8)
    return out

# ================= COLAGEM VINTAGE =================
def seal_shape(cx, cy, r, seed):
    rnd = random.Random(seed); ph = [rnd.uniform(0, 6.3) for _ in range(4)]
    pts = []
    for i in range(72):
        a = 2*math.pi*i/72
        rr = r*(1 + .035*math.sin(3*a + ph[0]) + .025*math.sin(7*a + ph[1]) + .015*math.sin(13*a + ph[2]))
        pts.append(pol(cx, cy, rr, a))
    return poly(pts)

def wax(cx, cy, r, base, light, dark, seed):
    gid = f'w{seed}'
    out = (f'<radialGradient id="{gid}" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="{light}"/>'
           f'<stop offset=".55" stop-color="{base}"/><stop offset="1" stop-color="{dark}"/></radialGradient>')
    out += f'<path d="{seal_shape(cx, cy, r, seed)}" fill="url(#{gid})" filter="url(#sombra)"/>'
    out += f'<circle cx="{cx}" cy="{cy}" r="{f(r*.74)}" fill="{dark}" opacity=".35"/>'
    out += f'<circle cx="{cx}" cy="{cy}" r="{f(r*.72)}" fill="url(#{gid})"/>'
    out += f'<circle cx="{cx}" cy="{cy}" r="{f(r*.72)}" fill="none" stroke="{light}" stroke-opacity=".5" stroke-width="1.2"/>'
    return out

def ribbon(cx, top, w, L, color, dark):
    out = ''
    for s in (-1, 1):
        x0 = cx + s*6; x1 = cx + s*(w + 18)
        out += (f'<path fill="{color}" d="M{pt(x0 - s*10, top)}L{pt(x0 + s*w*.6, top)}L{pt(x1, top + L)}L{pt(x1 - s*12, top + L - 14)}'
                f'L{pt(x1 - s*26, top + L + 4)}Z"/>')
        out += f'<path fill="{dark}" opacity=".35" d="M{pt(x0 - s*10, top)}L{pt(x0, top)}L{pt(x1 - s*26, top + L + 4)}L{pt(x1 - s*30, top + L)}Z"/>'
    return out

@el('selo-cera-verde', 'Selo de cera verde', 'Lacre com samambaia dourada e fitas.', (220, 260), 'colagem', PERG, paper=False)
def _():
    out = ribbon(110, 130, 34, 110, '#1C3A27', '#06120A')
    out += wax(110, 110, 92, '#1B3626', '#2F5A40', '#0A1810', 3)
    out += fern([(110, 168), (108, 140), (112, 100), (110, 56)], 15, 30, 'url(#ouro)', sw=1.6)
    return out

@el('selo-cera-roxo', 'Selo de cera roxo', 'Lacre com lua crescente e estrelas.', (220, 220), 'colagem', PERG)
def _():
    out = wax(110, 110, 92, '#43284A', '#6A4472', '#22122A', 7)
    out += crescent(104, 110, 38, k=.8, rot=0)
    out += sparkle(140, 84, 10) + sparkle(150, 128, 6) + sparkle(128, 150, 4)
    out += ring(110, 110, 58, 1, dash='0.1 5')
    return out

def stamp_mask(mid, x0, y0, x1, y1, step=12, r=4.6):
    out = f'<mask id="{mid}"><rect x="{x0-6}" y="{y0-6}" width="{x1-x0+12}" height="{y1-y0+12}" fill="#000"/><rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#fff"/>'
    nx = int((x1 - x0)/step); ny = int((y1 - y0)/step)
    sx = (x1 - x0)/nx; sy = (y1 - y0)/ny
    for i in range(nx + 1):
        out += f'<circle cx="{f(x0+i*sx)}" cy="{y0}" r="{r}" fill="#000"/><circle cx="{f(x0+i*sx)}" cy="{y1}" r="{r}" fill="#000"/>'
    for j in range(ny + 1):
        out += f'<circle cx="{x0}" cy="{f(y0+j*sy)}" r="{r}" fill="#000"/><circle cx="{x1}" cy="{f(y0+j*sy)}" r="{r}" fill="#000"/>'
    return out + '</mask>'

@el('selo-postal-samambaia', 'Selo postal de samambaias', 'Selo serrilhado com samambaias e flores.', (200, 250), 'colagem', ROXO, paper=True)
def _():
    out = stamp_mask('ms1', 12, 12, 188, 238)
    out += f'<g mask="url(#ms1)" filter="url(#sombra)"><rect x="6" y="6" width="188" height="238" fill="#EDE2D2"/>'
    out += f'<rect x="22" y="22" width="156" height="206" fill="{VERDE}"/>'
    out += f'<rect x="28" y="28" width="144" height="194" fill="none" stroke="url(#ouro)" stroke-width="1"/>'
    out += '<g clip-path="url(#cs1)">'
    out += fern([(70, 228), (66, 180), (58, 130), (52, 70)], 14, 30, PERG, sw=1.2)
    out += fern([(120, 228), (124, 170), (136, 120), (150, 64)], 14, 32, '#C4AE92', sw=1.2)
    out += fern([(96, 228), (96, 190), (98, 160), (96, 120)], 10, 22, PERG, sw=1)
    for (x, y) in [(80, 190), (140, 196), (104, 176), (60, 204), (152, 168)]:
        out += f'<path stroke="{PERG}" stroke-width=".8" d="M{x} {y}L{x} 228"/>' + flower(x, y, 7, '#F2E8D8')
    rnd = random.Random(3)
    for _ in range(40): out += dot(rnd.uniform(28, 172), rnd.uniform(214, 222), rnd.uniform(1.5, 3.5), '#2C4A33')
    out += sparkle(150, 46, 7) + sparkle(46, 52, 4)
    out += '</g><clipPath id="cs1"><rect x="28" y="28" width="144" height="194"/></clipPath></g>'
    return out

@el('selo-postal-floresta', 'Selo postal da floresta', 'Pinheiros, lua e céu em pergaminho.', (200, 250), 'colagem', VERDE, gold='velho', paper=True)
def _():
    out = stamp_mask('ms2', 12, 12, 188, 238)
    out += f'<g mask="url(#ms2)" filter="url(#sombra)"><rect x="6" y="6" width="188" height="238" fill="#EDE2D2"/>'
    out += f'<rect x="22" y="22" width="156" height="206" fill="{PERG}"/>'
    out += f'<rect x="28" y="28" width="144" height="194" fill="none" stroke="url(#ouro)" stroke-width="1"/>'
    out += f'<g clip-path="url(#cs2)">'
    out += f'<path fill="#B9A386" d="M28 170L60 120L84 146L118 96L150 150L172 130L172 222L28 222Z"/>'
    rnd = random.Random(6)
    for (x, h) in [(40, 70), (58, 92), (76, 60), (130, 80), (150, 104), (168, 66), (100, 50)]:
        tr = ''
        for k in range(6):
            y = 222 - h + k*h*.15; w = 4 + k*3.4
            tr += f'<path fill="{VERDE}" d="M{pt(x-w, y+h*.18)}L{pt(x, y)}L{pt(x+w, y+h*.18)}Z"/>'
        out += f'<path stroke="{VERDE}" stroke-width="2" d="M{x} 222L{x} {222-h}"/>' + tr
    out += f'<rect x="28" y="214" width="144" height="10" fill="{VERDE}"/>'
    out += crescent(132, 64, 16, k=.8, rot=0) + sparkle(70, 52, 7) + sparkle(98, 72, 4) + sparkle(158, 92, 4)
    out += '</g><clipPath id="cs2"><rect x="28" y="28" width="144" height="194"/></clipPath></g>'
    return out

def tag_path(x0, y0, x1, y1, c):
    return f'M{x0} {y0+c}L{x0+c} {y0}L{x1-c} {y0}L{x1} {y0+c}L{x1} {y1}L{x0} {y1}Z'

@el('etiqueta-verde', 'Etiqueta verde', 'Tag com ilhós dourado, ramos e flores.', (140, 260), 'colagem', PERG)
def _():
    out = f'<mask id="mt1"><rect width="140" height="260" fill="#fff"/><circle cx="70" cy="34" r="8" fill="#000"/></mask>'
    out += f'<g mask="url(#mt1)" filter="url(#sombra)"><path fill="{VERDE}" d="{tag_path(12, 10, 128, 250, 28)}"/>'
    out += f'<path fill="none" stroke="url(#ouro)" stroke-width="1" d="{tag_path(20, 18, 120, 242, 24)}"/></g>'
    out += ring(70, 34, 11, 4.5)
    out += fern([(70, 236), (68, 196), (74, 150), (70, 100)], 12, 22, PERG, sw=1)
    out += sprig([(48, 236), (40, 200), (34, 170), (40, 140)], 6, 11, '#B9A386')
    out += sprig([(92, 236), (100, 210), (104, 186), (100, 160)], 5, 10, '#B9A386')
    for (x, y) in [(42, 196), (98, 182), (58, 214), (86, 220)]: out += flower(x, y, 6, '#F2E8D8')
    out += sparkle(100, 70, 6) + sparkle(36, 92, 4)
    return out

@el('etiqueta-pergaminho', 'Etiqueta pergaminho', 'Tag clara com samambaias em verde.', (140, 260), 'colagem', VERDE, gold='velho')
def _():
    out = f'<mask id="mt2"><rect width="140" height="260" fill="#fff"/><circle cx="70" cy="34" r="8" fill="#000"/></mask>'
    out += f'<g mask="url(#mt2)" filter="url(#sombra)"><path fill="#E6D8C4" d="{tag_path(12, 10, 128, 250, 28)}"/>'
    out += f'<path fill="none" stroke="url(#ouro)" stroke-width="1" d="{tag_path(20, 18, 120, 242, 24)}"/></g>'
    out += ring(70, 34, 11, 4.5)
    out += fern([(62, 238), (60, 190), (52, 140), (46, 86)], 14, 26, VERDE, sw=1.1)
    out += fern([(80, 238), (84, 196), (92, 160), (100, 120)], 11, 20, '#4D6B55', sw=1)
    out += sparkle(96, 72, 6) + sparkle(104, 98, 3.5)
    return out

def torn(pts, amp, seed, step=5):
    rnd = random.Random(seed); out = []
    for (a, b) in zip(pts, pts[1:] + pts[:1]):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(int(L/step), 1)
        nx, ny = -(b[1] - a[1])/L, (b[0] - a[0])/L
        for i in range(n):
            t = i/n; j = rnd.uniform(-amp, amp) + (rnd.uniform(-amp, amp)*1.6 if rnd.random() < .15 else 0)
            out.append((a[0] + (b[0] - a[0])*t + nx*j, a[1] + (b[1] - a[1])*t + ny*j))
    return poly(out)

@el('papel-rasgado', 'Papel rasgado noturno', 'Recorte com céu estrelado, lua e samambaias.', (300, 220), 'colagem', PERG, paper=True)
def _():
    base = [(14, 60), (280, 14), (288, 160), (22, 206)]
    out = f'<path fill="#EFE5D6" d="{torn([(10, 56), (284, 9), (292, 164), (18, 211)], 4, 1, 4)}" filter="url(#sombra)"/>'
    out += f'<clipPath id="cp1"><path d="{torn(base, 3.2, 2, 4)}"/></clipPath>'
    out += '<linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1C12"/><stop offset="1" stop-color="#1D3B28"/></linearGradient>'
    out += '<g clip-path="url(#cp1)"><rect width="300" height="220" fill="url(#ceu)"/>'
    out += crescent(176, 74, 22, k=.82, rot=0)
    for (x, y, r) in [(96, 70, 9), (228, 50, 6), (130, 110, 5), (250, 100, 4), (64, 120, 4)]: out += sparkle(x, y, r)
    rnd = random.Random(4)
    for _ in range(40): out += dot(rnd.uniform(20, 280), rnd.uniform(20, 150), rnd.uniform(.5, 1.3))
    for (cx, cy, r) in [(210, 180, 30), (238, 168, 26), (262, 182, 30), (186, 196, 22), (284, 160, 22)]:
        out += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#E7DCCB" opacity=".9" filter="url(#nevoa)"/>'
    out += fern([(30, 220), (40, 186), (56, 160), (70, 128)], 12, 22, PERG, sw=1)
    out += fern([(70, 220), (82, 196), (100, 180), (120, 166)], 10, 18, '#B9A386', sw=1)
    out += '</g>'
    return out

def cartouche(x0, y0, x1, y1, c):
    return (f'M{x0+c} {y0}L{x1-c} {y0}A{c} {c} 0 0 0 {x1} {y0+c}L{x1} {y1-c}A{c} {c} 0 0 0 {x1-c} {y1}'
            f'L{x0+c} {y1}A{c} {c} 0 0 0 {x0} {y1-c}L{x0} {y0+c}A{c} {c} 0 0 0 {x0+c} {y0}Z')

@el('moldura-ornamentada', 'Moldura ornamentada', 'Cartela com borda verde, filete dourado e samambaias.', (220, 280), 'colagem', ROXO, paper=True)
def _():
    out = f'<path fill="{VERDE}" d="{cartouche(10, 10, 210, 270, 22)}" filter="url(#sombra)"/>'
    out += f'<path fill="none" stroke="url(#ouro)" stroke-width="1.6" d="{cartouche(17, 17, 203, 263, 18)}"/>'
    out += f'<path fill="#EBDFCD" d="{cartouche(24, 24, 196, 256, 16)}"/>'
    out += f'<path fill="none" stroke="url(#ouro)" stroke-width=".8" d="{cartouche(30, 30, 190, 250, 13)}"/>'
    out += '<clipPath id="cm1"><path d="' + cartouche(24, 24, 196, 256, 16) + '"/></clipPath><g clip-path="url(#cm1)">'
    out += fern([(30, 140), (40, 100), (52, 70), (80, 40)], 12, 18, VERDE, sw=1)
    out += sprig([(30, 170), (40, 150), (50, 136), (64, 124)], 5, 9, '#4D6B55')
    out += fern([(190, 140), (180, 180), (168, 210), (140, 240)], 12, 18, VERDE, sw=1)
    out += sprig([(190, 110), (180, 128), (170, 140), (156, 150)], 5, 9, '#4D6B55')
    for (x, y) in [(60, 60), (162, 222), (48, 92)]: out += flower(x, y, 5, '#F7F0E4')
    out += '</g>'
    for cy, s in ((10, 1), (270, -1)):
        out += (f'<path {GS} stroke-width="1.4" d="M86 {cy}C96 {cy+s*12} 104 {cy+s*12} 110 {cy+s*4}C116 {cy+s*12} 124 {cy+s*12} 134 {cy}'
                f'M92 {cy+s*2}C84 {cy-s*8} 74 {cy-s*2} 70 {cy+s*4}M128 {cy+s*2}C136 {cy-s*8} 146 {cy-s*2} 150 {cy+s*4}"/>')
        out += f'<path {G} d="M110 {cy-6}L116 {cy}L110 {cy+6}L104 {cy}Z"/>'
    return out

@el('marcador', 'Marcador de página', 'Fita vertical com padrão dourado de losangos e estrelas.', (80, 300), 'colagem', PERG)
def _():
    out = f'<path fill="{VERDE}" d="M8 6L72 6L72 294L40 274L8 294Z" filter="url(#sombra)"/>'
    out += f'<path fill="none" stroke="url(#ouro)" stroke-width="1" d="M14 12L66 12L66 282L40 264L14 282Z"/>'
    out += f'<path fill="none" stroke="url(#ouro)" stroke-width=".6" d="M18 16L62 16L62 274L40 258L18 274Z"/>'
    for i in range(7):
        y = 40 + i*32
        out += f'<path {GS} stroke-width=".9" d="M40 {y-14}L54 {y}L40 {y+14}L26 {y}Z"/>'
        out += sparkle(40, y, 6) if i % 2 else dot(40, y, 2.4)
        out += dot(40, y + 16, 1.2)
    return out

# ---------------- saída ----------------
def defs(e, uid):
    w, h = e['vb']; c0, c1, c2 = GOLDS[e['gold']]
    d = (f'<linearGradient id="ouro" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="{h}">'
         f'<stop offset="0" stop-color="{c0}"/><stop offset=".5" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
         f'<radialGradient id="luz"><stop offset="0" stop-color="{c1}" stop-opacity=".85"/><stop offset=".35" stop-color="{c1}" stop-opacity=".35"/>'
         f'<stop offset="1" stop-color="{c1}" stop-opacity="0"/></radialGradient>'
         # folha de ouro: ruído fino multiplicado só dentro da forma
         '<filter id="folha" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4" result="t"/>'
         '<feColorMatrix in="t" type="saturate" values="0" result="g"/>'
         '<feComponentTransfer in="g" result="g2"><feFuncR type="linear" slope=".55" intercept=".72"/><feFuncG type="linear" slope=".55" intercept=".72"/>'
         '<feFuncB type="linear" slope=".55" intercept=".72"/><feFuncA type="table" tableValues="1 1"/></feComponentTransfer>'
         '<feBlend in="SourceGraphic" in2="g2" mode="multiply" result="b"/><feComposite in="b" in2="SourceGraphic" operator="in"/></filter>'
         f'<filter id="brilho" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur in="SourceAlpha" stdDeviation="{e["glow"] or 1}" result="bl"/>'
         f'<feFlood flood-color="{c1}" flood-opacity=".55"/><feComposite in2="bl" operator="in" result="gl"/>'
         '<feMerge><feMergeNode in="gl"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         '<filter id="sombra" x="-15%" y="-15%" width="130%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#000" flood-opacity=".28"/></filter>'
         '<filter id="nevoa" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>'
         '<filter id="papel" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="3" seed="9" result="t"/>'
         '<feColorMatrix in="t" type="matrix" values="0 0 0 0 .35  0 0 0 0 .28  0 0 0 0 .2  0 0 0 .22 0" result="n"/>'
         '<feComposite in="n" in2="SourceGraphic" operator="in" result="nn"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="nn"/></feMerge></filter>')
    return d.replace('id="', f'id="{uid}').replace('url(#', f'url(#{uid}')

def svg(e, uid='x'):
    w, h = e['vb']
    body = e['fn']().replace('id="', f'id="{uid}').replace('url(#', f'url(#{uid}')
    wrap = body
    if e['foil'] and e['cat'] != 'colagem': wrap = f'<g filter="url(#{uid}folha)">{wrap}</g>'
    if e['glow']: wrap = f'<g filter="url(#{uid}brilho)">{wrap}</g>'
    if e['paper']: wrap = f'<g filter="url(#{uid}papel)">{wrap}</g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><defs>{defs(e, uid)}</defs>{wrap}</svg>'

# ================= MOLDURAS (da primeira biblioteca, com o novo acabamento) =================
def _importar_molduras():
    import importlib.util
    spec = importlib.util.spec_from_file_location('v1', os.path.join(HERE, '..', 'elementos', 'gerar.py'))
    v1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)
    fundos = [PERG, PETRO, ROXO, VERDE, PERG, PETRO]
    for i, e in enumerate([e for e in v1.E if e['cat'] == 'molduras']):
        def fn(f0=e['fn']):
            return (f0().replace('class="fl"', 'fill="url(#ouro)"')
                    .replace('class="ln"', 'fill="none" stroke="url(#ouro)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'))
        bg = fundos[i % len(fundos)]
        E.append(dict(key=e['key'], nome=e['nome'], desc=e['desc'], vb=e['vb'], cat='molduras', bg=bg,
                      gold='metalico', glow=2, foil=True, paper=False, fn=fn))
_importar_molduras()

if __name__ == '__main__':
    import copy
    for v in ('metalico', 'velho'): os.makedirs(os.path.join(HERE, 'svg', v), exist_ok=True)
    for e in E:
        versions = ['metalico', 'velho'] if e['cat'] != 'colagem' else [e['gold']]
        for v in versions:
            ee = copy.copy(e); ee['gold'] = v
            open(os.path.join(HERE, 'svg', v, e['key'] + '.svg'), 'w').write(svg(ee, 'e'))
    print(len(E), 'elementos')
