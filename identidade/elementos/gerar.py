# Gera a biblioteca de elementos da identidade Lara Oraculista.
# Cada elemento vira um SVG independente (dourado metálico e dourado velho)
# e o catálogo em HTML para visualização.
import math, random, os

HERE = os.path.dirname(os.path.abspath(__file__))
GOLDS = {
    'metalico': ('#A98545', '#CDAE6E', '#A98545'),
    'velho':    ('#6E5523', '#A68844', '#6E5523'),
}

def f(v): return f'{v:.2f}'.rstrip('0').rstrip('.')

# ---------- geometria ----------
def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

def bez_tan(p0, p1, p2, p3, t):
    u = 1 - t
    dx = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    n = math.hypot(dx, dy) or 1
    return dx/n, dy/n

def cpath(p0, p1, p2, p3):
    return f'M{f(p0[0])} {f(p0[1])}C{f(p1[0])} {f(p1[1])} {f(p2[0])} {f(p2[1])} {f(p3[0])} {f(p3[1])}'

def leaf(x, y, ang, L, W, bend=0.0, vein=False, line=False, sw=1.2):
    """folha com base em (x,y), apontando para ang (graus)."""
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    tip = (x + dx*L + nx*bend*L, y + dy*L + ny*bend*L)
    c1 = (x + dx*.30*L + nx*W, y + dy*.30*L + ny*W)
    c2 = (x + dx*.78*L + nx*W*.62 + nx*bend*L*.6, y + dy*.78*L + ny*W*.62 + ny*bend*L*.6)
    c3 = (x + dx*.78*L - nx*W*.62 + nx*bend*L*.6, y + dy*.78*L - ny*W*.62 + ny*bend*L*.6)
    c4 = (x + dx*.30*L - nx*W, y + dy*.30*L - ny*W)
    d = (f'M{f(x)} {f(y)}C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(tip[0])} {f(tip[1])}'
         f'C{f(c3[0])} {f(c3[1])} {f(c4[0])} {f(c4[1])} {f(x)} {f(y)}Z')
    out = f'<path d="{d}" class="{"ln" if line else "fl"}"/>'
    if vein:
        m = (x + dx*.5*L + nx*bend*L*.3, y + dy*.5*L + ny*bend*L*.3)
        out += f'<path d="M{f(x)} {f(y)}Q{f(m[0])} {f(m[1])} {f(x+(tip[0]-x)*.86)} {f(y+(tip[1]-y)*.86)}" class="ln" style="stroke-width:{sw*.7}"/>'
    return out

def star4(x, y, r, thin=0.18):
    t = r*thin
    return (f'<path class="fl" d="M{f(x)} {f(y-r)}Q{f(x+t)} {f(y-t)} {f(x+r)} {f(y)}Q{f(x+t)} {f(y+t)} {f(x)} {f(y+r)}'
            f'Q{f(x-t)} {f(y+t)} {f(x-r)} {f(y)}Q{f(x-t)} {f(y-t)} {f(x)} {f(y-r)}Z"/>')

def star8(x, y, r):
    pts = []
    for i in range(16):
        a = math.pi/8*i - math.pi/2
        rr = r if i % 4 == 0 else (r*.55 if i % 2 == 0 else r*.16)
        pts.append(f'{f(x+rr*math.cos(a))} {f(y+rr*math.sin(a))}')
    return f'<path class="fl" d="M{" L".join(pts)}Z"/>'

def circle(x, y, r, cls='ln', sw=None):
    st = f' style="stroke-width:{sw}"' if sw else ''
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" class="{cls}"{st}/>'

def line(x1, y1, x2, y2, sw=None, cls='ln'):
    st = f' style="stroke-width:{sw}"' if sw else ''
    return f'<path d="M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}" class="{cls}"{st}/>'

def branch(p0, p1, p2, p3, n, Lmax, Lmin, Wr, spread=48, alternate=True, tip=True, line_=False, vein=False, t0=0.12, sw=1.5, bend=0.0, pet=0.0):
    out = f'<path d="{cpath(p0,p1,p2,p3)}" class="ln" style="stroke-width:{sw}"/>'
    for i in range(n):
        t = t0 + (0.92 - t0) * i / max(n-1, 1)
        x, y = bez(p0, p1, p2, p3, t); tx, ty = bez_tan(p0, p1, p2, p3, t)
        base = math.degrees(math.atan2(ty, tx))
        L = Lmax - (Lmax - Lmin) * t
        sides = ([1] if i % 2 == 0 else [-1]) if alternate else [1, -1]
        for s in sides:
            aa = math.radians(base + s*spread)
            bx, by = x + pet*math.cos(aa), y + pet*math.sin(aa)
            if pet: out += line(x, y, bx, by, sw*.7)
            out += leaf(bx, by, base + s*spread, L, L*Wr, bend=bend*s, vein=vein, line=line_)
    if tip:
        tx, ty = bez_tan(p0, p1, p2, p3, 1)
        out += leaf(p3[0], p3[1], math.degrees(math.atan2(ty, tx)), Lmin*1.05, Lmin*1.05*Wr, vein=vein, line=line_)
    return out

def mirror(content, cx):
    return content + f'<g transform="translate({2*cx} 0) scale(-1 1)">{content}</g>'

# ---------- elementos ----------
E = []
def el(key, nome, desc, vb, cat, span=1):
    def deco(fn):
        E.append(dict(key=key, nome=nome, desc=desc, vb=vb, cat=cat, span=span, fn=fn)); return fn
    return deco

# ===== FOLHAGENS & NATUREZA =====
@el('eucalipto', 'Ramo de eucalipto', 'Folhas redondas e alternadas, leve e orgânico.', (200, 200), 'natureza')
def _():
    return branch((40, 188), (60, 130), (120, 90), (160, 18), 14, 25, 12, 0.78, spread=62, sw=1.5, pet=5)

@el('samambaia', 'Samambaia', 'Fronde que se desenrola, símbolo de renovação.', (200, 200), 'natureza')
def _():
    p = [(40, 190), (70, 130), (120, 70), (170, 28)]
    out = f'<path d="{cpath(*p)}" class="ln" style="stroke-width:1.6"/>'
    n = 22
    for i in range(n):
        t = 0.06 + 0.9*i/(n-1)
        x, y = bez(*p, t); tx, ty = bez_tan(*p, t); a = math.degrees(math.atan2(ty, tx))
        L = 34*(1-t)**0.8 + 5
        for s in (1, -1):
            out += leaf(x, y, a + s*62, L, L*.2, bend=-0.08*s)
    # broto enrolado na ponta
    out += '<path d="M170 28c6-4 12-2 12 4s-6 8-10 5-2-8 2-8" class="ln" style="stroke-width:1.4"/>'
    return out

@el('oliveira', 'Ramo de oliveira', 'Folhas finas e frutos: paz, sabedoria e colheita.', (200, 200), 'natureza')
def _():
    out = branch((25, 175), (60, 150), (120, 110), (178, 35), 9, 40, 24, 0.24, spread=36, sw=1.5, bend=0.06)
    for (x, y, a) in [(92, 128, 30), (128, 98, -20), (70, 150, 70)]:
        out += f'<ellipse cx="{x}" cy="{y}" rx="5.2" ry="7.4" transform="rotate({a} {x} {y})" class="fl"/>'
        out += line(x, y-7, x-2, y-12, 1.1)
    return out

@el('mosquitinho', 'Mosquitinho', 'Flores miúdas em nuvem, delicadas como no seu moodboard.', (200, 200), 'natureza')
def _():
    rnd = random.Random(7); out = ''
    def grow(x, y, a, L, d):
        nonlocal out
        x2, y2 = x + L*math.cos(math.radians(a)), y + L*math.sin(math.radians(a))
        out += f'<path d="M{f(x)} {f(y)}Q{f((x+x2)/2+rnd.uniform(-4,4))} {f((y+y2)/2)} {f(x2)} {f(y2)}" class="ln" style="stroke-width:{f(1.5-d*.25)}"/>'
        if d >= 4:
            r = rnd.uniform(3.4, 5.2)
            for k in range(5):
                aa = k*72 + rnd.uniform(0, 30)
                out += circle(x2 + r*.55*math.cos(math.radians(aa)), y2 + r*.55*math.sin(math.radians(aa)), r*.5, 'fl')
            out += circle(x2, y2, r*.32, 'fl')
            return
        for _ in range(rnd.choice([2, 3])):
            grow(x2, y2, a + rnd.uniform(-44, 44), L*rnd.uniform(.72, .9), d+1)
    grow(100, 196, -90, 58, 0)
    return out

@el('lavanda', 'Lavanda', 'Calma, purificação e proteção.', (200, 200), 'natureza')
def _():
    out = ''
    for (bx, lean) in [(85, -10), (110, 6), (128, 18)]:
        top = (bx + lean, 30 + abs(lean))
        p = [(100, 195), (100, 140), (bx, 90), top]
        out += f'<path d="{cpath(*p)}" class="ln" style="stroke-width:1.4"/>'
        for i in range(9):
            t = 0.55 + 0.45*i/8
            x, y = bez(*p, t); tx, ty = bez_tan(*p, t); a = math.degrees(math.atan2(ty, tx))
            s = 6.5 - i*.35
            for side in (1, -1):
                out += leaf(x, y, a + side*28, s, s*.55)
    out += leaf(100, 190, -120, 50, 4.5) + leaf(100, 190, -62, 46, 4.5)
    return out

@el('cogumelos', 'Cogumelos da floresta', 'Mistério do solo, o oculto que nasce na sombra.', (200, 200), 'natureza')
def _():
    out = ''
    def mush(x, base, h, w, tilt):
        nonlocal out
        g = f'<g transform="rotate({tilt} {x} {base})">'
        top = base - h
        g += f'<path d="M{x-w*.16} {base}C{x-w*.12} {base-h*.4} {x-w*.1} {top+h*.38} {x-w*.12} {top+h*.3}L{x+w*.12} {top+h*.3}C{x+w*.1} {top+h*.38} {x+w*.12} {base-h*.4} {x+w*.16} {base}" class="ln"/>'
        g += f'<path d="M{x-w*.5} {top+h*.3}C{x-w*.5} {top-h*.05} {x-w*.2} {top-h*.2} {x} {top-h*.2}C{x+w*.2} {top-h*.2} {x+w*.5} {top-h*.05} {x+w*.5} {top+h*.3}Q{x} {top+h*.22} {x-w*.5} {top+h*.3}Z" class="fl"/>'
        for k in range(-3, 4):
            g += line(x + k*w*.06, top+h*.31, x + k*w*.09, top+h*.36, 0.9)
        g += '</g>'
        out += g
    mush(78, 182, 92, 86, -6)
    mush(140, 184, 58, 56, 8)
    for (gx, gl, ga) in [(40, 26, -100), (52, 20, -78), (166, 22, -96), (176, 16, -70), (112, 14, -88)]:
        out += leaf(gx, 186, ga, gl, 2.6)
    out += line(24, 186, 186, 186, 1.3)
    out += star4(160, 48, 7) + star4(40, 70, 4.5)
    return out

@el('floresta', 'Floresta & montanhas', 'Pinheiros e montanhas: o caminho e a jornada.', (260, 160), 'natureza')
def _():
    out = '<path d="M10 120 L60 62 L84 88 L122 40 L160 92 L184 70 L250 120" class="ln" style="stroke-width:1.3"/>'
    out += '<path d="M108 56 L122 40 L134 58" class="ln" style="stroke-width:1"/>'
    out += line(10, 140, 250, 140, 1.3)
    rnd = random.Random(3)
    for (x, h) in [(28, 46), (46, 60), (64, 40), (190, 52), (210, 68), (230, 44), (96, 34), (164, 30)]:
        out += line(x, 140, x, 140-h, 1.2)
        for k in range(5):
            yy = 140 - h + k*h*.17
            w = 4 + k*3.2
            out += f'<path d="M{x-w} {yy+h*.14}L{x} {yy}L{x+w} {yy+h*.14}" class="ln" style="stroke-width:1.2"/>'
    out += '<path d="M200 22a10 10 0 1 0 8 16a8 8 0 1 1 -8 -16Z" class="fl"/>'
    out += star4(60, 26, 4) + star4(150, 16, 3)
    return out

@el('mariposa', 'Mariposa lunar', 'A noturna que segue a lua: intuição e transformação.', (200, 200), 'natureza')
def _():
    half = ('<path d="M102 92C120 60 160 40 186 52C194 72 170 104 132 110C120 112 108 104 102 92Z" class="ln" style="stroke-width:1.5"/>'
            '<path d="M102 104C126 108 160 120 164 150C156 172 124 168 112 146C106 134 102 118 102 104Z" class="ln" style="stroke-width:1.5"/>'
            '<path d="M150 66a11 11 0 1 0 6 18a9 9 0 1 1 -6 -18Z" class="fl"/>'
            '<circle cx="136" cy="140" r="7" class="ln"/><circle cx="136" cy="140" r="2.6" class="fl"/>'
            '<path d="M102 66C106 46 118 30 134 24" class="ln" style="stroke-width:1.2"/>')
    for k in range(6):
        x, y = bez((102, 66), (106, 46), (118, 30), (134, 24), 0.25 + k*.14)
        half += line(x, y, x + 4, y - 3, 0.9)
    for (x, y) in [(176, 70), (168, 86), (156, 98), (152, 156), (140, 162)]:
        half += circle(x, y, 1.4, 'fl')
    body = '<ellipse cx="100" cy="100" rx="5" ry="26" class="fl"/>' + circle(100, 70, 5, 'fl')
    return mirror(half, 100) + body

# ===== MÍSTICO & CELESTIAL =====
@el('fases-da-lua', 'Fases da lua', 'O ciclo completo: do crescente ao minguante.', (400, 90), 'mistico', span=2)
def _():
    out = ''; R = 22; cy = 45; r = R - 3.5
    spec = [('wax', .2), ('wax', .5), ('wax', .8), ('full', 1), ('wan', .8), ('wan', .5), ('wan', .2)]
    for i, (kind, ph) in enumerate(spec):
        x = 40 + i*53.3
        out += circle(x, cy, R, 'ln', 1.2)
        if kind == 'full':
            out += circle(x, cy, r, 'fl'); continue
        k = abs(1 - 2*ph) * r          # raio horizontal do terminador
        right = kind == 'wax'          # crescente: luz à direita
        s_outer = 1 if right else 0
        # terminador: côncavo (crescente) ou convexo (gibosa)
        s_term = (0 if ph < .5 else 1) if right else (1 if ph < .5 else 0)
        out += (f'<path class="fl" d="M{f(x)} {f(cy-r)}A{f(r)} {f(r)} 0 0 {s_outer} {f(x)} {f(cy+r)}'
                f'A{f(max(k,.01))} {f(r)} 0 0 {s_term} {f(x)} {f(cy-r)}Z"/>')
    return out

@el('lua-ramo', 'Lua envolta em ramos', 'O místico e a natureza abraçados.', (200, 200), 'mistico')
def _():
    out = '<path class="fl" d="M118 26A76 76 0 1 0 172 150A62 62 0 1 1 118 26Z"/>'
    pts = [(150, 176), (90, 196), (30, 150), (34, 80)]
    out += branch(*pts, 10, 22, 12, 0.42, spread=50, sw=1.4)
    out += star4(160, 70, 9) + star4(178, 104, 5) + star4(140, 40, 4)
    return out

@el('olho', 'Olho que tudo vê', 'Visão, intuição e o véu entre os mundos.', (200, 200), 'mistico')
def _():
    out = '<path d="M28 108C60 66 140 66 172 108C140 150 60 150 28 108Z" class="ln" style="stroke-width:1.8"/>'
    out += circle(100, 108, 26, 'ln', 1.5) + circle(100, 108, 13, 'fl')
    out += star4(106, 102, 4.5)
    for k in range(-6, 7):
        a = -90 + k*13; L = 22 if k % 2 == 0 else 13
        r0 = 52
        x0, y0 = 100 + r0*math.cos(math.radians(a)), 108 + r0*math.sin(math.radians(a))
        out += line(x0, y0, 100 + (r0+L)*math.cos(math.radians(a)), 108 + (r0+L)*math.sin(math.radians(a)), 1.3)
    for k in range(-3, 4):
        if k == 0: continue
        x = 100 + k*17; y = 140 - abs(k)*3.5
        out += leaf(x, y, 90 + k*14, 13, 4.6)
    out += leaf(100, 142, 90, 16, 5)
    return out

@el('constelacao', 'Constelação', 'Mapa das estrelas: destino e orientação.', (200, 200), 'mistico')
def _():
    pts = [(30, 140), (62, 112), (96, 124), (118, 84), (150, 70), (172, 38), (140, 150), (96, 124)]
    out = '<path d="M' + ' L'.join(f'{x} {y}' for x, y in pts[:6]) + '" class="ln" style="stroke-width:1;stroke-dasharray:3 4"/>'
    out += '<path d="M96 124 L140 150 L170 132" class="ln" style="stroke-width:1;stroke-dasharray:3 4"/>'
    for (x, y), r in zip([(30, 140), (62, 112), (96, 124), (118, 84), (150, 70), (172, 38), (140, 150), (170, 132)], [5, 4, 8, 5, 6, 10, 5, 4]):
        out += star4(x, y, r) if r >= 6 else circle(x, y, r*.5, 'fl')
    rnd = random.Random(11)
    for _ in range(26):
        out += circle(rnd.uniform(10, 190), rnd.uniform(10, 190), rnd.uniform(.5, 1.2), 'fl')
    out += circle(100, 100, 90, 'ln', .6)
    return out

@el('sol-lua', 'Sol e lua', 'Equilíbrio entre luz e sombra.', (200, 200), 'mistico')
def _():
    out = circle(100, 100, 42, 'ln', 1.6) + circle(100, 100, 36, 'ln', .8)
    out += '<path class="fl" d="M92 70A30 30 0 1 0 122 120A24 24 0 1 1 92 70Z"/>'
    for k in range(24):
        a = math.radians(k*15)
        if k % 2 == 0:
            x0, y0 = 100 + 50*math.cos(a), 100 + 50*math.sin(a)
            x1, y1 = 100 + 86*math.cos(a), 100 + 86*math.sin(a)
            nx, ny = -math.sin(a), math.cos(a)
            out += f'<path class="fl" d="M{f(x0+nx*3)} {f(y0+ny*3)}L{f(x1)} {f(y1)}L{f(x0-nx*3)} {f(y0-ny*3)}Z"/>'
        else:
            pts = []
            for j in range(9):
                rr = 50 + j*3.6; off = math.sin(j*1.6)*2.4
                pts.append((100 + rr*math.cos(a) - off*math.sin(a), 100 + rr*math.sin(a) + off*math.cos(a)))
            out += '<path d="M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + '" class="ln" style="stroke-width:1.1"/>'
    return out

@el('cristais', 'Cristais', 'Ametista e quartzo: energia, cura e proteção.', (200, 200), 'mistico')
def _():
    def crystal(x, base, w, h, tilt):
        top = base - h
        pts = [(x-w/2, base), (x-w/2, top+w*.6), (x, top), (x+w/2, top+w*.6), (x+w/2, base)]
        g = f'<g transform="rotate({tilt} {x} {base})">'
        g += '<path d="M' + ' L'.join(f'{f(a)} {f(b)}' for a, b in pts) + '" class="ln" style="stroke-width:1.6"/>'
        g += f'<path d="M{x-w/2} {top+w*.6}L{x-w*.08} {top+w*.75}L{x} {top}M{x-w*.08} {top+w*.75}L{x+w/2} {top+w*.6}M{x-w*.08} {top+w*.75}L{x-w*.08} {base}" class="ln" style="stroke-width:1"/>'
        g += f'<path d="M{x-w*.08} {top+w*.75}L{x} {top}L{x+w/2} {top+w*.6}Z" class="fl" style="opacity:.55"/>'
        return g + '</g>'
    out = crystal(100, 182, 40, 140, 0) + crystal(64, 184, 30, 96, -16) + crystal(138, 184, 28, 84, 15)
    out += crystal(36, 186, 18, 46, -30) + crystal(166, 186, 18, 50, 28)
    out += line(20, 186, 180, 186, 1.3)
    out += star4(150, 46, 8) + star4(46, 70, 5) + star4(170, 92, 3.5)
    return out

@el('chave', 'Chave antiga', 'Abrir caminhos e revelar o que está guardado.', (200, 200), 'mistico')
def _():
    out = '<g transform="rotate(-38 100 100)">'
    out += circle(100, 42, 26, 'ln', 1.8) + circle(100, 42, 19, 'ln', .9)
    out += star8(100, 42, 14)
    out += '<path d="M96 68L96 170M104 68L104 170" class="ln" style="stroke-width:1.6"/>'
    out += '<path d="M90 82L110 82M92 90L108 90" class="ln" style="stroke-width:1.4"/>'
    out += '<path d="M104 140L122 140L122 150L114 150L114 158L122 158L122 168L104 168" class="ln" style="stroke-width:1.6"/>'
    out += '<path d="M96 170Q100 176 104 170" class="ln" style="stroke-width:1.6"/>'
    out += '</g>'
    out += leaf(118, 104, 20, 22, 7, vein=True, line=True) + leaf(118, 104, 70, 18, 6, vein=True, line=True)
    return out

@el('arvore-vida', 'Árvore da vida', 'Raízes e galhos espelhados: o de cima e o de baixo.', (200, 200), 'divisores')
def _():
    rnd = random.Random(5); out = ''
    def grow(x, y, a, L, d, up):
        nonlocal out
        x2 = x + L*math.cos(math.radians(a)); y2 = y + L*math.sin(math.radians(a))
        out += f'<path d="M{f(x)} {f(y)}L{f(x2)} {f(y2)}" class="ln" style="stroke-width:{f(max(3.8-d*.6, .7))}"/>'
        if up and d >= 4:
            out += leaf(x2, y2, a + rnd.uniform(-30, 30), 8 if d == 6 else 6.5, 3.2 if d == 6 else 2.6)
        if d == (6 if up else 5):
            return
        spread = 30 + d*5
        grow(x2, y2, a - spread + rnd.uniform(-6, 6), L*.78, d+1, up)
        grow(x2, y2, a + spread + rnd.uniform(-6, 6), L*.78, d+1, up)
    out += line(100, 128, 100, 100, 3.8)
    grow(100, 100, -90, 22, 1, True)
    grow(100, 128, 90, 17, 1, False)
    out += circle(100, 100, 88, 'ln', 1.6) + circle(100, 100, 82, 'ln', .7)
    return out

# ===== PORTAIS, MOLDURAS & DIVISORES =====
@el('portal', 'Portal em arco', 'Moldura de passagem com vinha subindo.', (200, 260), 'molduras')
def _():
    def arch(inset, sw):
        l, r, b, top = 20+inset, 180-inset, 248-inset, 100
        rad = (r-l)/2
        return f'<path d="M{l} {b}L{l} {top}A{rad} {rad} 0 0 1 {r} {top}L{r} {b}Z" class="ln" style="stroke-width:{sw}"/>'
    out = arch(0, 1.6) + arch(8, .8)
    out += star8(100, 30, 9) + '<path class="fl" d="M96 64a9 9 0 1 0 8 14a7 7 0 1 1 -8 -14Z"/>'
    out += branch((22, 250), (6, 200), (30, 140), (24, 92), 8, 20, 11, 0.42, spread=52, sw=1.3)
    out += branch((178, 250), (196, 220), (172, 190), (180, 160), 4, 16, 10, 0.42, spread=52, sw=1.3)
    return out

@el('guirlanda', 'Guirlanda de folhas', 'Moldura circular aberta, para nomes e selos.', (200, 200), 'molduras')
def _():
    out = ''
    for side in (1, -1):
        n = 13
        for i in range(n):
            a = math.radians(90 + side*(12 + i*12.5))
            x, y = 100 + 76*math.cos(a), 100 + 76*math.sin(a)
            tang = math.degrees(a) + side*90
            L = 20 - i*.55
            out += leaf(x, y, tang - side*38, L, L*.4) if i % 2 == 0 else leaf(x, y, tang + side*30, L*.85, L*.36)
        out += f'<path d="M{f(100+76*math.cos(math.radians(90+side*6)))} {f(100+76*math.sin(math.radians(90+side*6)))}A76 76 0 0 {1 if side==1 else 0} {f(100+76*math.cos(math.radians(90+side*165)))} {f(100+76*math.sin(math.radians(90+side*165)))}" class="ln" style="stroke-width:1.4"/>'
    for a in (60, 120, 200, 340):
        out += circle(100 + 70*math.cos(math.radians(a)), 100 + 70*math.sin(math.radians(a)), 2.6, 'fl')
    out += star8(100, 22, 9)
    return out

@el('moldura-taro', 'Moldura de carta', 'Inspirada nas cartas de tarô, com sol e lua.', (180, 280), 'molduras')
def _():
    out = '<rect x="10" y="10" width="160" height="260" rx="10" class="ln" style="stroke-width:1.6"/>'
    out += '<path d="M22 262L22 70A68 68 0 0 1 158 70L158 262Z" class="ln" style="stroke-width:.8"/>'
    out += star8(90, 34, 10)
    out += '<path class="fl" d="M84 236a10 10 0 1 0 9 15a8 8 0 1 1 -9 -15Z"/>'
    for (x, y) in [(22, 22), (158, 22), (22, 258), (158, 258)]:
        out += star4(x, y, 5)
    out += line(40, 250, 70, 250, .9) + line(110, 250, 140, 250, .9)
    return out

@el('rosa-dos-ventos', 'Rosa dos ventos', 'Astrolábio e direção: escolhas e caminhos.', (200, 200), 'molduras')
def _():
    out = circle(100, 100, 86, 'ln', 1.5) + circle(100, 100, 78, 'ln', .7) + circle(100, 100, 30, 'ln', .9)
    for k in range(72):
        a = math.radians(k*5); L = 7 if k % 9 == 0 else 3.5
        out += line(100 + 78*math.cos(a), 100 + 78*math.sin(a), 100 + (78-L)*math.cos(a), 100 + (78-L)*math.sin(a), .8)
    for k in range(8):
        a = math.radians(k*45 - 90); R = 70 if k % 2 == 0 else 44; w = 9 if k % 2 == 0 else 6
        x1, y1 = 100 + R*math.cos(a), 100 + R*math.sin(a)
        nx, ny = -math.sin(a), math.cos(a)
        out += f'<path class="fl" d="M100 100L{f(100+w*math.cos(a)+nx*w)} {f(100+w*math.sin(a)+ny*w)}L{f(x1)} {f(y1)}Z"/>'
        out += f'<path class="ln" style="stroke-width:.9" d="M100 100L{f(100+w*math.cos(a)-nx*w)} {f(100+w*math.sin(a)-ny*w)}L{f(x1)} {f(y1)}"/>'
    out += circle(100, 100, 4, 'fl')
    return out

@el('divisor-celeste', 'Divisor celeste', 'Lua cheia entre crescentes, para separar seções.', (400, 60), 'divisores', span=2)
def _():
    out = ('<path d="M10 30L148 30" class="ln" style="stroke-width:1.2;stroke-dasharray:1 5;stroke-linecap:round"/>'
           '<path d="M252 30L390 30" class="ln" style="stroke-width:1.2;stroke-dasharray:1 5;stroke-linecap:round"/>')
    out += circle(200, 30, 14, 'fl') + circle(200, 30, 19, 'ln', .8)
    out += '<path class="fl" d="M174 18a12 12 0 1 0 0 24a15 15 0 0 1 0 -24Z"/>'
    out += '<path class="fl" d="M226 18a12 12 0 1 1 0 24a15 15 0 0 0 0 -24Z"/>'
    out += star4(156, 30, 4) + star4(244, 30, 4)
    return out

@el('divisor-botanico', 'Divisor botânico', 'Ramos espelhados com estrela ao centro.', (400, 60), 'divisores', span=2)
def _():
    half = branch((216, 30), (260, 26), (320, 34), (388, 30), 11, 17, 9, .42, spread=46, sw=1.2, tip=True)
    out = mirror(half, 200)
    out += star8(200, 30, 12)
    return out

@el('cantoneira', 'Cantoneira de samambaia', 'Canto de moldura com fronde e estrela.', (200, 200), 'molduras')
def _():
    out = '<path d="M14 186L14 14L186 14" class="ln" style="stroke-width:1.5"/><path d="M22 186L22 22L186 22" class="ln" style="stroke-width:.7"/>'
    p = [(26, 26), (60, 50), (90, 70), (140, 120)]
    out += f'<path d="{cpath(*p)}" class="ln" style="stroke-width:1.3"/>'
    for i in range(16):
        t = 0.08 + 0.9*i/15
        x, y = bez(*p, t); tx, ty = bez_tan(*p, t); a = math.degrees(math.atan2(ty, tx))
        L = 22*(1-t)**0.7 + 4
        for s in (1, -1):
            out += leaf(x, y, a + s*60, L, L*.22)
    out += star4(14, 14, 7) + star4(186, 14, 4) + star4(14, 186, 4)
    return out

@el('poeira-estelar', 'Poeira estelar', 'Brilhos soltos para fundos e texturas.', (200, 200), 'divisores')
def _():
    rnd = random.Random(21); out = ''
    for _ in range(14):
        out += star4(rnd.uniform(14, 186), rnd.uniform(14, 186), rnd.uniform(2.5, 9))
    for _ in range(40):
        out += circle(rnd.uniform(6, 194), rnd.uniform(6, 194), rnd.uniform(.5, 1.3), 'fl')
    return out


@el('selo-celeste', 'Selo celeste', 'Selo com espaço central para preço ou nome.', (200, 200), 'molduras')
def _():
    out = circle(100, 100, 84, 'ln', 1.6) + circle(100, 100, 77, 'ln', .7)
    out += '<circle cx="100" cy="100" r="64" class="ln" style="stroke-width:1.1;stroke-dasharray:1 5"/>'
    for k in range(12):
        a = math.radians(k*30 - 90)
        if k in (0, 6): continue
        out += star4(100 + 70.5*math.cos(a), 100 + 70.5*math.sin(a), 3.4 if k % 3 else 5)
    out += '<path class="fl" d="M96 6a11 11 0 1 0 9 17a9 9 0 1 1 -9 -17Z"/>'
    for side in (1, -1):
        for i in range(4):
            x = 100 + side*(10 + i*9); y = 188 - i*3.5
            out += leaf(x, y, -90 - side*(60 - i*8), 10, 3.6)
    out += star4(100, 186, 5)
    return out

# ---------- saída ----------
def svg(e, gold, uid, size=None):
    w, h = e['vb']; c0, c1, c2 = GOLDS[gold]
    g = f'g{uid}'
    dims = f' width="{size[0]}" height="{size[1]}"' if size else ''
    body = e['fn']().replace('class="fl"', f'class="f{uid}"').replace('class="ln"', f'class="l{uid}"')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"{dims}>'
            f'<defs><linearGradient id="{g}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="{h}">'
            f'<stop offset="0" stop-color="{c0}"/><stop offset=".5" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
            f'<style>.f{uid}{{fill:url(#{g})}}.l{uid}{{fill:none;stroke:url(#{g});stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}}</style></defs>'
            f'{body}</svg>')

if __name__ == '__main__':
    for gold in GOLDS:
        os.makedirs(os.path.join(HERE, 'svg', gold), exist_ok=True)
    for i, e in enumerate(E):
        for gold in GOLDS:
            open(os.path.join(HERE, 'svg', gold, f'{e["key"]}.svg'), 'w').write(svg(e, gold, f'{gold[0]}{i}'))
    print(len(E), 'elementos')
