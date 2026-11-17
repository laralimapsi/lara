# Monta o catálogo (HTML) com os elementos gerados em gerar.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar
HERE = os.path.dirname(os.path.abspath(__file__))
CATS = [('natureza', 'Folhagens & natureza', 'Ramos, flores e a floresta: o lado orgânico da marca.'),
        ('mistico', 'Místico & celestial', 'Lua, estrelas, cristais e símbolos de intuição.'),
        ('molduras', 'Portais & molduras', 'Estruturas para emoldurar títulos, nomes e preços.'),
        ('divisores', 'Divisores & detalhes', 'Para separar seções, criar texturas e marcar o centro.')]
BGS = [('#3B2340', 'metalico', 'Roxo'), ('#11281A', 'metalico', 'Verde'), ('#D6C2AA', 'velho', 'Pergaminho'), ('#2E4F4A', 'metalico', 'Petróleo')]
CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;background:#111}
.pg{position:relative;width:1080px;height:1350px;overflow:hidden;color:#D6C2AA;font-family:'EB Garamond',serif;
 background:radial-gradient(ellipse 60% 40% at 70% 15%,rgba(120,70,130,.35),transparent 70%),radial-gradient(ellipse 120% 100% at 50% 45%,#3B2340 0%,#2C1A32 55%,#1B0F20 100%)}
.cab{position:absolute;top:56px;left:0;right:0;text-align:center}
.cab .ey{font-family:'Cinzel';font-weight:600;font-size:13px;letter-spacing:.24em;opacity:.8}
.cab h1{font-family:'Cinzel';font-weight:400;font-size:64px;letter-spacing:.05em;margin-top:14px;line-height:1}
.cab p{font-family:'Cormorant Garamond';font-style:italic;font-weight:500;font-size:23px;margin-top:12px}
.grid{position:absolute;top:258px;left:56px;right:56px;bottom:84px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.card{border-radius:14px;display:flex;flex-direction:column;padding:14px 16px 16px;border:1px solid rgba(214,194,170,.16);min-height:0}
.card .art{flex:1;display:flex;align-items:center;justify-content:center;min-height:0;padding:6px}
.card .art svg{width:100%;height:100%}
.card h3{font-family:'Cinzel';font-weight:600;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;margin-top:8px}
.card p{font-family:'EB Garamond';font-style:italic;font-size:14.5px;line-height:1.3;margin-top:4px;opacity:.85}
.card .bg{font-family:'Cinzel';font-size:8.5px;letter-spacing:.2em;text-transform:uppercase;opacity:.55;align-self:flex-end}
.pe{position:absolute;bottom:36px;left:0;right:0;text-align:center;font-family:'Cinzel';font-size:11px;letter-spacing:.26em;opacity:.55}
'''
def page(idx, cat, title, sub):
    els = [e for e in gerar.E if e['cat'] == cat]
    cols = {'molduras': 3, 'divisores': 2}.get(cat, 4)
    order = ['divisor-celeste', 'divisor-botanico', 'arvore-vida', 'poeira-estelar']
    if cat == 'divisores': els.sort(key=lambda e: order.index(e['key']))
    slots = sum(e['span'] for e in els); rows = -(-slots // cols)
    cards = ''
    for i, e in enumerate(els):
        bg, gold, nm = BGS[(i + idx) % 4]
        fg = '#3B2340' if gold == 'velho' else '#D6C2AA'
        art = gerar.svg(e, gold, f'{cat[0]}{i}')
        cards += (f'<div class="card" style="background:{bg};color:{fg};grid-column:span {e["span"]}">'
                  f'<div class="bg">{nm} · dourado {"velho" if gold=="velho" else "metálico"}</div>'
                  f'<div class="art">{art}</div><h3>{e["nome"]}</h3><p>{e["desc"]}</p></div>')
    return (f'<section class="pg" id="p{idx+1}"><div class="cab"><div class="ey">Elementos · {idx+1} de 4</div>'
            f'<h1>{title}</h1><p>{sub}</p></div>'
            f'<div class="grid" style="grid-template-columns:repeat({cols},1fr);grid-template-rows:repeat({rows},1fr)">{cards}</div>'
            f'<div class="pe">Lara Oraculista · Biblioteca de elementos</div></section>')
html = ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Elementos — Lara Oraculista</title>'
        '<link rel="stylesheet" href="../tipografia/fonts/fonts.css"><style>' + CSS + '</style></head><body>'
        + ''.join(page(i, *c) for i, c in enumerate(CATS)) + '</body></html>')
open(os.path.join(HERE, 'catalogo.html'), 'w').write(html)
