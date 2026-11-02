#!/usr/bin/env python3
"""Builds the self-contained, offline index.html from src/. Fonts are inlined as base64 WOFF2."""
import base64, json, re, pathlib
R = pathlib.Path(__file__).parent; S = R/'src'
def kebab(s): return re.sub(r'[A-Z]', lambda m: '-'+m.group(0).lower(), s)
tok = json.loads((S/'tokens.json').read_text())
css_tok = ''.join(':root[data-theme="%s"]{color-scheme:%s;%s}\n' % (m, 'dark' if m=='night' else 'light',
          ''.join('--c-%s:%s;' % (kebab(k), v) for k, v in tok[m].items())) for m in ('night','day'))
css_tok = css_tok.replace(':root[data-theme="night"]', ':root,:root[data-theme="night"]')
fonts = ''
for fam, fn, w in [('Roboto','roboto-latin-400-normal',400),('Roboto','roboto-latin-500-normal',500),
                   ('Roboto Mono','roboto-mono-latin-400-normal',400),('Roboto Mono','roboto-mono-latin-500-normal',500)]:
    b = base64.b64encode((R/'fonts'/(fn+'.woff2')).read_bytes()).decode()
    fonts += '@font-face{font-family:"%s";font-weight:%d;font-style:normal;font-display:swap;src:url(data:font/woff2;base64,%s) format("woff2")}\n' % (fam, w, b)
content = ''.join((S/p).read_text() for p in ('part1.html','part2.html','part3.html'))
html = (S/'template.html').read_text()
html = (html.replace('/*FONTS*/', fonts).replace('/*TOKENS*/', css_tok).replace('/*STYLES*/', (S/'styles.css').read_text())
            .replace('<!--CONTENT-->', content).replace('/*JSON*/', json.dumps(tok)).replace('/*JS*/', (S/'app.js').read_text()))
(R/'index.html').write_text(html)
print('index.html', len(html)//1024, 'KB')
