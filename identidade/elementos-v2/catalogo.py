import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar
HERE = os.path.dirname(os.path.abspath(__file__))
CATS = [('estrelas', 'Estrelas com brilho', 'Folha de ouro com luz suave, para céus e destaques.', 3),
        ('misticos', 'Símbolos místicos', 'Luas, olho, talismãs e ornamentos em traço dourado.', 3),
        ('colagem', 'Colagem vintage', 'Selos, etiquetas, papel rasgado e molduras com textura de papel.', 3)]
CSS = '''*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;background:#111}
.pg{position:relative;width:1080px;height:1350px;overflow:hidden;color:#D6C2AA;font-family:'EB Garamond',serif;
background:radial-gradient(ellipse 60% 40% at 70% 15%,rgba(120,70,130,.35),transparent 70%),radial-gradient(ellipse 120% 100% at 50% 45%,#3B2340 0%,#2C1A32 55%,#1B0F20 100%)}
.cab{position:absolute;top:56px;left:0;right:0;text-align:center}
.cab .ey{font-family:'Cinzel';font-weight:600;font-size:13px;letter-spacing:.24em;opacity:.8}
.cab h1{font-family:'Cinzel';font-weight:400;font-size:62px;letter-spacing:.05em;margin-top:14px;line-height:1}
.cab p{font-family:'Cormorant Garamond';font-style:italic;font-weight:500;font-size:23px;margin-top:12px}
.grid{position:absolute;top:250px;left:56px;right:56px;bottom:80px;display:grid;gap:14px}
.card{border-radius:14px;display:flex;flex-direction:column;padding:12px 16px 14px;border:1px solid rgba(214,194,170,.16);min-height:0}
.card .art{flex:1;min-height:0;display:flex;align-items:center;justify-content:center}
.card .art img{max-width:100%;max-height:100%;width:100%;height:100%;object-fit:contain}
.card h3{font-family:'Cinzel';font-weight:600;font-size:12px;letter-spacing:.16em;text-transform:uppercase;margin-top:6px}
.card p{font-style:italic;font-size:14px;line-height:1.28;margin-top:3px;opacity:.85}
.pe{position:absolute;bottom:34px;left:0;right:0;text-align:center;font-family:'Cinzel';font-size:11px;letter-spacing:.26em;opacity:.55}'''
def page(i, cat, t, sub, cols):
    els = [e for e in gerar.E if e['cat'] == cat]; rows = -(-len(els)//cols)
    cards = ''
    for e in els:
        v = e['gold'] if cat == 'colagem' else ('velho' if e['bg'] == gerar.PERG else 'metalico')
        fg = '#3B2340' if e['bg'] == gerar.PERG else '#D6C2AA'
        cards += (f'<div class="card" style="background:{e["bg"]};color:{fg}"><div class="art"><img src="svg/{v}/{e["key"]}.svg"></div>'
                  f'<h3>{e["nome"]}</h3><p>{e["desc"]}</p></div>')
    return (f'<section class="pg" id="p{i+1}"><div class="cab"><div class="ey">Elementos · {i+1} de 3</div><h1>{t}</h1><p>{sub}</p></div>'
            f'<div class="grid" style="grid-template-columns:repeat({cols},1fr);grid-template-rows:repeat({rows},1fr)">{cards}</div>'
            f'<div class="pe">Lara Oraculista · Elementos</div></section>')
open(os.path.join(HERE, 'catalogo.html'), 'w').write('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Elementos v2</title>'
    '<link rel="stylesheet" href="../tipografia/fonts/fonts.css"><style>' + CSS + '</style></head><body>' + ''.join(page(i, *c) for i, c in enumerate(CATS)) + '</body></html>')
