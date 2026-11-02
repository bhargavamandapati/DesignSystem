#!/usr/bin/env python3
"""Builds the self-contained, offline index.html from src/. Fonts are inlined as base64 WOFF2."""
import base64, json, re, pathlib
R = pathlib.Path(__file__).parent; S = R/'src'
def kebab(s): return re.sub(r'[A-Z]', lambda m: '-'+m.group(0).lower(), s)
import subprocess, sys
subprocess.run([sys.executable, str(R/'tools'/'icons_src.py')], check=True)
tok = json.loads((S/'tokens.json').read_text())
css_tok = ''
for tid, t in tok['themes'].items():
    sel = ':root,:root[data-theme="%s"]' % tid if tid == 'aurora-night' else ':root[data-theme="%s"]' % tid
    css_tok += '%s{color-scheme:%s;%s}\n' % (sel, t['mode'], ''.join('--c-%s:%s;' % (kebab(k), v) for k, v in t['roles'].items()))
fonts = ''
for fam, fn, w in [('Roboto','roboto-latin-400-normal',400),('Roboto','roboto-latin-500-normal',500),
                   ('Roboto Mono','roboto-mono-latin-400-normal',400),('Roboto Mono','roboto-mono-latin-500-normal',500)]:
    b = base64.b64encode((R/'fonts'/(fn+'.woff2')).read_bytes()).decode()
    fonts += '@font-face{font-family:"%s";font-weight:%d;font-style:normal;font-display:swap;src:url(data:font/woff2;base64,%s) format("woff2")}\n' % (fam, w, b)
content = ''.join((S/p).read_text() for p in ('part1.html','part2.html','part4.html','part3.html'))
html = (S/'template.html').read_text()
html = (html.replace('/*FONTS*/', fonts).replace('/*TOKENS*/', css_tok).replace('/*STYLES*/', (S/'styles.css').read_text())
            .replace('<!--CONTENT-->', content).replace('/*JSON*/', json.dumps(tok)).replace('/*ICONS*/', (S/'icons.json').read_text())
            .replace('/*JS*/', (S/'app.js').read_text().replace('/*SCREENS*/', (S/'screens.js').read_text()).replace('/*ICONS_UI*/', (S/'icons.js').read_text()).replace('/*SPECS*/', (S/'specs.js').read_text())))
(R/'index.html').write_text(html)
print('index.html', len(html)//1024, 'KB')

# ---- Android colors.xml per theme -> android/res/ (same naming as the in-page export) ----
def snake(s): return kebab(s).replace('-', '_')
GROUPS = [('Primary / secondary / tertiary', ['primary','onPrimary','primaryContainer','onPrimaryContainer','secondary','onSecondary','secondaryContainer','onSecondaryContainer','tertiary','onTertiary','tertiaryContainer','onTertiaryContainer']),
 ('Status (error / success / warning)', ['error','onError','errorContainer','onErrorContainer','success','onSuccess','successContainer','onSuccessContainer','warning','onWarning','warningContainer','onWarningContainer']),
 ('Surface & background', ['background','onBackground','surface','onSurface','surfaceVariant','onSurfaceVariant','surfaceContainerLowest','surfaceContainerLow','surfaceContainer','surfaceContainerHigh','surfaceContainerHighest']),
 ('Outline & inverse', ['outline','outlineVariant','inverseSurface','inverseOnSurface','inversePrimary','scrim'])]
def colors_xml(tid, t):
    p = 'aurora' if tid in ('aurora-night','aurora-day') else 'aurora_' + snake(tid.replace('drive-',''))
    A = lambda h: '#FF' + h[1:].upper()
    where = 'res/values-night/colors.xml' if tid=='aurora-night' else 'res/values/colors.xml' if tid=='aurora-day' else 'res/values/colors_%s.xml' % snake(tid)
    o = '<?xml version="1.0" encoding="utf-8"?>\n<!--\n  Aurora AAOS IVI design system — %s (%s, %s)\n  %s\n  Place in: %s\n  Naming: %s_<role> (snake_case Material 3 roles) · %s_palette_<family>_<tone> (tonal palette)\n-->\n<resources>\n' % (t['name'], t['group'], t['mode'], t['desc'], where, p, p)
    for title, ks in GROUPS:
        o += '\n    <!-- %s -->\n' % title + '\n'.join('    <color name="%s_%s">%s</color>' % (p, snake(k), A(t['roles'][k])) for k in ks) + '\n'
    o += '\n    <!-- Tonal palettes -->\n'
    for fam, steps in t['tonal'].items():
        o += '\n'.join('    <color name="%s_palette_%s_%s">%s</color>' % (p, snake(fam.replace(' ','_')).lower(), tn, A(v)) for tn, v in steps.items()) + '\n'
    o += '\n    <!-- State layer opacities -->\n' + ''.join('    <item name="%s_state_%s" format="float" type="dimen">%s</item>\n' % (p, n, v) for n, v in [('hover','0.08'),('focus','0.12'),('pressed','0.12'),('dragged','0.16'),('disabled_content','0.38'),('disabled_container','0.12')]) + '</resources>\n'
    return where, o
for tid, t in tok['themes'].items():
    w, x = colors_xml(tid, t)
    f = R/'android'/w; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(x)
print('android colors written')
