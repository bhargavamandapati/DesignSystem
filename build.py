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
                   ('Roboto Condensed','roboto-condensed-latin-400-normal',400),('Roboto Condensed','roboto-condensed-latin-500-normal',500),
                   ('Roboto Mono','roboto-mono-latin-400-normal',400),('Roboto Mono','roboto-mono-latin-500-normal',500)]:
    b = base64.b64encode((R/'fonts'/(fn+'.woff2')).read_bytes()).decode()
    fonts += '@font-face{font-family:"%s";font-weight:%d;font-style:normal;font-display:swap;src:url(data:font/woff2;base64,%s) format("woff2")}\n' % (fam, w, b)
# ---- Android fonts: res/font/*.ttf + family XMLs + type.xml (single source -> repo files and in-page downloads) ----
import shutil
TYPE = json.loads((S/'type.json').read_text())
FONTS = [('roboto','Roboto','roboto',400,'regular'),('roboto','Roboto','roboto',500,'medium'),
         ('roboto_condensed','Roboto Condensed','roboto-condensed',400,'regular'),('roboto_condensed','Roboto Condensed','roboto-condensed',500,'medium'),
         ('roboto_mono','Roboto Mono','roboto-mono',400,'regular'),('roboto_mono','Roboto Mono','roboto-mono',500,'medium')]
fontfiles, fontxml = {}, {}
fdir = R/'android'/'res'/'font'; fdir.mkdir(parents=True, exist_ok=True)
for res, fam, src, w, nm in FONTS:
    ttf = (R/'fonts'/'ttf'/('%s-%d.ttf' % (src, w))).read_bytes()
    (fdir/('%s_%s.ttf' % (res, nm))).write_bytes(ttf)
    fontfiles['%s_%s' % (res, nm)] = {'family': fam, 'weight': w, 'b64': base64.b64encode(ttf).decode()}
for res in ('roboto','roboto_condensed','roboto_mono'):
    items = ''.join('    <font android:fontStyle="normal" android:fontWeight="%d" android:font="@font/%s_%s"/>\n' % (w, res, nm) for r2, f2, s2, w, nm in FONTS if r2 == res)
    fontxml['res/font/%s.xml' % res] = '<?xml version="1.0" encoding="utf-8"?>\n<font-family xmlns:android="http://schemas.android.com/apk/res/android">\n' + items + '</font-family>\n'
def sname(n): return n.replace(' ', '')
tx = '<?xml version="1.0" encoding="utf-8"?>\n<!-- Aurora AAOS IVI type scale. Normal = Roboto, Condensed = Roboto Condensed. sp sizes; letterSpacing in em. -->\n<resources>\n'
for cond in (False, True):
    fam = '@font/roboto_condensed' if cond else '@font/roboto'
    tx += '\n    <!-- %s -->\n' % ('Condensed' if cond else 'Normal')
    for name, cls, size, line, wt, ls, sample in TYPE:
        p = 'TextAppearance.Aurora.' + ('Condensed.' if cond else '') + sname(name)
        em = round(float(ls) / size, 4)
        tx += '    <style name="%s">\n        <item name="android:fontFamily">%s</item>\n        <item name="android:textSize">%dsp</item>\n        <item name="android:lineHeight">%dsp</item>\n        <item name="android:textFontWeight">%d</item>\n        <item name="android:letterSpacing">%s</item>\n    </style>\n' % (p, fam, size, line, wt, em)
tx += '\n    <!-- Tabular numerals helper -->\n    <style name="TextAppearance.Aurora.Tabular">\n        <item name="android:fontFeatureSettings">tnum</item>\n    </style>\n</resources>\n'
fontxml['res/values/type.xml'] = tx
for k, v in fontxml.items():
    f = R/'android'/k; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(v)
content = ''.join((S/p).read_text() for p in ('part1.html','part2.html','part4.html','part3.html'))
html = (S/'template.html').read_text()
html = (html.replace('/*FONTS*/', fonts).replace('/*TOKENS*/', css_tok).replace('/*STYLES*/', (S/'styles.css').read_text())
            .replace('<!--CONTENT-->', content).replace('/*JSON*/', json.dumps(tok)).replace('/*FONTFILES*/', json.dumps(fontfiles)).replace('/*FONTXML*/', json.dumps(fontxml)).replace('/*ICONS*/', (S/'icons.json').read_text())
            .replace('/*JS*/', (S/'app.js').read_text().replace('/*SCREENS*/', (S/'screens.js').read_text()).replace('/*ICONS_UI*/', (S/'icons.js').read_text()).replace('/*SPECS*/', (S/'specs.js').read_text()).replace('/*AUDIT*/', (S/'audit.js').read_text()).replace('/*TYPE*/', json.dumps(TYPE))))
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
