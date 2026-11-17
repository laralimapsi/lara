# Gera tipografia.html com as 3 opções de combinação tipográfica
import os
HERE=os.path.dirname(os.path.abspath(__file__))
STAR='''<path d="M0-22 L2.2-4.2 L15.6-15.6 L4.2-2.2 L22 0 L4.2 2.2 L15.6 15.6 L2.2 4.2 L0 22 L-2.2 4.2 L-15.6 15.6 L-4.2 2.2 L-22 0 L-4.2-2.2 L-15.6-15.6 L-2.2-4.2Z"/><path d="M0-30 L1.1-9 L0 0 L-1.1-9Z M0 30 L1.1 9 L0 0 L-1.1 9Z M-30 0 L-9 1.1 L0 0 L-9-1.1Z M30 0 L9 1.1 L0 0 L9-1.1Z"/>'''
CHECK='<svg class="ck" viewBox="0 0 20 20"><path d="M3 10.5 L8 15 L17 4" fill="none" stroke="url(#{g}l)" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

OPTS=[
 dict(id='t1',num='1',nome='Clássico Místico',insp='Inspirada no título “AURA” do seu moodboard: letras de inscrição, elegantes e atemporais.',
      modo='Modo roxo',bg='radial-gradient(circle at 50% 28%,#4A2C51,#3B2340 55%,#29172D)',fg='#D6C2AA',sub_fg='#D6C2AA',g='m',
      nome_css="font-family:'Cinzel';font-weight:400;letter-spacing:.04em",
      title_html='Caminhos<br>do Amor', title_css="font-family:'Cinzel';font-weight:400;font-size:47px;line-height:1.08;letter-spacing:.05em;text-transform:uppercase",
      sub_css="font-family:'Cormorant Garamond';font-style:italic;font-weight:500;font-size:25px;line-height:1.22",
      lab_css="font-family:'Cinzel';font-weight:600;font-size:12.5px;letter-spacing:.22em",
      body_css="font-family:'EB Garamond';font-weight:400;font-size:18.5px;line-height:1.38",
      specs=[('Título','Cinzel','Regular 400 · CAIXA ALTA · espaçamento +5%',"font-family:'Cinzel';font-weight:400;font-size:46px;letter-spacing:.04em",'AURA'),
             ('Subtítulo','Cormorant Garamond','Itálico Medium 500',"font-family:'Cormorant Garamond';font-style:italic;font-weight:500;font-size:44px",'Destino'),
             ('Texto','EB Garamond','Regular 400 · rótulos em Cinzel SemiBold espaçado',"font-family:'EB Garamond';font-size:40px",'Leitura')],
      nota='Clima solene e místico, como capa de livro antigo. Brilha nos modos escuros.'),
 dict(id='t2',num='2',nome='Editorial Elegante',insp='Continuação da arte aprovada “Caminhos do Amor”: serifa fina e de alto contraste, leitura confortável.',
      modo='Modo claro',bg='radial-gradient(circle at 50% 28%,#E9DCCB,#D6C2AA 70%,#C9B193)',fg='#3B2340',sub_fg='#11281A',g='v',
      nome_css="font-family:'Newsreader';font-variation-settings:'opsz' 72;font-weight:340;letter-spacing:-.015em",
      title_html='Caminhos<br>do Amor', title_css="font-family:'Newsreader';font-variation-settings:'opsz' 72;font-weight:340;font-size:62px;line-height:.92;letter-spacing:-.025em",
      sub_css="font-family:'Noto Serif';font-style:italic;font-weight:400;font-size:19px;line-height:1.3;letter-spacing:.01em",
      lab_css="font-family:'Noto Serif';font-weight:500;font-size:12.5px;letter-spacing:.24em",
      body_css="font-family:'Noto Serif';font-weight:400;font-size:15.5px;line-height:1.45",
      specs=[('Título','Newsreader (Display)','Light 340 · espaçamento −2%',"font-family:'Newsreader';font-variation-settings:'opsz' 72;font-weight:340;font-size:50px;letter-spacing:-.02em",'Amor'),
             ('Subtítulo','Noto Serif','Itálico Regular 400',"font-family:'Noto Serif';font-style:italic;font-size:40px",'Destino'),
             ('Texto','Noto Serif','Regular 400 · rótulos em Medium 500 espaçado',"font-family:'Noto Serif';font-size:38px",'Leitura')],
      nota='Moderna, limpa e muito legível no celular. Ideal para o catálogo e textos mais longos.'),
 dict(id='t3',num='3',nome='Natureza Poética',insp='Inspirada no moodboard verde: palavra-destaque manuscrita, delicada, com serifa clássica ao redor.',
      modo='Modo verde',bg='radial-gradient(circle at 50% 28%,#1C3A27,#11281A 55%,#0A1A10)',fg='#D6C2AA',sub_fg='#D6C2AA',g='m',
      nome_css="font-family:'Cormorant Garamond';font-weight:400",
      title_html='<span class="sc">Caminhos do</span><span class="scr">Amor</span>', title_css="font-family:'Cormorant Garamond';font-weight:500;font-size:28px;letter-spacing:.3em;text-transform:uppercase;line-height:1",
      sub_css="font-family:'Cormorant Garamond';font-style:italic;font-weight:500;font-size:23px;line-height:1.25",
      lab_css="font-family:'Cormorant Garamond';font-weight:700;font-size:13px;letter-spacing:.26em",
      body_css="font-family:'Lora';font-weight:400;font-size:15.5px;line-height:1.5",
      specs=[('Título','Cormorant Garamond + Waterfall','CAIXA ALTA espaçada (+30%) + palavra-destaque manuscrita',"font-family:'Waterfall';font-size:64px;line-height:.9",'Amor'),
             ('Subtítulo','Cormorant Garamond','Itálico Medium 500',"font-family:'Cormorant Garamond';font-style:italic;font-weight:500;font-size:44px",'Destino'),
             ('Texto','Lora','Regular 400 · rótulos em Cormorant Bold espaçado',"font-family:'Lora';font-size:36px",'Leitura')],
      nota='Romântica e acolhedora. Use a manuscrita só em 1 palavra por arte, nunca em textos longos.'),
]

CSS='''
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;background:#111}
.pg{position:relative;width:1080px;height:1350px;overflow:hidden;color:#3B2340;font-family:'Noto Serif',serif;
 background:radial-gradient(ellipse 75% 45% at 50% 20%,rgba(244,234,220,.9),transparent 75%),linear-gradient(#DECDB8,#D3BEA4)}
.cab{position:absolute;top:58px;left:80px;right:80px;text-align:center}
.cab small{font-size:13px;letter-spacing:.26em;font-weight:500;text-transform:uppercase;color:#11281A}
.cab h1{font-size:64px;font-weight:400;margin-top:14px;color:#3B2340;line-height:1}
.cab p{font-style:italic;font-size:17px;margin-top:14px;color:#4A3448;line-height:1.4}
.orn{display:flex;align-items:center;justify-content:center;gap:12px;margin-top:16px}
.orn i{display:block;width:110px;height:1.2px}
.orn i:first-child{background:linear-gradient(90deg,transparent,#85692B)} .orn i:last-child{background:linear-gradient(90deg,#85692B,transparent)}
.corpo{position:absolute;top:318px;left:72px;right:72px;display:grid;grid-template-columns:500px 1fr;gap:40px}
.mock{width:500px;height:625px;border-radius:14px;overflow:hidden;position:relative;box-shadow:0 14px 34px rgba(40,20,30,.28);text-align:center;padding:46px 40px 0}
.mock .tag{position:absolute;top:14px;left:16px;font-size:10px;letter-spacing:.2em;text-transform:uppercase;opacity:.65;font-family:'Noto Serif'}
.mock .t{margin-top:12px}
.mock .t .sc{display:block}
.mock .t .scr{display:block;font-family:'Waterfall';font-size:96px;letter-spacing:0;text-transform:none;line-height:.8;margin-top:6px;font-weight:400}
.mock .s{margin:14px auto 0;max-width:380px}
.mock .div{display:flex;align-items:center;justify-content:center;gap:10px;margin:20px 0 16px}
.mock .div i{display:block;height:1.2px;width:70px}
.mock .lab{display:flex;align-items:center;gap:12px;text-transform:uppercase}
.mock .lab i{flex:1;height:1px}
.mock ul{list-style:none;text-align:left;margin-top:14px}
.mock li{display:grid;grid-template-columns:22px 1fr;gap:8px;margin-bottom:9px}
.ck{width:18px;height:18px;margin-top:3px}
.mock .rod{position:absolute;bottom:30px;left:0;right:0;display:flex;justify-content:center}
.specs .bl{padding:16px 0 18px;border-bottom:1px solid rgba(59,35,64,.2)}
.specs .bl:first-child{padding-top:0}
.specs .k{font-size:11.5px;letter-spacing:.24em;text-transform:uppercase;font-weight:500;color:#11281A}
.specs .ex{color:#3B2340;margin:8px 0 6px;line-height:1.05}
.specs .fn{font-size:18px;font-weight:600;color:#3B2340}
.specs .ds{font-size:13.5px;color:#5A4458;margin-top:3px;line-height:1.35}
.specs .nota{margin-top:18px;font-style:italic;font-size:15px;line-height:1.45;color:#3B2340}
.specs .modo{display:inline-block;margin-top:14px;font-size:11px;letter-spacing:.2em;text-transform:uppercase;padding:6px 12px;border-radius:20px;border:1px solid rgba(59,35,64,.35)}
.pe{position:absolute;bottom:40px;left:0;right:0;text-align:center;font-size:12px;letter-spacing:.26em;color:rgba(59,35,64,.55);text-transform:uppercase}
.alf{position:absolute;left:72px;right:72px;top:1000px;padding-top:22px;border-top:1px solid rgba(59,35,64,.2)}
.alf .row{display:flex;justify-content:space-between;align-items:baseline;gap:20px;margin-bottom:10px}
.alf .row small{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#11281A;width:110px;flex:none}
.alf .row span{flex:1;color:#3B2340;white-space:nowrap;overflow:hidden}
'''

def page(o):
    G='url(#g'+o['g']+')'
    lc = '#B8924F' if o['g']=='m' else '#85692B'
    star=f'<svg width="{{w}}" height="{{w}}" viewBox="-31 -31 62 62"><g fill="{G}">{STAR}</g></svg>'
    items=['Descobrir como tende a ser sua vida amorosa nos próximos seis meses.',
           'Investigar se existem caminhos para iniciar um relacionamento sério.',
           'Entender o que você pode fazer para construir uma relação saudável.']
    lis=''.join(f'<li>{CHECK.format(g="g"+o["g"])}<span>{t}</span></li>' for t in items)
    specs=''.join(f'<div class="bl"><div class="k">{k}</div><div class="ex" style="{css}">{ex}</div><div class="fn">{fn}</div><div class="ds">{ds}</div></div>' for k,fn,ds,css,ex in o['specs'])
    tfont=o['specs'][0][3].split(';font-size')[0]
    alf=f'''<div class="alf">
      <div class="row"><small>Título</small><span style="{o['title_css'].split(';font-size')[0]};font-size:34px{';text-transform:uppercase;letter-spacing:.08em' if o['id']=='t1' else ''}">{'Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm' if o['id']!='t1' else 'ABCDEFGHIJKLMNOPQRSTUV'}</span></div>
      {'<div class="row"><small>Destaque</small><span style="font-family:Waterfall;font-size:46px">Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn</span></div>' if o['id']=='t3' else ''}
      <div class="row"><small>Subtítulo</small><span style="{o['sub_css'].split(';font-size')[0]};font-size:28px">Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp</span></div>
      <div class="row"><small>Texto</small><span style="{o['body_css'].split(';font-size')[0]};font-size:22px">Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss 0123456789</span></div>
    </div>'''
    return f'''
<section class="pg" id="{o['id']}">
  <div class="cab"><small>Tipografia · Opção {o['num']} de 3</small>
    <h1 style="{o['nome_css']}">{o['nome']}</h1>
    <p>{o['insp']}</p>
    <div class="orn"><i></i><svg width="18" height="18" viewBox="-31 -31 62 62"><g fill="url(#gv)">{STAR}</g></svg><i></i></div></div>
  <div class="corpo">
    <div class="mock" style="background:{o['bg']};color:{o['fg']}">
      <div class="tag">{o['modo']}</div>
      {star.format(w=34)}
      <div class="t" style="{o['title_css']}">{o['title_html']}</div>
      <div class="s" style="{o['sub_css']};color:{o['sub_fg']}">O que os próximos seis meses reservam para sua vida amorosa?</div>
      <div class="div"><i style="background:linear-gradient(90deg,transparent,{lc})"></i>{star.format(w=16)}<i style="background:linear-gradient(90deg,{lc},transparent)"></i></div>
      <div class="lab" style="{o['lab_css']}"><i style="background:linear-gradient(90deg,transparent,{lc})"></i>Leitura indicada para:<i style="background:linear-gradient(90deg,{lc},transparent)"></i></div>
      <ul style="{o['body_css']}">{lis}</ul>
      <div class="rod">{star.format(w=22)}</div>
    </div>
    <div class="specs">{specs}<div class="nota">{o['nota']}</div><div class="modo">Exemplo aplicado: {o['modo'].lower()}</div></div>
  </div>
  {alf}
  <div class="pe">Lara Oraculista · Tipografia</div>
</section>'''

html=f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Tipografia — 3 opções · Lara Oraculista</title>
<link rel="stylesheet" href="fonts/fonts.css"><link rel="stylesheet" href="../../artes/como-funcionam-as-leituras/fonts2/fonts.css">
<style>{CSS}</style></head><body>
<svg width="0" height="0" style="position:absolute"><defs>
<linearGradient id="gm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9E7B3E"/><stop offset=".5" stop-color="#CDAE6E"/><stop offset="1" stop-color="#9E7B3E"/></linearGradient>
<linearGradient id="gml" x1="0" y1="0" x2="1" y2="1" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#B8924F"/><stop offset="1" stop-color="#CDAE6E"/></linearGradient>
<linearGradient id="gv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6E5523"/><stop offset=".5" stop-color="#A68844"/><stop offset="1" stop-color="#6E5523"/></linearGradient>
<linearGradient id="gvl" x1="0" y1="0" x2="1" y2="1" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#85692B"/><stop offset="1" stop-color="#85692B"/></linearGradient>
</defs></svg>
{''.join(page(o) for o in OPTS)}
</body></html>'''
open(os.path.join(HERE,'tipografia.html'),'w').write(html)
