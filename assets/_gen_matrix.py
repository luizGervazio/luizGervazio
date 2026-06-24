# -*- coding: utf-8 -*-
# Gera um banner "Matrix digital rain" com o avatar (gato) emergindo no meio.
# SVG autocontido (avatar embutido em base64) + animacao CSS -> anima no GitHub.
import base64, random, os

random.seed(7)

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 760, 300

# avatar embutido (sem dependencia externa, requisito do SVG-as-img no GitHub)
with open(os.path.join(HERE, "_avatar_src.png"), "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")
data_uri = "data:image/jpeg;base64," + b64

# conjunto de caracteres estilo Matrix (katakana + digitos + simbolos)
glyphs = list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモ"
              "ヤユヨラリルレロワン0123456789:.=*+<>|")

COL_STEP = 16
N = W // COL_STEP
LINE_H = 18

cols = []
for i in range(N):
    x = 6 + i * COL_STEP
    length = random.randint(16, 30)
    chars = "".join(random.choice(glyphs) for _ in range(length))
    dur = round(random.uniform(4.5, 9.5), 2)
    delay = round(-random.uniform(0, 9.5), 2)
    cols.append((x, chars, dur, delay, length))

def tspans(chars, x):
    out = []
    for j, ch in enumerate(chars):
        dy = 0 if j == 0 else LINE_H
        ch = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}.get(ch, ch)
        out.append(f'<tspan x="{x}" dy="{dy}">{ch}</tspan>')
    return "".join(out)

# OBS: o X fica no <text> (nao no <g>), pois a animacao CSS usa transform e
# sobrescreveria um translate(x,0) do grupo -> colunas empilhariam na esquerda.
rain = []
for (x, chars, dur, delay, length) in cols:
    style = f"animation:fall {dur}s linear infinite;animation-delay:{delay}s"
    rain.append(
        f'<g style="{style}">'
        f'<text y="0" fill="url(#stream)">{tspans(chars, x)}</text></g>'
    )
rain_svg = "\n      ".join(rain)

# algumas colunas claras na frente do gato (integra a chuva ao rosto)
front = []
for i in range(0, N, 3):
    x = 6 + i * COL_STEP
    chars = "".join(random.choice(glyphs) for _ in range(20))
    dur = round(random.uniform(5, 8), 2)
    delay = round(-random.uniform(0, 8), 2)
    style = f"animation:fall {dur}s linear infinite;animation-delay:{delay}s"
    front.append(
        f'<g style="{style}">'
        f'<text y="0" fill="url(#stream)">{tspans(chars, x)}</text></g>'
    )
front_svg = "\n      ".join(front)

CAT = 250
cx = (W - CAT) / 2
cy = (H - CAT) / 2 + 6

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="'Courier New',monospace" font-size="15">
  <defs>
    <linearGradient id="stream" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#00ff66" stop-opacity="0"/>
      <stop offset="0.55" stop-color="#13d65a" stop-opacity="0.7"/>
      <stop offset="0.88" stop-color="#3bff7a" stop-opacity="1"/>
      <stop offset="1" stop-color="#ccffcc" stop-opacity="1"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#00ff66" stop-opacity="0.55"/>
      <stop offset="0.6" stop-color="#00ff66" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#00ff66" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vig" cx="0.5" cy="0.5" r="0.75">
      <stop offset="0.55" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.85"/>
    </radialGradient>
    <!-- transforma o avatar num "fantasma" verde: brilho proporcional a luminancia -->
    <filter id="greenize" x="-10%" y="-10%" width="120%" height="120%">
      <feColorMatrix type="matrix" values="0 0 0 0 0
                                            0.55 0.95 0.2 0 0
                                            0.12 0.22 0.05 0 0
                                            0.5 0.9 0.18 0 0"/>
      <feComponentTransfer><feFuncA type="gamma" amplitude="1.5" exponent="1.3" offset="0"/></feComponentTransfer>
      <feGaussianBlur stdDeviation="0.4"/>
    </filter>
    <clipPath id="frame"><rect x="0" y="0" width="{W}" height="{H}" rx="14"/></clipPath>
    <style>
      @keyframes fall {{ 0%{{transform:translateY(-480px)}} 100%{{transform:translateY({H}px)}} }}
      @keyframes breathe {{ 0%,100%{{opacity:.18}} 45%,65%{{opacity:.92}} }}
      @keyframes flick {{ 0%,100%{{opacity:.92}} 50%{{opacity:.7}} 53%{{opacity:.95}} }}
      .cat {{ animation: breathe 7s ease-in-out infinite; }}
      .catf {{ animation: flick 2.6s steps(1) infinite; }}
    </style>
  </defs>

  <g clip-path="url(#frame)">
    <rect x="0" y="0" width="{W}" height="{H}" fill="#000600"/>

    <!-- chuva de fundo -->
    <g opacity="0.95">
      {rain_svg}
    </g>

    <!-- brilho + gato emergindo -->
    <ellipse cx="{W/2}" cy="{H/2}" rx="170" ry="150" fill="url(#glow)"/>
    <g class="cat">
      <g class="catf">
        <image href="{data_uri}" x="{cx}" y="{cy}" width="{CAT}" height="{CAT}" filter="url(#greenize)"/>
      </g>
    </g>

    <!-- chuva na frente (baixa opacidade) -->
    <g opacity="0.35">
      {front_svg}
    </g>

    <!-- vinheta -->
    <rect x="0" y="0" width="{W}" height="{H}" fill="url(#vig)"/>
    <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#0a3" stroke-opacity="0.4"/>
  </g>
</svg>
'''

out = os.path.join(HERE, "matrix-cat.svg")
with open(out, "w", encoding="utf-8") as f:
    f.write(svg)
print("ok ->", out, len(svg), "bytes")
