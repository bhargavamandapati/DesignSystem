#!/usr/bin/env python3
"""Android UI kit generator: Compose + XML (layout, style, color state lists, drawable state selectors) per component,
plus theme files (attrs/themes/dimens/shapes) and AuroraTheme.kt. Returns {path: content} and {component: blocks}."""
import json, re

XMLNS = 'xmlns:android="http://schemas.android.com/apk/res/android"'
HDR = '<?xml version="1.0" encoding="utf-8"?>\n'

def sel(items, note=''):
    """items: list of (states:dict, color_attr_or_ref, alpha|None). Builds res/color selector."""
    o = HDR + ('<!-- %s -->\n' % note if note else '') + '<selector %s>\n' % XMLNS
    for st, col, a in items:
        attrs = ''.join(' android:state_%s="%s"' % (k, 'true' if v else 'false') for k, v in st.items())
        o += '    <item%s android:color="%s"%s/>\n' % (attrs, col, (' android:alpha="%s"' % a) if a else '')
    return o + '</selector>\n'

def dis(col, a):  # disabled item helper
    return ({'enabled': False}, col, a)

# ---------------------------------------------------------------- generic pill-shaped control (buttons, chips, tiles, segments)
def pill_files(key, container, content, layer, radius, stroke=None, elevated=False):
    """Returns dict of resource files for a rounded control with state-aware colors, ripple (state layer) and focus ring."""
    f = {}
    f['res/color/aurora_%s_container.xml' % key] = sel(container, '%s container: enabled / checked / disabled' % key)
    f['res/color/aurora_%s_content.xml' % key] = sel(content, '%s label + icon color' % key)
    f['res/color/aurora_%s_layer.xml' % key] = sel([
        ({'pressed': True}, layer, '0.12'), ({'focused': True}, layer, '0.12'),
        ({'hovered': True}, layer, '0.08'), ({}, '@android:color/transparent', None)],
        'state layer: pressed 12%, focused 12%, hovered 8%')
    if stroke:
        f['res/color/aurora_%s_stroke.xml' % key] = sel(stroke, '%s outline' % key)
    stroke_xml = ('\n        <stroke android:width="2dp" android:color="@color/aurora_%s_stroke"/>' % key) if stroke else ''
    shape = lambda body: '<shape android:shape="rectangle">\n%s\n    </shape>' % body
    fill = '        <solid android:color="@color/aurora_%s_container"/>\n        <corners android:radius="%sdp"/>%s' % (key, radius, stroke_xml)
    f['res/drawable/aurora_%s_shape.xml' % key] = HDR + '<!-- Focused: 6dp ring in theme focus color drawn inside the control (clip-safe). Default: filled shape. -->\n<selector %s>\n    <item android:state_focused="true">\n        <layer-list>\n            <item>\n                <shape android:shape="rectangle">\n                    <solid android:color="@android:color/transparent"/>\n                    <corners android:radius="%sdp"/>\n                    <stroke android:width="6dp" android:color="?attr/auroraColorFocusRing"/>\n                </shape>\n            </item>\n            <item android:left="6dp" android:top="6dp" android:right="6dp" android:bottom="6dp">\n                <shape android:shape="rectangle">\n%s\n                </shape>\n            </item>\n        </layer-list>\n    </item>\n    <item>\n        <shape android:shape="rectangle">\n%s\n        </shape>\n    </item>\n</selector>\n' % (XMLNS, radius, fill.replace('\n', '\n        '), fill.replace('\n', '\n    '))
    f['res/drawable/aurora_%s_background.xml' % key] = HDR + '<!-- Ripple = state layer (pressed/focused/hovered). Mask matches the %sdp corner radius. -->\n<ripple %s android:color="@color/aurora_%s_layer">\n    <item android:id="@android:id/mask">\n        <shape android:shape="rectangle">\n            <solid android:color="@android:color/white"/>\n            <corners android:radius="%sdp"/>\n        </shape>\n    </item>\n    <item android:drawable="@drawable/aurora_%s_shape"/>\n</ripple>\n' % (radius, XMLNS, key, radius, key)
    return f

BLOCK = lambda title, lang, files: {'title': title, 'lang': lang, 'files': files}

def join_files(d):  # for display: path header + content
    return '\n'.join(('<!-- ' if p.endswith('.xml') else '// ') + p + (' -->' if p.endswith('.xml') else '') + '\n' + c for p, c in d.items())

COMPONENTS = {}   # id -> dict(name, section, groups{compose,layout,style,colors,drawables: [paths]}, files{path: content})
def add(cid, name, section, compose, layout, style, res):
    files = {compose[0]: compose[1], layout[0]: layout[1], style[0]: style[1], **res}
    COMPONENTS[cid] = {'name': name, 'section': section, 'files': files,
        'groups': {'compose': [compose[0]], 'layout': [layout[0]], 'style': [style[0]],
                   'colors': [p for p in res if p.startswith('res/color/')], 'drawables': [p for p in res if p.startswith('res/drawable/')]}}

ON = lambda a: '?attr/' + a
# ================================================================ BUTTONS
def btn(cid, name, cls_parent, container, content, layer, stroke=None, extra_style='', compose_colors='', compose_border='', elevated=False):
    key = 'btn_' + cid.split('-')[1]
    res = pill_files(key, container, content, layer, 38, stroke)
    style = ('res/values/styles_%s.xml' % key, HDR + '<resources>\n    <style name="Widget.Aurora.Button.%s" parent="%s">\n        <item name="android:minHeight">76dp</item>\n        <item name="android:minWidth">120dp</item>\n        <item name="android:insetTop">0dp</item>\n        <item name="android:insetBottom">0dp</item>\n        <item name="android:paddingStart">40dp</item>\n        <item name="android:paddingEnd">40dp</item>\n        <item name="android:textAppearance">@style/TextAppearance.Aurora.LabelLarge</item>\n        <item name="iconSize">40dp</item>\n        <item name="iconPadding">12dp</item>\n        <item name="android:background">@drawable/aurora_%s_background</item>\n        <item name="backgroundTint">@null</item>\n        <item name="android:textColor">@color/aurora_%s_content</item>\n        <item name="iconTint">@color/aurora_%s_content</item>\n        <item name="android:focusable">true</item>\n%s    </style>\n</resources>\n' % (name.split()[0], cls_parent, key, key, key, extra_style))
    layout = ('res/layout/example_%s.xml' % key, HDR + '<LinearLayout %s xmlns:app="http://schemas.android.com/apk/res-auto"\n    android:layout_width="wrap_content" android:layout_height="wrap_content" android:orientation="horizontal">\n\n    <!-- Enabled / pressed / focused / hovered states are driven by the drawable + color state lists -->\n    <com.google.android.material.button.MaterialButton\n        android:id="@+id/button"\n        style="@style/Widget.Aurora.Button.%s"\n        android:layout_width="wrap_content" android:layout_height="wrap_content"\n        android:text="Navigate"\n        app:icon="@drawable/ic_nav" />\n\n    <!-- Disabled state -->\n    <com.google.android.material.button.MaterialButton\n        style="@style/Widget.Aurora.Button.%s"\n        android:layout_width="wrap_content" android:layout_height="wrap_content"\n        android:enabled="false" android:text="Disabled" />\n</LinearLayout>\n' % (XMLNS, name.split()[0], name.split()[0]))
    fname = 'Aurora' + name.split()[0] + 'Button'
    colors = compose_colors or 'containerColor = cs.primary, contentColor = cs.onPrimary'
    comp = ('compose/%s.kt' % fname, '''package com.aurora.ivi.ui.components

import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsFocusedAsState
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.shape.RoundedCornerShape
import com.aurora.ivi.ui.*

/** %(name)s — 76dp high, min 120dp, radius 38dp (full), Label Large 28sp. States: enabled, hovered 8%%, focused 12%% + 6dp ring, pressed 12%%, disabled 12%%/38%%. */
@Composable
fun %(fn)s(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    icon: ImageVector? = null,
) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    val shape = RoundedCornerShape(38.dp)
    %(btn)s(
        onClick = onClick,
        modifier = modifier
            .heightIn(min = 76.dp).widthIn(min = 120.dp)
            .auroraFocusRing(focused, 38.dp),
        enabled = enabled,
        shape = shape,
        colors = %(cols)s,
%(border)s        contentPadding = PaddingValues(start = if (icon != null) 32.dp else 40.dp, end = 40.dp),
        interactionSource = interaction,
    ) {
        if (icon != null) { Icon(icon, null, Modifier.size(40.dp)); Spacer(Modifier.width(12.dp)) }
        Text(text, style = AuroraType.labelLarge)
    }
}
''' % dict(name=name, fn=fname, btn={'btn-filled': 'Button', 'btn-tonal': 'FilledTonalButton', 'btn-outlined': 'OutlinedButton', 'btn-text': 'TextButton', 'btn-elevated': 'ElevatedButton', 'btn-danger': 'Button'}[cid],
        cols={'btn-filled': 'ButtonDefaults.buttonColors(containerColor = cs.primary, contentColor = cs.onPrimary, disabledContainerColor = cs.onSurface.copy(alpha = 0.12f), disabledContentColor = cs.onSurface.copy(alpha = 0.38f))',
              'btn-tonal': 'ButtonDefaults.filledTonalButtonColors(containerColor = cs.secondaryContainer, contentColor = cs.onSecondaryContainer, disabledContainerColor = cs.onSurface.copy(alpha = 0.12f), disabledContentColor = cs.onSurface.copy(alpha = 0.38f))',
              'btn-outlined': 'ButtonDefaults.outlinedButtonColors(contentColor = cs.primary, disabledContentColor = cs.onSurface.copy(alpha = 0.38f))',
              'btn-text': 'ButtonDefaults.textButtonColors(contentColor = cs.primary, disabledContentColor = cs.onSurface.copy(alpha = 0.38f))',
              'btn-elevated': 'ButtonDefaults.elevatedButtonColors(containerColor = cs.surfaceContainerLow, contentColor = cs.primary, disabledContainerColor = cs.onSurface.copy(alpha = 0.12f), disabledContentColor = cs.onSurface.copy(alpha = 0.38f))',
              'btn-danger': 'ButtonDefaults.buttonColors(containerColor = cs.error, contentColor = cs.onError, disabledContainerColor = cs.onSurface.copy(alpha = 0.12f), disabledContentColor = cs.onSurface.copy(alpha = 0.38f))'}[cid],
        border='        border = BorderStroke(2.dp, if (enabled) cs.outline else cs.onSurface.copy(alpha = 0.12f)),\n' if cid == 'btn-outlined' else ''))
    if cid == 'btn-outlined':
        comp = (comp[0], comp[1].replace('import androidx.compose.foundation.interaction.MutableInteractionSource', 'import androidx.compose.foundation.BorderStroke\nimport androidx.compose.foundation.interaction.MutableInteractionSource'))
    add(cid, name, 'buttons', comp, layout, style, res)

btn('btn-filled', 'Filled button', 'Widget.Material3.Button', [dis('?attr/colorOnSurface', '0.12'), ({}, '?attr/colorPrimary', None)], [dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorOnPrimary', None)], '?attr/colorOnPrimary')
btn('btn-tonal', 'Tonal button', 'Widget.Material3.Button.TonalButton', [dis('?attr/colorOnSurface', '0.12'), ({}, '?attr/colorSecondaryContainer', None)], [dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorOnSecondaryContainer', None)], '?attr/colorOnSecondaryContainer')
btn('btn-outlined', 'Outlined button', 'Widget.Material3.Button.OutlinedButton', [({}, '@android:color/transparent', None)], [dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorPrimary', None)], '?attr/colorPrimary', stroke=[dis('?attr/colorOnSurface', '0.12'), ({}, '?attr/colorOutline', None)])
btn('btn-text', 'Text button', 'Widget.Material3.Button.TextButton', [({}, '@android:color/transparent', None)], [dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorPrimary', None)], '?attr/colorPrimary')
btn('btn-elevated', 'Elevated button', 'Widget.Material3.Button.ElevatedButton', [dis('?attr/colorOnSurface', '0.12'), ({}, '?attr/colorSurfaceContainerLow', None)], [dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorPrimary', None)], '?attr/colorPrimary', extra_style='        <item name="android:elevation">2dp</item>\n')
btn('btn-danger', 'Destructive button', 'Widget.Material3.Button', [dis('?attr/colorOnSurface', '0.12'), ({}, '?attr/colorError', None)], [dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorOnError', None)], '?attr/colorOnError')

# ---------------------------------------------------------------- icon button + FAB
def icon_btn(var, container, content, layer, stroke=None, checked=False):
    key = 'iconbtn_' + var
    res = pill_files(key, container, content, layer, 38, stroke)
    return key, res
ICON_VARS = {
 'standard': ([({}, '@android:color/transparent', None)], [dis('?attr/colorOnSurface', '0.38'), ({'checked': True}, '?attr/colorOnPrimaryContainer', None), ({}, '?attr/colorOnSurfaceVariant', None)], '?attr/colorOnSurfaceVariant', None),
 'filled': ([dis('?attr/colorOnSurface', '0.12'), ({}, '?attr/colorPrimary', None)], [dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorOnPrimary', None)], '?attr/colorOnPrimary', None),
 'tonal': ([dis('?attr/colorOnSurface', '0.12'), ({}, '?attr/colorSecondaryContainer', None)], [dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorOnSecondaryContainer', None)], '?attr/colorOnSecondaryContainer', None),
 'outlined': ([({}, '@android:color/transparent', None)], [dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorOnSurfaceVariant', None)], '?attr/colorOnSurfaceVariant', [dis('?attr/colorOnSurface', '0.12'), ({}, '?attr/colorOutline', None)]),
 'toggle': ([dis('?attr/colorOnSurface', '0.12'), ({'checked': True}, '?attr/colorPrimaryContainer', None), ({}, '@android:color/transparent', None)], [dis('?attr/colorOnSurface', '0.38'), ({'checked': True}, '?attr/colorOnPrimaryContainer', None), ({}, '?attr/colorOnSurfaceVariant', None)], '?attr/colorOnSurface', None)}
res = {}
for v, (c, o, l, s) in ICON_VARS.items():
    res.update(pill_files('iconbtn_' + v, c, o, l, 38, s))
styles = HDR + '<resources>\n    <!-- 76 x 76dp, glyph 40dp, circular. Variants: standard, filled, tonal, outlined, toggle (checkable) -->\n'
for v in ICON_VARS:
    styles += '    <style name="Widget.Aurora.IconButton.%s" parent="Widget.Material3.Button.IconButton">\n        <item name="android:minWidth">76dp</item>\n        <item name="android:minHeight">76dp</item>\n        <item name="android:layout_width">76dp</item>\n        <item name="android:layout_height">76dp</item>\n        <item name="iconSize">40dp</item>\n        <item name="iconPadding">0dp</item>\n        <item name="android:insetTop">0dp</item>\n        <item name="android:insetBottom">0dp</item>\n        <item name="android:background">@drawable/aurora_iconbtn_%s_background</item>\n        <item name="backgroundTint">@null</item>\n        <item name="iconTint">@color/aurora_iconbtn_%s_content</item>\n%s    </style>\n' % (v.capitalize(), v, v, '        <item name="android:checkable">true</item>\n' if v == 'toggle' else '')
styles += '</resources>\n'
add('icon-button', 'Icon button', 'buttons',
 ('compose/AuroraIconButton.kt', '''package com.aurora.ivi.ui.components

import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsFocusedAsState
import androidx.compose.foundation.layout.size
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import com.aurora.ivi.ui.*

enum class AuroraIconButtonStyle { Standard, Filled, Tonal, Outlined }

/** 76x76dp hit area, 40dp glyph. States: hovered 8%, focused 12% + 6dp ring, pressed 12%, disabled 38%. */
@Composable
fun AuroraIconButton(
    icon: ImageVector, contentDescription: String, onClick: () -> Unit,
    modifier: Modifier = Modifier, style: AuroraIconButtonStyle = AuroraIconButtonStyle.Standard, enabled: Boolean = true,
) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    val m = modifier.size(76.dp).auroraFocusRing(focused, 38.dp)
    when (style) {
        AuroraIconButtonStyle.Standard -> IconButton(onClick, m, enabled, interactionSource = interaction,
            colors = IconButtonDefaults.iconButtonColors(contentColor = cs.onSurfaceVariant, disabledContentColor = cs.onSurface.copy(0.38f))) { Icon(icon, contentDescription, Modifier.size(40.dp)) }
        AuroraIconButtonStyle.Filled -> FilledIconButton(onClick, m, enabled, interactionSource = interaction,
            colors = IconButtonDefaults.filledIconButtonColors(cs.primary, cs.onPrimary, cs.onSurface.copy(0.12f), cs.onSurface.copy(0.38f))) { Icon(icon, contentDescription, Modifier.size(40.dp)) }
        AuroraIconButtonStyle.Tonal -> FilledTonalIconButton(onClick, m, enabled, interactionSource = interaction,
            colors = IconButtonDefaults.filledTonalIconButtonColors(cs.secondaryContainer, cs.onSecondaryContainer, cs.onSurface.copy(0.12f), cs.onSurface.copy(0.38f))) { Icon(icon, contentDescription, Modifier.size(40.dp)) }
        AuroraIconButtonStyle.Outlined -> OutlinedIconButton(onClick, m, enabled, interactionSource = interaction,
            border = androidx.compose.foundation.BorderStroke(2.dp, if (enabled) cs.outline else cs.onSurface.copy(0.12f)),
            colors = IconButtonDefaults.outlinedIconButtonColors(contentColor = cs.onSurfaceVariant, disabledContentColor = cs.onSurface.copy(0.38f))) { Icon(icon, contentDescription, Modifier.size(40.dp)) }
    }
}

/** Toggle (e.g. HVAC seat heat): checked = primaryContainer / onPrimaryContainer. */
@Composable
fun AuroraToggleIconButton(checked: Boolean, onCheckedChange: (Boolean) -> Unit, icon: ImageVector, contentDescription: String, modifier: Modifier = Modifier, enabled: Boolean = true) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    FilledIconToggleButton(checked, onCheckedChange, modifier.size(76.dp).auroraFocusRing(focused, 38.dp), enabled, interactionSource = interaction,
        colors = IconButtonDefaults.filledIconToggleButtonColors(
            containerColor = androidx.compose.ui.graphics.Color.Transparent, contentColor = cs.onSurfaceVariant,
            checkedContainerColor = cs.primaryContainer, checkedContentColor = cs.onPrimaryContainer,
            disabledContainerColor = cs.onSurface.copy(0.12f), disabledContentColor = cs.onSurface.copy(0.38f))) { Icon(icon, contentDescription, Modifier.size(40.dp)) }
}
'''),
 ('res/layout/example_icon_buttons.xml', HDR + '<LinearLayout %s xmlns:app="http://schemas.android.com/apk/res-auto"\n    android:layout_width="wrap_content" android:layout_height="wrap_content" android:orientation="horizontal">\n    <com.google.android.material.button.MaterialButton style="@style/Widget.Aurora.IconButton.Standard" app:icon="@drawable/ic_menu" android:contentDescription="Menu"/>\n    <com.google.android.material.button.MaterialButton style="@style/Widget.Aurora.IconButton.Filled"   app:icon="@drawable/ic_mic"  android:contentDescription="Voice"/>\n    <com.google.android.material.button.MaterialButton style="@style/Widget.Aurora.IconButton.Tonal"    app:icon="@drawable/ic_vol" android:contentDescription="Volume"/>\n    <com.google.android.material.button.MaterialButton style="@style/Widget.Aurora.IconButton.Outlined" app:icon="@drawable/ic_search" android:contentDescription="Search"/>\n    <!-- Toggle: checked = primaryContainer -->\n    <com.google.android.material.button.MaterialButton style="@style/Widget.Aurora.IconButton.Toggle"   app:icon="@drawable/ic_seat_heat" android:contentDescription="Seat heat"/>\n    <com.google.android.material.button.MaterialButton style="@style/Widget.Aurora.IconButton.Filled"   app:icon="@drawable/ic_mic" android:enabled="false" android:contentDescription="Disabled"/>\n</LinearLayout>\n' % XMLNS),
 ('res/values/styles_icon_buttons.xml', styles), res)

# FAB
res = pill_files('fab', [dis('?attr/colorOnSurface', '0.12'), ({}, '?attr/colorPrimaryContainer', None)], [dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorOnPrimaryContainer', None)], '?attr/colorOnPrimaryContainer', 28)
add('fab', 'FAB / Extended FAB', 'buttons',
 ('compose/AuroraFab.kt', '''package com.aurora.ivi.ui.components

import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsFocusedAsState
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import com.aurora.ivi.ui.*

/** 96x96dp, radius 28dp, icon 44dp, elevation level 3. One per screen. */
@Composable
fun AuroraFab(icon: ImageVector, contentDescription: String, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    FloatingActionButton(onClick, modifier.size(96.dp).auroraFocusRing(focused, 28.dp), RoundedCornerShape(28.dp),
        cs.primaryContainer, cs.onPrimaryContainer, interactionSource = interaction) { Icon(icon, contentDescription, Modifier.size(44.dp)) }
}

@Composable
fun AuroraExtendedFab(text: String, icon: ImageVector, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    ExtendedFloatingActionButton(onClick, modifier.height(96.dp).auroraFocusRing(focused, 28.dp), RoundedCornerShape(28.dp),
        cs.primaryContainer, cs.onPrimaryContainer, interactionSource = interaction) {
        Icon(icon, null, Modifier.size(44.dp)); Spacer(Modifier.width(16.dp)); Text(text, style = AuroraType.labelLarge)
    }
}
'''),
 ('res/layout/example_fab.xml', HDR + '<FrameLayout %s xmlns:app="http://schemas.android.com/apk/res-auto"\n    android:layout_width="wrap_content" android:layout_height="wrap_content">\n    <com.google.android.material.floatingactionbutton.FloatingActionButton\n        style="@style/Widget.Aurora.Fab"\n        android:layout_width="96dp" android:layout_height="96dp"\n        android:src="@drawable/ic_nav" android:contentDescription="Navigate"/>\n    <com.google.android.material.floatingactionbutton.ExtendedFloatingActionButton\n        style="@style/Widget.Aurora.ExtendedFab"\n        android:layout_width="wrap_content" android:layout_height="96dp"\n        android:text="Start route" app:icon="@drawable/ic_nav"/>\n</FrameLayout>\n' % XMLNS),
 ('res/values/styles_fab.xml', HDR + '<resources>\n    <style name="Widget.Aurora.Fab" parent="Widget.Material3.FloatingActionButton.Primary">\n        <item name="shapeAppearanceOverlay">@style/ShapeAppearance.Aurora.Large</item>\n        <item name="backgroundTint">?attr/colorPrimaryContainer</item>\n        <item name="tint">?attr/colorOnPrimaryContainer</item>\n        <item name="maxImageSize">44dp</item>\n        <item name="elevation">6dp</item>\n    </style>\n    <style name="Widget.Aurora.ExtendedFab" parent="Widget.Material3.ExtendedFloatingActionButton.Primary">\n        <item name="shapeAppearanceOverlay">@style/ShapeAppearance.Aurora.Large</item>\n        <item name="backgroundTint">?attr/colorPrimaryContainer</item>\n        <item name="iconTint">?attr/colorOnPrimaryContainer</item>\n        <item name="android:textColor">?attr/colorOnPrimaryContainer</item>\n        <item name="android:textAppearance">@style/TextAppearance.Aurora.LabelLarge</item>\n        <item name="iconSize">44dp</item>\n        <item name="android:paddingStart">28dp</item>\n        <item name="android:paddingEnd">28dp</item>\n    </style>\n</resources>\n'), res)

# ================================================================ SELECTION
def kt_head(extra=''):
    return 'package com.aurora.ivi.ui.components\n\nimport androidx.compose.foundation.*\nimport androidx.compose.foundation.interaction.*\nimport androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.shape.RoundedCornerShape\nimport androidx.compose.material3.*\nimport androidx.compose.runtime.*\nimport androidx.compose.ui.Alignment\nimport androidx.compose.ui.Modifier\nimport androidx.compose.ui.draw.scale\nimport androidx.compose.ui.graphics.Color\nimport androidx.compose.ui.graphics.vector.ImageVector\nimport androidx.compose.ui.unit.dp\nimport com.aurora.ivi.ui.*\n' + extra + '\n'

# --- Switch
res = {
 'res/color/aurora_switch_thumb.xml': sel([dis('?attr/colorOnSurface', '0.38'), ({'checked': True}, '?attr/colorOnPrimary', None), ({}, '?attr/colorOutline', None)], 'thumb: on = onPrimary, off = outline, disabled 38%'),
 'res/color/aurora_switch_track.xml': sel([dis('?attr/colorOnSurface', '0.12'), ({'checked': True}, '?attr/colorPrimary', None), ({}, '?attr/colorSurfaceContainerHighest', None)], 'track: on = primary, off = surfaceContainerHighest'),
 'res/color/aurora_switch_track_stroke.xml': sel([dis('?attr/colorOnSurface', '0.12'), ({'checked': True}, '?attr/colorPrimary', None), ({}, '?attr/colorOutline', None)], '2dp track border'),
 'res/color/aurora_switch_icon.xml': sel([dis('?attr/colorSurface', None), ({'checked': True}, '?attr/colorPrimary', None), ({}, '@android:color/transparent', None)], 'check icon inside the on-thumb'),
 'res/drawable/aurora_switch_focus.xml': HDR + '<!-- Wrap the switch: focused = 6dp ring in the theme focus color -->\n<selector %s>\n    <item android:state_focused="true">\n        <shape android:shape="rectangle">\n            <solid android:color="@android:color/transparent"/>\n            <corners android:radius="38dp"/>\n            <stroke android:width="6dp" android:color="?attr/auroraColorFocusRing"/>\n        </shape>\n    </item>\n    <item><shape android:shape="rectangle"><solid android:color="@android:color/transparent"/></shape></item>\n</selector>\n' % XMLNS}
add('switch', 'Switch', 'selection',
 ('compose/AuroraSwitch.kt', kt_head() + '''
/** Track 104x64dp, thumb 32dp (off) / 48dp (on) with check icon, row hit area 76dp. M3 Switch is 52x32, so it is scaled 2x inside a fixed box. */
@Composable
fun AuroraSwitch(checked: Boolean, onCheckedChange: (Boolean) -> Unit, modifier: Modifier = Modifier, enabled: Boolean = true) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    Box(modifier.size(width = 104.dp, height = 76.dp).auroraFocusRing(focused, 38.dp), contentAlignment = Alignment.Center) {
        Switch(
            checked, onCheckedChange, Modifier.scale(2f), enabled = enabled, interactionSource = interaction,
            thumbContent = if (checked) ({ Icon(androidx.compose.material.icons.Icons.Filled.Check, null, Modifier.size(SwitchDefaults.IconSize)) }) else null,
            colors = SwitchDefaults.colors(
                checkedThumbColor = cs.onPrimary, checkedTrackColor = cs.primary, checkedBorderColor = cs.primary, checkedIconColor = cs.primary,
                uncheckedThumbColor = cs.outline, uncheckedTrackColor = cs.surfaceContainerHighest, uncheckedBorderColor = cs.outline,
                disabledCheckedThumbColor = cs.surface, disabledCheckedTrackColor = cs.onSurface.copy(0.12f),
                disabledUncheckedThumbColor = cs.onSurface.copy(0.38f), disabledUncheckedTrackColor = cs.onSurface.copy(0.12f),
                disabledUncheckedBorderColor = cs.onSurface.copy(0.12f)))
    }
}
'''),
 ('res/layout/example_switch.xml', HDR + '<com.google.android.material.materialswitch.MaterialSwitch %s xmlns:app="http://schemas.android.com/apk/res-auto"\n    style="@style/Widget.Aurora.Switch"\n    android:layout_width="match_parent" android:layout_height="wrap_content"\n    android:text="Bluetooth" android:checked="true"/>\n' % XMLNS),
 ('res/values/styles_switch.xml', HDR + '<resources>\n    <!-- Track 104x64dp = default M3 switch (52x32) scaled 2x; row min height 76dp -->\n    <style name="Widget.Aurora.Switch" parent="Widget.Material3.CompoundButton.MaterialSwitch">\n        <item name="android:minHeight">76dp</item>\n        <item name="android:scaleX">2</item>\n        <item name="android:scaleY">2</item>\n        <item name="android:textAppearance">@style/TextAppearance.Aurora.BodyLarge</item>\n        <item name="thumbTint">@color/aurora_switch_thumb</item>\n        <item name="trackTint">@color/aurora_switch_track</item>\n        <item name="trackDecorationTint">@color/aurora_switch_track_stroke</item>\n        <item name="thumbIconTint">@color/aurora_switch_icon</item>\n        <item name="thumbIcon">@drawable/ic_check</item>\n        <item name="android:foreground">@drawable/aurora_switch_focus</item>\n    </style>\n</resources>\n'), res)

# --- Checkbox / Radio
for cid, nm, shape_txt, xml_cls, style_parent in [('checkbox', 'Checkbox', 'box 44dp, radius 8dp, border 3dp', 'com.google.android.material.checkbox.MaterialCheckBox', 'Widget.Material3.CompoundButton.CheckBox'), ('radio', 'Radio button', 'ring 44dp, border 3dp, dot 22dp', 'com.google.android.material.radiobutton.MaterialRadioButton', 'Widget.Material3.CompoundButton.RadioButton')]:
    res = {'res/color/aurora_%s_tint.xml' % cid: sel([dis('?attr/colorOnSurface', '0.38'), ({'checked': True}, '?attr/colorPrimary', None), ({}, '?attr/colorOutline', None)], '%s: checked = primary, unchecked = outline (theme-hued), disabled 38%%' % nm),
           'res/color/aurora_%s_tint_error.xml' % cid: sel([dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorError', None)], 'error state'),
           'res/color/aurora_%s_ripple.xml' % cid: sel([({'checked': True, 'pressed': True}, '?attr/colorPrimary', '0.12'), ({'pressed': True}, '?attr/colorOnSurface', '0.12'), ({'focused': True}, '?attr/colorPrimary', '0.12'), ({'hovered': True}, '?attr/colorOnSurface', '0.08'), ({}, '@android:color/transparent', None)], 'state layer'),
           'res/drawable/aurora_%s_focus.xml' % cid: HDR + '<selector %s>\n    <item android:state_focused="true">\n        <shape android:shape="oval">\n            <solid android:color="@android:color/transparent"/>\n            <stroke android:width="6dp" android:color="?attr/auroraColorFocusRing"/>\n        </shape>\n    </item>\n    <item><shape android:shape="oval"><solid android:color="@android:color/transparent"/></shape></item>\n</selector>\n' % XMLNS}
    compose_core = ('Checkbox(checked, onCheckedChange, Modifier.scale(2.4f), enabled, interactionSource = interaction,\n            colors = CheckboxDefaults.colors(checkedColor = cs.primary, uncheckedColor = cs.outline, checkmarkColor = cs.onPrimary, disabledCheckedColor = cs.onSurface.copy(0.38f), disabledUncheckedColor = cs.onSurface.copy(0.38f)))' if cid == 'checkbox'
                    else 'RadioButton(selected, onClick, Modifier.scale(1.8f), enabled, interactionSource = interaction,\n            colors = RadioButtonDefaults.colors(selectedColor = cs.primary, unselectedColor = cs.outline, disabledSelectedColor = cs.onSurface.copy(0.38f), disabledUnselectedColor = cs.onSurface.copy(0.38f)))')
    sig = 'checked: Boolean, onCheckedChange: ((Boolean) -> Unit)?' if cid == 'checkbox' else 'selected: Boolean, onClick: (() -> Unit)?'
    add(cid, nm, 'selection',
     ('compose/Aurora%s.kt' % ('Checkbox' if cid == 'checkbox' else 'RadioButton'), kt_head() + '''
/** %s. Glyph is scaled to match the spec; the clickable box is 76x76dp. */
@Composable
fun Aurora%s(%s, modifier: Modifier = Modifier, enabled: Boolean = true) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    Box(modifier.size(76.dp).auroraFocusRing(focused, 38.dp), contentAlignment = Alignment.Center) {
        %s
    }
}
''' % (shape_txt, 'Checkbox' if cid == 'checkbox' else 'RadioButton', sig, compose_core)),
     ('res/layout/example_%s.xml' % cid, HDR + '<LinearLayout %s xmlns:app="http://schemas.android.com/apk/res-auto"\n    android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical">\n    <%s style="@style/Widget.Aurora.%s" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Avoid tolls" android:checked="true"/>\n    <%s style="@style/Widget.Aurora.%s" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Avoid highways"/>\n    <%s style="@style/Widget.Aurora.%s" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="Disabled" android:enabled="false"/>\n</LinearLayout>\n' % (XMLNS, xml_cls, nm.split()[0], xml_cls, nm.split()[0], xml_cls, nm.split()[0])),
     ('res/values/styles_%s.xml' % cid, HDR + '<resources>\n    <style name="Widget.Aurora.%s" parent="%s">\n        <item name="android:minHeight">76dp</item>\n        <item name="android:minWidth">76dp</item>\n        <item name="android:paddingStart">16dp</item>\n        <item name="android:textAppearance">@style/TextAppearance.Aurora.BodyLarge</item>\n        <item name="buttonTint">@color/aurora_%s_tint</item>\n        <item name="android:foreground">@drawable/aurora_%s_focus</item>\n    </style>\n    <style name="Widget.Aurora.%s.Error">\n        <item name="buttonTint">@color/aurora_%s_tint_error</item>\n    </style>\n</resources>\n' % (nm.split()[0], style_parent, cid, cid, nm.split()[0], cid)), res)

# --- Slider
res = {'res/color/aurora_slider_active.xml': sel([dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorPrimary', None)], 'active track + handle'),
       'res/color/aurora_slider_inactive.xml': sel([dis('?attr/colorOnSurface', '0.12'), ({}, '?attr/colorSecondaryContainer', None)], 'inactive track'),
       'res/color/aurora_slider_thumb.xml': sel([dis('?attr/colorOnSurface', '0.38'), ({'focused': True}, '?attr/auroraColorFocusRing', None), ({}, '?attr/colorPrimary', None)], 'handle: focused = focus color (theme hue)'),
       'res/color/aurora_slider_halo.xml': sel([({'pressed': True}, '?attr/colorPrimary', '0.12'), ({'focused': True}, '?attr/colorPrimary', '0.12'), ({}, '@android:color/transparent', None)], 'halo = state layer')}
add('slider', 'Slider', 'selection',
 ('compose/AuroraSlider.kt', kt_head('import androidx.compose.ui.draw.clip\n') + '''
/** Track 16dp (radius 8), handle 12x64dp, row 76dp. Focused handle uses the theme focus color. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuroraSlider(value: Float, onValueChange: (Float) -> Unit, modifier: Modifier = Modifier, valueRange: ClosedFloatingPointRange<Float> = 0f..1f, enabled: Boolean = true) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    Slider(
        value, onValueChange, modifier.heightIn(min = 76.dp), enabled, valueRange, interactionSource = interaction,
        colors = SliderDefaults.colors(thumbColor = cs.primary, activeTrackColor = cs.primary, inactiveTrackColor = cs.secondaryContainer,
            disabledThumbColor = cs.onSurface.copy(0.38f), disabledActiveTrackColor = cs.onSurface.copy(0.38f), disabledInactiveTrackColor = cs.onSurface.copy(0.12f)),
        thumb = { Box(Modifier.size(12.dp, 64.dp).clip(RoundedCornerShape(6.dp)).background(if (!enabled) cs.onSurface.copy(0.38f) else if (focused) LocalAuroraExtras.current.focusRing else cs.primary)) },
        track = { state -> SliderDefaults.Track(state, Modifier.height(16.dp), enabled = enabled, thumbTrackGapSize = 6.dp, trackInsideCornerSize = 8.dp) },
    )
}
'''),
 ('res/layout/example_slider.xml', HDR + '<com.google.android.material.slider.Slider %s xmlns:app="http://schemas.android.com/apk/res-auto"\n    style="@style/Widget.Aurora.Slider"\n    android:layout_width="match_parent" android:layout_height="wrap_content"\n    android:valueFrom="0" android:valueTo="40" android:value="18" android:stepSize="1"/>\n' % XMLNS),
 ('res/values/styles_slider.xml', HDR + '<resources>\n    <style name="Widget.Aurora.Slider" parent="Widget.Material3.Slider">\n        <item name="android:minHeight">76dp</item>\n        <item name="trackHeight">16dp</item>\n        <item name="trackCornerSize">8dp</item>\n        <item name="thumbWidth">12dp</item>\n        <item name="thumbHeight">64dp</item>\n        <item name="thumbTrackGapSize">6dp</item>\n        <item name="trackColorActive">@color/aurora_slider_active</item>\n        <item name="trackColorInactive">@color/aurora_slider_inactive</item>\n        <item name="thumbTintList">@color/aurora_slider_thumb</item>\n        <item name="haloColor">@color/aurora_slider_halo</item>\n        <item name="haloRadius">38dp</item>\n    </style>\n</resources>\n'), res)

# ================================================================ CHIPS / SEGMENTED / HVAC TILE (pill controls with checked state)
def checkable(cid, nm, section, key, radius, height, minw, px, cont_checked, cont_def, content_checked, content_def, layer, stroke, kotlin, layout_cls, parent, text_style, extra=''):
    res = pill_files(key, [dis('?attr/colorOnSurface', '0.12'), ({'checked': True}, cont_checked, None), ({}, cont_def, None)],
                     [dis('?attr/colorOnSurface', '0.38'), ({'checked': True}, content_checked, None), ({}, content_def, None)], layer, radius, stroke)
    add(cid, nm, section, ('compose/Aurora%s.kt' % ''.join(w[0].upper() + w[1:] for w in nm.replace('/', ' ').split()), kotlin),
        ('res/layout/example_%s.xml' % key, HDR + '<LinearLayout %s xmlns:app="http://schemas.android.com/apk/res-auto"\n    android:layout_width="wrap_content" android:layout_height="wrap_content" android:orientation="horizontal">\n    <%s style="@style/Widget.Aurora.%s" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Fastest" android:checked="true"/>\n    <%s style="@style/Widget.Aurora.%s" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Avoid tolls"/>\n    <%s style="@style/Widget.Aurora.%s" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Disabled" android:enabled="false"/>\n</LinearLayout>\n' % (XMLNS, layout_cls, nm.split()[0], layout_cls, nm.split()[0], layout_cls, nm.split()[0])),
        ('res/values/styles_%s.xml' % key, HDR + '<resources>\n    <style name="Widget.Aurora.%s" parent="%s">\n        <item name="android:minHeight">%sdp</item>\n        <item name="android:minWidth">%sdp</item>\n        <item name="android:paddingStart">%sdp</item>\n        <item name="android:paddingEnd">%sdp</item>\n        <item name="android:textAppearance">@style/TextAppearance.Aurora.%s</item>\n        <item name="android:background">@drawable/aurora_%s_background</item>\n        <item name="android:textColor">@color/aurora_%s_content</item>\n        <item name="android:checkable">true</item>\n        <item name="backgroundTint">@null</item>\n        <item name="iconTint">@color/aurora_%s_content</item>\n%s    </style>\n</resources>\n' % (nm.split()[0], parent, height, minw, px, px, text_style, key, key, key, extra)), res)

checkable('chip', 'Filter chip', 'chips', 'chip', 16, 64, 64, 28, '?attr/colorSecondaryContainer', '@android:color/transparent', '?attr/colorOnSecondaryContainer', '?attr/colorOnSurfaceVariant', '?attr/colorOnSurface',
 [dis('?attr/colorOnSurface', '0.12'), ({'checked': True}, '@android:color/transparent', None), ({}, '?attr/colorOutline', None)],
 kt_head() + '''
/** 64dp visual (76dp hit area), radius 16dp, label 24sp. Unselected: outline border; selected: secondaryContainer + check. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuroraFilterChip(label: String, selected: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier, enabled: Boolean = true) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    FilterChip(
        selected, onClick, { Text(label, style = AuroraType.labelMedium) },
        modifier.heightIn(min = 76.dp).padding(vertical = 6.dp).auroraFocusRing(focused, 16.dp), enabled,
        leadingIcon = if (selected) ({ Icon(androidx.compose.material.icons.Icons.Filled.Check, null, Modifier.size(32.dp)) }) else null,
        shape = RoundedCornerShape(16.dp), interactionSource = interaction,
        colors = FilterChipDefaults.filterChipColors(
            containerColor = Color.Transparent, labelColor = cs.onSurfaceVariant, iconColor = cs.onSurfaceVariant,
            selectedContainerColor = cs.secondaryContainer, selectedLabelColor = cs.onSecondaryContainer, selectedLeadingIconColor = cs.onSecondaryContainer,
            disabledLabelColor = cs.onSurface.copy(0.38f)),
        border = FilterChipDefaults.filterChipBorder(enabled, selected, borderColor = cs.outline, selectedBorderColor = Color.Transparent,
            disabledBorderColor = cs.onSurface.copy(0.12f), borderWidth = 2.dp))
}
''', 'com.google.android.material.chip.Chip', 'Widget.Material3.Chip.Filter', 'LabelMedium')

checkable('segmented', 'Segmented button', 'chips', 'seg', 38, 76, 96, 36, '?attr/colorSecondaryContainer', '@android:color/transparent', '?attr/colorOnSecondaryContainer', '?attr/colorOnSurface', '?attr/colorOnSurface',
 [dis('?attr/colorOnSurface', '0.12'), ({}, '?attr/colorOutline', None)],
 kt_head() + '''
/** 76dp high, 2dp outline, 2-4 segments, label 26sp. Selected: secondaryContainer. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuroraSegmentedButton(options: List<String>, selectedIndex: Int, onSelect: (Int) -> Unit, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    SingleChoiceSegmentedButtonRow(modifier.heightIn(min = 76.dp)) {
        options.forEachIndexed { i, label ->
            SegmentedButton(
                selected = i == selectedIndex, onClick = { onSelect(i) },
                shape = SegmentedButtonDefaults.itemShape(i, options.size, RoundedCornerShape(38.dp)),
                modifier = Modifier.heightIn(min = 76.dp),
                colors = SegmentedButtonDefaults.colors(
                    activeContainerColor = cs.secondaryContainer, activeContentColor = cs.onSecondaryContainer, activeBorderColor = cs.outline,
                    inactiveContainerColor = Color.Transparent, inactiveContentColor = cs.onSurface, inactiveBorderColor = cs.outline,
                    disabledInactiveContentColor = cs.onSurface.copy(0.38f), disabledInactiveBorderColor = cs.onSurface.copy(0.12f)),
                border = BorderStroke(2.dp, cs.outline),
            ) { Text(label, style = AuroraType.labelMedium) }
        }
    }
}
''', 'com.google.android.material.button.MaterialButton', 'Widget.Material3.Button.OutlinedButton', 'LabelLarge', extra='        <item name="android:insetTop">0dp</item>\n        <item name="android:insetBottom">0dp</item>\n')

checkable('tile', 'HVAC toggle tile', 'hvac', 'tile', 28, 112, 112, 8, '?attr/colorPrimaryContainer', '?attr/colorSurfaceContainerHighest', '?attr/colorOnPrimaryContainer', '?attr/colorOnSurfaceVariant', '?attr/colorOnSurface', None,
 kt_head() + '''
/** 112x112dp tile, radius 28dp, icon 44dp, label 20sp. Off: surfaceContainerHighest; On: primaryContainer. */
@Composable
fun AuroraToggleTile(label: String, icon: ImageVector, checked: Boolean, onCheckedChange: (Boolean) -> Unit, modifier: Modifier = Modifier, enabled: Boolean = true) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    val container = if (!enabled) cs.onSurface.copy(0.12f) else if (checked) cs.primaryContainer else cs.surfaceContainerHighest
    val content = if (!enabled) cs.onSurface.copy(0.38f) else if (checked) cs.onPrimaryContainer else cs.onSurfaceVariant
    Surface(
        checked = checked, onCheckedChange = onCheckedChange, modifier = modifier.size(112.dp).auroraFocusRing(focused, 28.dp), enabled = enabled,
        shape = RoundedCornerShape(28.dp), color = container, contentColor = content, interactionSource = interaction,
    ) {
        Column(Modifier.fillMaxSize(), Arrangement.Center, Alignment.CenterHorizontally) {
            Icon(icon, null, Modifier.size(44.dp)); Text(label, style = AuroraType.labelSmall)
        }
    }
}
''', 'com.google.android.material.button.MaterialButton', 'Widget.Material3.Button.UnelevatedButton', 'LabelSmall', extra='        <item name="iconGravity">top</item>\n        <item name="iconSize">44dp</item>\n        <item name="android:layout_width">112dp</item>\n        <item name="android:layout_height">112dp</item>\n')

# ================================================================ TEXT FIELD / SEARCH
res = {'res/color/aurora_field_stroke.xml': sel([dis('?attr/colorOnSurface', '0.12'), ({'state_focused' if False else 'focused': True}, '?attr/colorPrimary', None), ({}, '?attr/colorOutline', None)], 'outline: focused = primary, default = outline (theme-hued), disabled 12%'),
       'res/color/aurora_field_hint.xml': sel([dis('?attr/colorOnSurface', '0.38'), ({'focused': True}, '?attr/colorPrimary', None), ({}, '?attr/colorOnSurfaceVariant', None)], 'floating label'),
       'res/color/aurora_field_text.xml': sel([dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorOnSurface', None)], 'input text'),
       'res/color/aurora_field_error.xml': sel([({}, '?attr/colorError', None)], 'error border / label / helper'),
       'res/drawable/aurora_search_bg.xml': HDR + '<!-- Search bar: surfaceContainerHigh, fully rounded; focused = 6dp focus ring -->\n<selector %s>\n    <item android:state_focused="true">\n        <layer-list>\n            <item><shape><solid android:color="?attr/colorSurfaceContainerHigh"/><corners android:radius="44dp"/><stroke android:width="6dp" android:color="?attr/auroraColorFocusRing"/></shape></item>\n        </layer-list>\n    </item>\n    <item><shape><solid android:color="?attr/colorSurfaceContainerHigh"/><corners android:radius="44dp"/></shape></item>\n</selector>\n' % XMLNS}
add('textfield', 'Text field', 'fields',
 ('compose/AuroraTextField.kt', kt_head() + '''
/** 88dp high, radius 12dp, 2dp border, input 28sp, floating label 28 -> 20sp. Border: outline -> primary (focused) -> error. */
@Composable
fun AuroraTextField(value: String, onValueChange: (String) -> Unit, label: String, modifier: Modifier = Modifier, enabled: Boolean = true, isError: Boolean = false, supportingText: String? = null) {
    val cs = MaterialTheme.colorScheme
    OutlinedTextField(
        value, onValueChange, modifier.heightIn(min = 88.dp), enabled = enabled, isError = isError,
        label = { Text(label, style = AuroraType.bodyLarge) },
        supportingText = supportingText?.let { { Text(it, style = AuroraType.bodySmall) } },
        textStyle = AuroraType.bodyLarge,
        shape = RoundedCornerShape(12.dp),
        colors = OutlinedTextFieldDefaults.colors(
            focusedBorderColor = cs.primary, unfocusedBorderColor = cs.outline, errorBorderColor = cs.error, disabledBorderColor = cs.onSurface.copy(0.12f),
            focusedLabelColor = cs.primary, unfocusedLabelColor = cs.onSurfaceVariant, errorLabelColor = cs.error,
            focusedTextColor = cs.onSurface, unfocusedTextColor = cs.onSurface, disabledTextColor = cs.onSurface.copy(0.38f)),
    )
}

/** Search bar: 88dp, fully rounded, surfaceContainerHigh. While driving replace with a voice button. */
@Composable
fun AuroraSearchBar(query: String, onQueryChange: (String) -> Unit, modifier: Modifier = Modifier, onVoice: () -> Unit = {}) {
    val cs = MaterialTheme.colorScheme
    TextField(
        query, onQueryChange, modifier.heightIn(min = 88.dp).fillMaxWidth(), singleLine = true, textStyle = AuroraType.bodyLarge,
        placeholder = { Text("Search music, places, contacts", style = AuroraType.bodyLarge) },
        leadingIcon = { Icon(androidx.compose.material.icons.Icons.Filled.Search, null, Modifier.size(40.dp)) },
        trailingIcon = { IconButton(onVoice, Modifier.size(76.dp)) { Icon(androidx.compose.material.icons.Icons.Filled.Mic, "Voice", Modifier.size(40.dp)) } },
        shape = RoundedCornerShape(44.dp),
        colors = TextFieldDefaults.colors(focusedContainerColor = cs.surfaceContainerHigh, unfocusedContainerColor = cs.surfaceContainerHigh,
            focusedIndicatorColor = Color.Transparent, unfocusedIndicatorColor = Color.Transparent, unfocusedPlaceholderColor = cs.onSurfaceVariant),
    )
}
'''),
 ('res/layout/example_text_field.xml', HDR + '<com.google.android.material.textfield.TextInputLayout %s xmlns:app="http://schemas.android.com/apk/res-auto"\n    style="@style/Widget.Aurora.TextField"\n    android:layout_width="420dp" android:layout_height="wrap_content"\n    android:hint="Destination" app:helperText="Street, place or contact">\n    <com.google.android.material.textfield.TextInputEditText\n        android:layout_width="match_parent" android:layout_height="wrap_content"\n        android:textAppearance="@style/TextAppearance.Aurora.BodyLarge" android:minHeight="88dp"/>\n</com.google.android.material.textfield.TextInputLayout>\n\n<!-- Error: style="@style/Widget.Aurora.TextField" + app:errorEnabled="true" + setError() -->\n' % XMLNS),
 ('res/values/styles_text_field.xml', HDR + '<resources>\n    <style name="Widget.Aurora.TextField" parent="Widget.Material3.TextInputLayout.OutlinedBox">\n        <item name="boxCornerRadiusTopStart">12dp</item>\n        <item name="boxCornerRadiusTopEnd">12dp</item>\n        <item name="boxCornerRadiusBottomStart">12dp</item>\n        <item name="boxCornerRadiusBottomEnd">12dp</item>\n        <item name="boxStrokeWidth">2dp</item>\n        <item name="boxStrokeWidthFocused">4dp</item>\n        <item name="boxStrokeColor">@color/aurora_field_stroke</item>\n        <item name="hintTextColor">@color/aurora_field_hint</item>\n        <item name="android:textColorHint">@color/aurora_field_hint</item>\n        <item name="errorTextColor">@color/aurora_field_error</item>\n        <item name="boxStrokeErrorColor">@color/aurora_field_error</item>\n        <item name="helperTextTextAppearance">@style/TextAppearance.Aurora.BodySmall</item>\n        <item name="errorTextAppearance">@style/TextAppearance.Aurora.BodySmall</item>\n    </style>\n</resources>\n'), res)

# ================================================================ LIST ITEM / CARD
res = {'res/color/aurora_list_selected.xml': sel([({'activated': True}, '?attr/colorPrimary', '0.16'), ({'selected': True}, '?attr/colorPrimary', '0.16'), ({}, '@android:color/transparent', None)], 'selected row = primary @16% over surfaceContainer'),
       'res/color/aurora_list_layer.xml': sel([({'pressed': True}, '?attr/colorOnSurface', '0.12'), ({'focused': True}, '?attr/colorOnSurface', '0.12'), ({'hovered': True}, '?attr/colorOnSurface', '0.08'), ({}, '@android:color/transparent', None)], 'state layer'),
       'res/color/aurora_list_primary_text.xml': sel([dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorOnSurface', None)], 'primary text'),
       'res/color/aurora_list_secondary_text.xml': sel([dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorOnSurfaceVariant', None)], 'secondary text'),
       'res/drawable/aurora_list_item_bg.xml': HDR + '<!-- Row background: ripple (hover/press/focus layers) over selected tint; focus = inset 6dp ring; bottom divider uses outlineVariant -->\n<ripple %s android:color="@color/aurora_list_layer">\n    <item>\n        <selector>\n            <item android:state_focused="true">\n                <layer-list>\n                    <item><shape><solid android:color="@color/aurora_list_selected"/><stroke android:width="6dp" android:color="?attr/auroraColorFocusRing"/></shape></item>\n                </layer-list>\n            </item>\n            <item><shape><solid android:color="@color/aurora_list_selected"/></shape></item>\n        </selector>\n    </item>\n    <item android:gravity="bottom">\n        <shape><size android:height="1dp"/><solid android:color="?attr/colorOutlineVariant"/></shape>\n    </item>\n</ripple>\n' % XMLNS}
add('listitem', 'List item', 'lists',
 ('compose/AuroraListItem.kt', kt_head() + '''
/** 96dp (1-line) / 120dp (2-line) / 144dp (3-line). Selected = primary @16% over surfaceContainer. Focus ring inset. */
@Composable
fun AuroraListItem(
    primary: String, modifier: Modifier = Modifier, secondary: String? = null, selected: Boolean = false, enabled: Boolean = true,
    leading: (@Composable () -> Unit)? = null, trailing: (@Composable () -> Unit)? = null, onClick: () -> Unit = {},
) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    val bg = if (selected) cs.primary.copy(0.16f).compositeOver(cs.surfaceContainer) else cs.surfaceContainer
    ListItem(
        headlineContent = { Text(primary, style = AuroraType.bodyLarge) },
        supportingContent = secondary?.let { { Text(it, style = AuroraType.bodyMedium) } },
        leadingContent = leading, trailingContent = trailing,
        colors = ListItemDefaults.colors(containerColor = bg, headlineColor = cs.onSurface, supportingColor = cs.onSurfaceVariant,
            disabledHeadlineColor = cs.onSurface.copy(0.38f), disabledLeadingIconColor = cs.onSurface.copy(0.38f)),
        modifier = modifier.heightIn(min = if (secondary == null) 96.dp else 120.dp)
            .then(if (focused) Modifier.border(6.dp, LocalAuroraExtras.current.focusRing) else Modifier)
            .clickable(enabled = enabled, interactionSource = interaction, indication = LocalIndication.current, onClick = onClick),
    )
}
'''.replace('import androidx.compose.ui.unit.dp', 'import androidx.compose.ui.unit.dp\nimport androidx.compose.ui.graphics.compositeOver')),
 ('res/layout/item_aurora_list.xml', HDR + '<LinearLayout %s\n    android:layout_width="match_parent" android:layout_height="wrap_content" android:minHeight="120dp"\n    android:orientation="horizontal" android:gravity="center_vertical"\n    android:paddingHorizontal="32dp" android:paddingVertical="12dp"\n    android:background="@drawable/aurora_list_item_bg" android:foreground="?attr/selectableItemBackground"\n    android:focusable="true" android:clickable="true">\n    <ImageView android:layout_width="64dp" android:layout_height="64dp" android:padding="12dp"\n        android:background="@drawable/aurora_avatar_bg" android:src="@drawable/ic_phone" app:tint="?attr/colorOnPrimaryContainer" xmlns:app="http://schemas.android.com/apk/res-auto"/>\n    <LinearLayout android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1"\n        android:layout_marginStart="28dp" android:orientation="vertical">\n        <TextView android:id="@+id/primary" android:textAppearance="@style/TextAppearance.Aurora.BodyLarge" android:textColor="@color/aurora_list_primary_text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:maxLines="1" android:ellipsize="end"/>\n        <TextView android:id="@+id/secondary" android:textAppearance="@style/TextAppearance.Aurora.BodyMedium" android:textColor="@color/aurora_list_secondary_text" android:layout_width="wrap_content" android:layout_height="wrap_content" android:maxLines="1" android:ellipsize="end"/>\n    </LinearLayout>\n</LinearLayout>\n' % XMLNS),
 ('res/values/styles_list.xml', HDR + '<resources>\n    <!-- RecyclerView / CarUiRecyclerView container -->\n    <style name="Widget.Aurora.List" parent="">\n        <item name="android:background">?attr/colorSurfaceContainer</item>\n        <item name="android:clipToOutline">true</item>\n        <item name="android:outlineProvider">background</item>\n    </style>\n    <style name="Widget.Aurora.ListItem.Primary"><item name="android:textAppearance">@style/TextAppearance.Aurora.BodyLarge</item><item name="android:textColor">@color/aurora_list_primary_text</item></style>\n    <style name="Widget.Aurora.ListItem.Secondary"><item name="android:textAppearance">@style/TextAppearance.Aurora.BodyMedium</item><item name="android:textColor">@color/aurora_list_secondary_text</item></style>\n</resources>\n'),
 {**res, 'res/drawable/aurora_avatar_bg.xml': HDR + '<shape %s android:shape="oval">\n    <solid android:color="?attr/colorPrimaryContainer"/>\n</shape>\n' % XMLNS})

res = {'res/color/aurora_card_container.xml': sel([dis('?attr/colorOnSurface', '0.12'), ({}, '?attr/colorSurfaceContainer', None)], 'default card'),
       'res/color/aurora_card_container_filled.xml': sel([({}, '?attr/colorSurfaceContainerHighest', None)], 'filled card'),
       'res/color/aurora_card_container_emphasis.xml': sel([({}, '?attr/colorPrimaryContainer', None)], 'emphasis card (one per screen)'),
       'res/color/aurora_card_stroke.xml': sel([({'focused': True}, '?attr/auroraColorFocusRing', None), ({}, '?attr/colorOutlineVariant', None)], 'outlined card border; focused = ring'),
       'res/drawable/aurora_card_ripple.xml': HDR + '<ripple %s android:color="?attr/colorOnSurface"/>\n' % XMLNS}
add('card', 'Card', 'lists',
 ('compose/AuroraCard.kt', kt_head() + '''
enum class AuroraCardStyle { Default, Filled, Outlined, Emphasis }

/** Radius 24dp, padding 28x32dp, title 32sp, body 24sp. Clickable cards show hover/focus/pressed layers and a focus ring. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuroraCard(title: String, body: String, modifier: Modifier = Modifier, style: AuroraCardStyle = AuroraCardStyle.Default, onClick: (() -> Unit)? = null) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    val shape = RoundedCornerShape(24.dp)
    val (container, content) = when (style) {
        AuroraCardStyle.Default -> cs.surfaceContainer to cs.onSurface
        AuroraCardStyle.Filled -> cs.surfaceContainerHighest to cs.onSurface
        AuroraCardStyle.Outlined -> Color.Transparent to cs.onSurface
        AuroraCardStyle.Emphasis -> cs.primaryContainer to cs.onPrimaryContainer
    }
    val colors = CardDefaults.cardColors(containerColor = container, contentColor = content)
    val border = if (style == AuroraCardStyle.Outlined) BorderStroke(2.dp, cs.outlineVariant) else null
    val m = modifier.heightIn(min = 120.dp).auroraFocusRing(focused, 24.dp)
    val inner: @Composable ColumnScope.() -> Unit = {
        Column(Modifier.padding(horizontal = 32.dp, vertical = 28.dp)) {
            Text(title, style = AuroraType.titleLarge); Text(body, style = AuroraType.bodyMedium, color = if (style == AuroraCardStyle.Emphasis) content else cs.onSurfaceVariant)
        }
    }
    if (onClick != null) Card(onClick, m, shape = shape, colors = colors, border = border, interactionSource = interaction, content = inner)
    else Card(m, shape = shape, colors = colors, border = border, content = inner)
}
'''),
 ('res/layout/example_card.xml', HDR + '<com.google.android.material.card.MaterialCardView %s\n    style="@style/Widget.Aurora.Card"\n    android:layout_width="match_parent" android:layout_height="wrap_content"\n    android:checkable="false" android:clickable="true" android:focusable="true">\n    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:paddingHorizontal="32dp" android:paddingVertical="28dp">\n        <TextView android:textAppearance="@style/TextAppearance.Aurora.TitleLarge" android:textColor="?attr/colorOnSurface" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Next: Fuel stop"/>\n        <TextView android:textAppearance="@style/TextAppearance.Aurora.BodyMedium" android:textColor="?attr/colorOnSurfaceVariant" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="In 6.2 km"/>\n    </LinearLayout>\n</com.google.android.material.card.MaterialCardView>\n' % XMLNS),
 ('res/values/styles_card.xml', HDR + '<resources>\n    <style name="Widget.Aurora.Card" parent="Widget.Material3.CardView.Filled">\n        <item name="cardBackgroundColor">@color/aurora_card_container</item>\n        <item name="shapeAppearance">@style/ShapeAppearance.Aurora.Large</item>\n        <item name="rippleColor">?attr/colorOnSurface</item>\n        <item name="cardElevation">0dp</item>\n        <item name="android:minHeight">120dp</item>\n    </style>\n    <style name="Widget.Aurora.Card.Filled"><item name="cardBackgroundColor">@color/aurora_card_container_filled</item></style>\n    <style name="Widget.Aurora.Card.Outlined" parent="Widget.Material3.CardView.Outlined">\n        <item name="cardBackgroundColor">@android:color/transparent</item>\n        <item name="strokeColor">@color/aurora_card_stroke</item>\n        <item name="strokeWidth">2dp</item>\n        <item name="shapeAppearance">@style/ShapeAppearance.Aurora.Large</item>\n    </style>\n    <style name="Widget.Aurora.Card.Emphasis"><item name="cardBackgroundColor">@color/aurora_card_container_emphasis</item></style>\n</resources>\n'), res)

# ================================================================ TABS / RAIL (app bar)
res = {'res/color/aurora_tab_text.xml': sel([dis('?attr/colorOnSurface', '0.38'), ({'selected': True}, '?attr/colorPrimary', None), ({}, '?attr/colorOnSurfaceVariant', None)], 'selected = primary, unselected = onSurfaceVariant'),
       'res/color/aurora_tab_ripple.xml': sel([({'pressed': True}, '?attr/colorOnSurface', '0.12'), ({'focused': True}, '?attr/colorOnSurface', '0.12'), ({'hovered': True}, '?attr/colorOnSurface', '0.08'), ({}, '@android:color/transparent', None)], 'state layer'),
       'res/drawable/aurora_tab_indicator.xml': HDR + '<!-- 6dp indicator, top corners rounded 3dp, primary -->\n<shape %s>\n    <solid android:color="?attr/colorPrimary"/>\n    <corners android:topLeftRadius="3dp" android:topRightRadius="3dp"/>\n</shape>\n' % XMLNS}
add('tabs', 'Tabs', 'tabs',
 ('compose/AuroraTabs.kt', kt_head() + '''
/** 88dp high, label 28sp, 6dp indicator (radius 3dp), 2-4 tabs, divider 2dp in outlineVariant. */
@Composable
fun AuroraTabs(titles: List<String>, selectedIndex: Int, onSelect: (Int) -> Unit, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    PrimaryTabRow(
        selectedTabIndex = selectedIndex, modifier = modifier, containerColor = Color.Transparent, contentColor = cs.primary,
        indicator = { TabRowDefaults.PrimaryIndicator(Modifier.tabIndicatorOffset(selectedIndex), width = 120.dp, height = 6.dp, color = cs.primary, shape = RoundedCornerShape(topStart = 3.dp, topEnd = 3.dp)) },
        divider = { HorizontalDivider(thickness = 2.dp, color = cs.outlineVariant) },
    ) {
        titles.forEachIndexed { i, t ->
            Tab(selected = i == selectedIndex, onClick = { onSelect(i) }, modifier = Modifier.heightIn(min = 88.dp),
                selectedContentColor = cs.primary, unselectedContentColor = cs.onSurfaceVariant,
                text = { Text(t, style = AuroraType.labelLarge) })
        }
    }
}
'''),
 ('res/layout/example_tabs.xml', HDR + '<com.google.android.material.tabs.TabLayout %s\n    style="@style/Widget.Aurora.Tabs"\n    android:layout_width="match_parent" android:layout_height="88dp">\n    <com.google.android.material.tabs.TabItem android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Library"/>\n    <com.google.android.material.tabs.TabItem android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Favourites"/>\n    <com.google.android.material.tabs.TabItem android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Browse"/>\n</com.google.android.material.tabs.TabLayout>\n' % XMLNS),
 ('res/values/styles_tabs.xml', HDR + '<resources>\n    <style name="Widget.Aurora.Tabs" parent="Widget.Material3.TabLayout.Secondary">\n        <item name="android:minHeight">88dp</item>\n        <item name="tabMinWidth">160dp</item>\n        <item name="tabIndicator">@drawable/aurora_tab_indicator</item>\n        <item name="tabIndicatorHeight">6dp</item>\n        <item name="tabIndicatorFullWidth">false</item>\n        <item name="tabTextColor">@color/aurora_tab_text</item>\n        <item name="tabIconTint">@color/aurora_tab_text</item>\n        <item name="tabRippleColor">@color/aurora_tab_ripple</item>\n        <item name="tabTextAppearance">@style/TextAppearance.Aurora.LabelLarge</item>\n        <item name="tabSelectedTextAppearance">@style/TextAppearance.Aurora.LabelLarge</item>\n    </style>\n</resources>\n'), res)

res = {'res/color/aurora_rail_icon.xml': sel([dis('?attr/colorOnSurface', '0.38'), ({'checked': True}, '?attr/colorOnSecondaryContainer', None), ({'selected': True}, '?attr/colorOnSecondaryContainer', None), ({}, '?attr/colorOnSurfaceVariant', None)], 'icon: active = onSecondaryContainer, inactive = onSurfaceVariant'),
       'res/color/aurora_rail_label.xml': sel([dis('?attr/colorOnSurface', '0.38'), ({'checked': True}, '?attr/colorOnSurface', None), ({'selected': True}, '?attr/colorOnSurface', None), ({}, '?attr/colorOnSurfaceVariant', None)], 'label: active = onSurface'),
       'res/color/aurora_rail_pill.xml': sel([({'checked': True}, '?attr/colorSecondaryContainer', None), ({'selected': True}, '?attr/colorSecondaryContainer', None), ({}, '@android:color/transparent', None)], 'active pill 88x40dp'),
       'res/color/aurora_rail_ripple.xml': sel([({'pressed': True}, '?attr/colorOnSurface', '0.12'), ({'focused': True}, '?attr/colorOnSurface', '0.12'), ({'hovered': True}, '?attr/colorOnSurface', '0.08'), ({}, '@android:color/transparent', None)], 'state layer'),
       'res/drawable/aurora_rail_focus.xml': HDR + '<!-- 6dp inset focus ring around the 112x88dp item -->\n<selector %s>\n    <item android:state_focused="true"><shape><solid android:color="@android:color/transparent"/><corners android:radius="28dp"/><stroke android:width="6dp" android:color="?attr/auroraColorFocusRing"/></shape></item>\n    <item><shape><solid android:color="@android:color/transparent"/></shape></item>\n</selector>\n' % XMLNS}
add('rail', 'App bar (right rail)', 'sysbars',
 ('compose/AuroraRail.kt', kt_head() + '''
data class RailDestination(val label: String, val icon: ImageVector)

/** 120dp wide, item 112x88dp, active pill 88x40dp, icon 36dp, label 24sp. Place on the trailing edge (right). */
@Composable
fun AuroraAppRail(destinations: List<RailDestination>, selectedIndex: Int, onSelect: (Int) -> Unit, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    NavigationRail(modifier.width(120.dp), containerColor = cs.surfaceContainerLowest, contentColor = cs.onSurfaceVariant, windowInsets = WindowInsets(0)) {
        Spacer(Modifier.weight(1f))
        destinations.forEachIndexed { i, d ->
            val interaction = remember { MutableInteractionSource() }
            val focused by interaction.collectIsFocusedAsState()
            NavigationRailItem(
                selected = i == selectedIndex, onClick = { onSelect(i) }, interactionSource = interaction,
                modifier = Modifier.size(112.dp, 88.dp).auroraFocusRing(focused, 28.dp),
                icon = { Icon(d.icon, null, Modifier.size(36.dp)) },
                label = { Text(d.label, style = AuroraType.labelMedium) }, alwaysShowLabel = true,
                colors = NavigationRailItemDefaults.colors(
                    selectedIconColor = cs.onSecondaryContainer, selectedTextColor = cs.onSurface, indicatorColor = cs.secondaryContainer,
                    unselectedIconColor = cs.onSurfaceVariant, unselectedTextColor = cs.onSurfaceVariant),
            )
        }
        Spacer(Modifier.weight(1f))
    }
}
'''),
 ('res/layout/example_rail.xml', HDR + '<com.google.android.material.navigationrail.NavigationRailView %s xmlns:app="http://schemas.android.com/apk/res-auto"\n    style="@style/Widget.Aurora.NavigationRail"\n    android:layout_width="120dp" android:layout_height="match_parent"\n    app:menu="@menu/aurora_app_bar"/>\n\n<!-- res/menu/aurora_app_bar.xml: Home, Maps, Phone, Media, Vehicle, Apps (6 max) -->\n' % XMLNS),
 ('res/values/styles_rail.xml', HDR + '<resources>\n    <style name="Widget.Aurora.NavigationRail" parent="Widget.Material3.NavigationRailView">\n        <item name="android:background">?attr/colorSurfaceContainerLowest</item>\n        <item name="itemIconSize">36dp</item>\n        <item name="itemMinHeight">88dp</item>\n        <item name="itemIconTint">@color/aurora_rail_icon</item>\n        <item name="itemTextColor">@color/aurora_rail_label</item>\n        <item name="itemRippleColor">@color/aurora_rail_ripple</item>\n        <item name="itemActiveIndicatorStyle">@style/Widget.Aurora.NavigationRail.Indicator</item>\n        <item name="itemTextAppearanceActive">@style/TextAppearance.Aurora.LabelMedium</item>\n        <item name="itemTextAppearanceInactive">@style/TextAppearance.Aurora.LabelMedium</item>\n        <item name="labelVisibilityMode">labeled</item>\n        <item name="menuGravity">center</item>\n    </style>\n    <style name="Widget.Aurora.NavigationRail.Indicator" parent="Widget.Material3.NavigationRailView.ActiveIndicator">\n        <item name="android:width">88dp</item>\n        <item name="android:height">40dp</item>\n        <item name="android:color">@color/aurora_rail_pill</item>\n    </style>\n</resources>\n'), res)

# ================================================================ DIALOG / MENU / SNACKBAR
res = {'res/color/aurora_dialog_container.xml': sel([({}, '?attr/colorSurfaceContainerHigh', None)], 'dialog surface'),
       'res/color/aurora_dialog_body.xml': sel([({}, '?attr/colorOnSurfaceVariant', None)], 'body text'),
       'res/color/aurora_scrim.xml': sel([({}, '?attr/colorScrim' if False else '@color/aurora_scrim_value', None)], 'scrim 55%')}
res['res/color/aurora_scrim.xml'] = sel([({}, '?android:attr/colorBackgroundFloating', None)], 'override with your scrim: black @ 55% (dim amount 0.55 via android:backgroundDimAmount)')
add('dialog', 'Dialog', 'dialogs',
 ('compose/AuroraDialog.kt', kt_head() + '''
/** Width 640dp (max 840), radius 28dp, padding 40dp, title 36sp, body 28sp (<= 120 chars while driving), max 2 actions while driving. */
@Composable
fun AuroraDialog(title: String, body: String, confirm: String, onConfirm: () -> Unit, dismiss: String?, onDismiss: () -> Unit, icon: ImageVector? = null) {
    val cs = MaterialTheme.colorScheme
    AlertDialog(
        onDismissRequest = onDismiss, shape = RoundedCornerShape(28.dp), containerColor = cs.surfaceContainerHigh,
        iconContentColor = cs.secondary, titleContentColor = cs.onSurface, textContentColor = cs.onSurfaceVariant,
        icon = icon?.let { { Icon(it, null, Modifier.size(48.dp)) } },
        title = { Text(title, style = AuroraType.headlineMedium) },
        text = { Text(body, style = AuroraType.bodyLarge) },
        modifier = Modifier.widthIn(min = 640.dp, max = 840.dp),
        confirmButton = { AuroraFilledButton(confirm, onConfirm) },
        dismissButton = dismiss?.let { { AuroraTextButton(it, onDismiss) } },
    )
}
'''),
 ('examples/DialogUsage.kt', '// Views: MaterialAlertDialogBuilder with the Aurora overlay\nMaterialAlertDialogBuilder(this, R.style.ThemeOverlay_Aurora_Dialog)\n    .setIcon(R.drawable.ic_phone)\n    .setTitle("Forget Pixel 9?")\n    .setMessage("You will need to pair again.")\n    .setNegativeButton("Cancel", null)\n    .setPositiveButton("Forget") { _, _ -> forget() }\n    .show()\n'),
 ('res/values/styles_dialog.xml', HDR + '<resources>\n    <style name="ThemeOverlay.Aurora.Dialog" parent="ThemeOverlay.Material3.MaterialAlertDialog">\n        <item name="colorSurfaceContainerHigh">?attr/colorSurfaceContainerHigh</item>\n        <item name="shapeAppearanceOverlay">@style/ShapeAppearance.Aurora.ExtraLarge</item>\n        <item name="materialAlertDialogTitleTextStyle">@style/MaterialAlertDialog.Aurora.Title</item>\n        <item name="materialAlertDialogBodyTextStyle">@style/MaterialAlertDialog.Aurora.Body</item>\n        <item name="buttonBarPositiveButtonStyle">@style/Widget.Aurora.Button.Filled</item>\n        <item name="buttonBarNegativeButtonStyle">@style/Widget.Aurora.Button.Text</item>\n        <item name="android:windowMinWidthMajor">640dp</item>\n        <item name="android:backgroundDimAmount">0.55</item>\n    </style>\n    <style name="MaterialAlertDialog.Aurora.Title" parent="MaterialAlertDialog.Material3.Title.Text">\n        <item name="android:textAppearance">@style/TextAppearance.Aurora.HeadlineMedium</item>\n        <item name="android:textColor">?attr/colorOnSurface</item>\n    </style>\n    <style name="MaterialAlertDialog.Aurora.Body" parent="MaterialAlertDialog.Material3.Body.Text">\n        <item name="android:textAppearance">@style/TextAppearance.Aurora.BodyLarge</item>\n        <item name="android:textColor">@color/aurora_dialog_body</item>\n    </style>\n</resources>\n'), res)

res = {'res/color/aurora_menu_text.xml': sel([dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorOnSurface', None)], 'menu item text'),
       'res/color/aurora_menu_item_bg.xml': sel([({'checked': True}, '?attr/colorSecondaryContainer', None), ({'activated': True}, '?attr/colorSecondaryContainer', None), ({'focused': True}, '?attr/colorOnSurface', '0.12'), ({'pressed': True}, '?attr/colorOnSurface', '0.12'), ({'hovered': True}, '?attr/colorOnSurface', '0.08'), ({}, '@android:color/transparent', None)], 'selected item = secondaryContainer'),
       'res/drawable/aurora_menu_bg.xml': HDR + '<shape %s>\n    <solid android:color="?attr/colorSurfaceContainer"/>\n    <corners android:radius="20dp"/>\n</shape>\n' % XMLNS}
add('menu', 'Menu', 'dialogs',
 ('compose/AuroraMenu.kt', kt_head() + '''
/** Width 320-560dp, radius 20dp, item 76dp, text 28sp, icon 40dp, max 6 items while driving. */
@Composable
fun AuroraDropdownMenu(expanded: Boolean, onDismiss: () -> Unit, content: @Composable ColumnScope.() -> Unit) {
    val cs = MaterialTheme.colorScheme
    DropdownMenu(expanded, onDismiss, Modifier.widthIn(min = 320.dp, max = 560.dp), shape = RoundedCornerShape(20.dp), containerColor = cs.surfaceContainer, tonalElevation = 0.dp, content = content)
}

@Composable
fun AuroraMenuItem(text: String, onClick: () -> Unit, selected: Boolean = false, destructive: Boolean = false, leading: ImageVector? = null, enabled: Boolean = true) {
    val cs = MaterialTheme.colorScheme
    val bg = if (selected) cs.secondaryContainer else Color.Transparent
    val fg = when { destructive -> cs.error; selected -> cs.onSecondaryContainer; else -> cs.onSurface }
    DropdownMenuItem(
        text = { Text(text, style = AuroraType.bodyLarge) }, onClick = onClick, enabled = enabled, modifier = Modifier.heightIn(min = 76.dp).background(bg),
        leadingIcon = leading?.let { { Icon(it, null, Modifier.size(40.dp)) } },
        colors = MenuDefaults.itemColors(textColor = fg, leadingIconColor = fg, disabledTextColor = cs.onSurface.copy(0.38f)),
    )
}
'''),
 ('examples/MenuUsage.kt', '// Views: PopupMenu with the Aurora overlay\nval popup = PopupMenu(ContextThemeWrapper(this, R.style.ThemeOverlay_Aurora_PopupMenu), anchor)\npopup.menuInflater.inflate(R.menu.route_options, popup.menu)\npopup.show()\n'),
 ('res/values/styles_menu.xml', HDR + '<resources>\n    <style name="ThemeOverlay.Aurora.PopupMenu" parent="">\n        <item name="popupMenuStyle">@style/Widget.Aurora.PopupMenu</item>\n        <item name="android:textAppearanceLargePopupMenu">@style/TextAppearance.Aurora.BodyLarge</item>\n        <item name="android:itemBackground">@color/aurora_menu_item_bg</item>\n        <item name="android:textColor">@color/aurora_menu_text</item>\n    </style>\n    <style name="Widget.Aurora.PopupMenu" parent="Widget.Material3.PopupMenu">\n        <item name="android:popupBackground">@drawable/aurora_menu_bg</item>\n        <item name="android:dropDownWidth">320dp</item>\n        <item name="android:minHeight">76dp</item>\n    </style>\n</resources>\n'), res)

res = {'res/color/aurora_snackbar_container.xml': sel([({}, '?attr/colorSurfaceInverse', None)], 'inverseSurface'),
       'res/color/aurora_snackbar_text.xml': sel([({}, '?attr/colorOnSurfaceInverse', None)], 'inverseOnSurface'),
       'res/color/aurora_snackbar_action.xml': sel([({'pressed': True}, '?attr/colorPrimaryInverse', '0.8'), ({}, '?attr/colorPrimaryInverse', None)], 'inversePrimary')}
add('snackbar', 'Snackbar', 'dialogs',
 ('compose/AuroraSnackbar.kt', kt_head() + '''
/** Min height 92dp, radius 16dp, width 640dp, text 26sp, action 76dp high. No action while driving. */
@Composable
fun AuroraSnackbarHost(state: SnackbarHostState, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    SnackbarHost(state, modifier) { data ->
        Snackbar(
            data, Modifier.widthIn(max = 640.dp).heightIn(min = 92.dp), shape = RoundedCornerShape(16.dp),
            containerColor = cs.inverseSurface, contentColor = cs.inverseOnSurface, actionColor = cs.inversePrimary,
        )
    }
}
'''),
 ('examples/SnackbarUsage.kt', '// Views: styled automatically through snackbarStyle in Theme.Aurora\nSnackbar.make(view, "Route updated · 4 min faster", Snackbar.LENGTH_LONG)\n    .setAction("Undo") { undo() }   // omit the action while driving\n    .show()\n'),
 ('res/values/styles_snackbar.xml', HDR + '<resources>\n    <style name="Widget.Aurora.Snackbar" parent="Widget.Material3.Snackbar">\n        <item name="android:minHeight">92dp</item>\n        <item name="android:maxWidth">640dp</item>\n        <item name="backgroundTint">@color/aurora_snackbar_container</item>\n        <item name="shapeAppearanceOverlay">@style/ShapeAppearance.Aurora.Medium</item>\n    </style>\n    <style name="Widget.Aurora.Snackbar.TextView" parent="Widget.Material3.Snackbar.TextView">\n        <item name="android:textAppearance">@style/TextAppearance.Aurora.BodyLarge</item>\n        <item name="android:textColor">@color/aurora_snackbar_text</item>\n    </style>\n    <style name="Widget.Aurora.Snackbar.Button" parent="Widget.Material3.Button.TextButton.Snackbar">\n        <item name="android:minHeight">76dp</item>\n        <item name="android:textColor">@color/aurora_snackbar_action</item>\n        <item name="android:textAppearance">@style/TextAppearance.Aurora.LabelLarge</item>\n    </style>\n</resources>\n'), res)

# ================================================================ PROGRESS / BADGE / BANNER
res = {'res/color/aurora_progress_indicator.xml': sel([dis('?attr/colorOnSurface', '0.38'), ({}, '?attr/colorPrimary', None)], 'indicator'),
       'res/color/aurora_progress_track.xml': sel([({}, '?attr/colorSecondaryContainer', None)], 'track')}
add('progress', 'Progress', 'progress',
 ('compose/AuroraProgress.kt', kt_head() + '''
/** Linear 8dp (radius 4), circular 72dp / stroke 8dp. Show a spinner after 300 ms, keep it >= 600 ms. */
@Composable
fun AuroraLinearProgress(progress: (() -> Float)?, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    if (progress != null) LinearProgressIndicator(progress, modifier.height(8.dp), cs.primary, cs.secondaryContainer, gapSize = 0.dp, drawStopIndicator = {})
    else LinearProgressIndicator(modifier.height(8.dp), cs.primary, cs.secondaryContainer)
}

@Composable
fun AuroraCircularProgress(modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    CircularProgressIndicator(modifier.size(72.dp), cs.primary, 8.dp, cs.secondaryContainer)
}
'''),
 ('res/layout/example_progress.xml', HDR + '<LinearLayout %s xmlns:app="http://schemas.android.com/apk/res-auto"\n    android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical">\n    <com.google.android.material.progressindicator.LinearProgressIndicator style="@style/Widget.Aurora.LinearProgress"\n        android:layout_width="match_parent" android:layout_height="wrap_content" android:progress="62"/>\n    <com.google.android.material.progressindicator.CircularProgressIndicator style="@style/Widget.Aurora.CircularProgress"\n        android:layout_width="wrap_content" android:layout_height="wrap_content" android:indeterminate="true"/>\n</LinearLayout>\n' % XMLNS),
 ('res/values/styles_progress.xml', HDR + '<resources>\n    <style name="Widget.Aurora.LinearProgress" parent="Widget.Material3.LinearProgressIndicator">\n        <item name="trackThickness">8dp</item>\n        <item name="trackCornerRadius">4dp</item>\n        <item name="indicatorColor">@color/aurora_progress_indicator</item>\n        <item name="trackColor">@color/aurora_progress_track</item>\n    </style>\n    <style name="Widget.Aurora.CircularProgress" parent="Widget.Material3.CircularProgressIndicator">\n        <item name="indicatorSize">72dp</item>\n        <item name="trackThickness">8dp</item>\n        <item name="indicatorColor">@color/aurora_progress_indicator</item>\n        <item name="trackColor">@color/aurora_progress_track</item>\n    </style>\n</resources>\n'), res)

res = {'res/color/aurora_badge_bg.xml': sel([({}, '?attr/colorError', None)], 'badge container'),
       'res/color/aurora_badge_text.xml': sel([({}, '?attr/colorOnError', None)], 'badge text')}
add('badge', 'Badge', 'progress',
 ('compose/AuroraBadge.kt', kt_head() + '''
/** Number badge 32dp high (min 32 wide), dot 16dp. Phone / Messages only. */
@Composable
fun AuroraBadge(count: Int?, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    if (count == null) Box(modifier.size(16.dp).background(cs.error, androidx.compose.foundation.shape.CircleShape))
    else Badge(modifier.heightIn(min = 32.dp).widthIn(min = 32.dp), containerColor = cs.error, contentColor = cs.onError) { Text("$count", style = AuroraType.labelSmall) }
}
'''),
 ('examples/BadgeUsage.kt', '// Views\nBadgeDrawable.create(context).apply {\n    number = 3\n    BadgeUtils.attachBadgeDrawable(this, anchorView)   // styled by Widget.Aurora.Badge\n}\n'),
 ('res/values/styles_badge.xml', HDR + '<resources>\n    <style name="Widget.Aurora.Badge" parent="Widget.Material3.Badge">\n        <item name="backgroundColor">@color/aurora_badge_bg</item>\n        <item name="badgeTextColor">@color/aurora_badge_text</item>\n        <item name="badgeHeight">32dp</item>\n        <item name="badgeWidth">32dp</item>\n        <item name="badgeWithTextHeight">32dp</item>\n        <item name="badgeWithTextWidth">32dp</item>\n        <item name="badgeTextAppearance">@style/TextAppearance.Aurora.LabelSmall</item>\n    </style>\n</resources>\n'), res)

res = {}
for t, bg, fg in [('error', 'colorErrorContainer', 'colorOnErrorContainer'), ('warning', 'auroraColorWarningContainer', 'auroraColorOnWarningContainer'), ('success', 'auroraColorSuccessContainer', 'auroraColorOnSuccessContainer'), ('info', 'colorSecondaryContainer', 'colorOnSecondaryContainer')]:
    res['res/color/aurora_banner_%s_text.xml' % t] = sel([({}, '?attr/%s' % fg, None)], 'banner %s content' % t)
    res['res/drawable/aurora_banner_%s_bg.xml' % t] = HDR + '<!-- Banner (%s): radius 20dp, never rely on color alone: always add icon + text -->\n<shape %s>\n    <solid android:color="?attr/%s"/>\n    <corners android:radius="20dp"/>\n</shape>\n' % (t, XMLNS, bg)
add('banner', 'Banner / alert', 'progress',
 ('compose/AuroraBanner.kt', kt_head() + '''
enum class AuroraBannerType { Error, Warning, Success, Info }

/** Radius 20dp, padding 20x28dp, text 26sp, icon 40dp, at most one action. Safety (error) banners never auto-dismiss. */
@Composable
fun AuroraBanner(type: AuroraBannerType, message: String, icon: ImageVector, modifier: Modifier = Modifier, action: String? = null, onAction: () -> Unit = {}) {
    val cs = MaterialTheme.colorScheme
    val x = LocalAuroraExtras.current
    val (bg, fg) = when (type) {
        AuroraBannerType.Error -> cs.errorContainer to cs.onErrorContainer
        AuroraBannerType.Warning -> x.warningContainer to x.onWarningContainer
        AuroraBannerType.Success -> x.successContainer to x.onSuccessContainer
        AuroraBannerType.Info -> cs.secondaryContainer to cs.onSecondaryContainer
    }
    Row(modifier.fillMaxWidth().background(bg, RoundedCornerShape(20.dp)).padding(horizontal = 28.dp, vertical = 20.dp), verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, null, Modifier.size(40.dp), tint = fg)
        Spacer(Modifier.width(20.dp))
        Text(message, Modifier.weight(1f), style = AuroraType.bodyLarge, color = fg)
        if (action != null) TextButton(onAction, Modifier.heightIn(min = 76.dp), colors = ButtonDefaults.textButtonColors(contentColor = fg)) { Text(action, style = AuroraType.labelLarge) }
    }
}
'''),
 ('res/layout/example_banner.xml', HDR + '<LinearLayout %s\n    android:layout_width="match_parent" android:layout_height="wrap_content"\n    android:orientation="horizontal" android:gravity="center_vertical"\n    android:paddingHorizontal="28dp" android:paddingVertical="20dp"\n    android:background="@drawable/aurora_banner_warning_bg">\n    <ImageView android:layout_width="40dp" android:layout_height="40dp" android:src="@drawable/ic_warn" app:tint="?attr/auroraColorOnWarningContainer" xmlns:app="http://schemas.android.com/apk/res-auto"/>\n    <TextView android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:layout_marginStart="20dp"\n        android:textAppearance="@style/TextAppearance.Aurora.BodyLarge" android:textColor="@color/aurora_banner_warning_text" android:text="Range 42 km — find a charger?"/>\n</LinearLayout>\n<!-- Variants: aurora_banner_error_bg / _warning_bg / _success_bg / _info_bg -->\n' % XMLNS),
 ('res/values/styles_banner.xml', HDR + '<resources>\n    <style name="Widget.Aurora.Banner.Text" parent="">\n        <item name="android:textAppearance">@style/TextAppearance.Aurora.BodyLarge</item>\n        <item name="android:minHeight">76dp</item>\n    </style>\n</resources>\n'), res)

# ================================================================ THEME-LEVEL FILES
def kebab(s): return re.sub(r'[A-Z]', lambda m: '_' + m.group(0).lower(), s)
def snake(s): return kebab(s).replace('-', '_')
def prefix(tid): return 'aurora' if tid in ('aurora-night', 'aurora-day') else 'aurora_' + snake(tid.replace('drive-', ''))
THEME_NAMES = {'aurora-night': 'Theme.Aurora', 'drive-comfort': 'Theme.Aurora.Comfort', 'drive-eco': 'Theme.Aurora.Eco', 'drive-sport': 'Theme.Aurora.Sport', 'drive-offroad': 'Theme.Aurora.Offroad', 'drive-night': 'Theme.Aurora.NightDrive'}

MAT_ATTRS = [('colorPrimary', 'primary'), ('colorOnPrimary', 'onPrimary'), ('colorPrimaryContainer', 'primaryContainer'), ('colorOnPrimaryContainer', 'onPrimaryContainer'),
 ('colorSecondary', 'secondary'), ('colorOnSecondary', 'onSecondary'), ('colorSecondaryContainer', 'secondaryContainer'), ('colorOnSecondaryContainer', 'onSecondaryContainer'),
 ('colorTertiary', 'tertiary'), ('colorOnTertiary', 'onTertiary'), ('colorTertiaryContainer', 'tertiaryContainer'), ('colorOnTertiaryContainer', 'onTertiaryContainer'),
 ('colorError', 'error'), ('colorOnError', 'onError'), ('colorErrorContainer', 'errorContainer'), ('colorOnErrorContainer', 'onErrorContainer'),
 ('android:colorBackground', 'background'), ('colorOnBackground', 'onBackground'), ('colorSurface', 'surface'), ('colorOnSurface', 'onSurface'),
 ('colorSurfaceVariant', 'surfaceVariant'), ('colorOnSurfaceVariant', 'onSurfaceVariant'), ('colorOutline', 'outline'), ('colorOutlineVariant', 'outlineVariant'),
 ('colorSurfaceInverse', 'inverseSurface'), ('colorOnSurfaceInverse', 'inverseOnSurface'), ('colorPrimaryInverse', 'inversePrimary'),
 ('colorSurfaceContainerLowest', 'surfaceContainerLowest'), ('colorSurfaceContainerLow', 'surfaceContainerLow'), ('colorSurfaceContainer', 'surfaceContainer'),
 ('colorSurfaceContainerHigh', 'surfaceContainerHigh'), ('colorSurfaceContainerHighest', 'surfaceContainerHighest')]
EXTRA_ATTRS = [('auroraColorSuccess', 'success'), ('auroraColorOnSuccess', 'onSuccess'), ('auroraColorSuccessContainer', 'successContainer'), ('auroraColorOnSuccessContainer', 'onSuccessContainer'),
 ('auroraColorWarning', 'warning'), ('auroraColorOnWarning', 'onWarning'), ('auroraColorWarningContainer', 'warningContainer'), ('auroraColorOnWarningContainer', 'onWarningContainer'),
 ('auroraColorFocusRing', 'onPrimaryContainer')]

def theme_files(tok, TYPE):
    f = {}
    f['res/values/attrs.xml'] = HDR + '<resources>\n    <!-- Aurora extras beyond Material 3 roles. Focus ring = onPrimaryContainer (theme-hued). -->\n' + ''.join('    <attr name="%s" format="color"/>\n' % a for a, _ in EXTRA_ATTRS) + '</resources>\n'
    th = HDR + '<!-- Aurora themes. Aurora (Day/Night) follows system dark mode via values / values-night colors.\n     Drive-mode themes are dark ThemeOverlays; apply with ContextThemeWrapper / setTheme() when the vehicle drive mode changes. -->\n<resources>\n'
    for tid, t in tok['themes'].items():
        if tid == 'aurora-day': continue
        p = prefix(tid)
        parent = 'Theme.Material3.DayNight.NoActionBar' if tid == 'aurora-night' else 'Theme.Material3.Dark.NoActionBar'
        th += '    <!-- %s — %s -->\n    <style name="%s" parent="%s">\n' % (t['name'], t['desc'], THEME_NAMES[tid], parent)
        for a, r in MAT_ATTRS + EXTRA_ATTRS:
            th += '        <item name="%s">@color/%s_%s</item>\n' % (a, p, snake(r))
        th += '        <item name="shapeAppearanceSmallComponent">@style/ShapeAppearance.Aurora.Small</item>\n        <item name="shapeAppearanceMediumComponent">@style/ShapeAppearance.Aurora.Medium</item>\n        <item name="shapeAppearanceLargeComponent">@style/ShapeAppearance.Aurora.Large</item>\n        <item name="snackbarStyle">@style/Widget.Aurora.Snackbar</item>\n        <item name="snackbarTextViewStyle">@style/Widget.Aurora.Snackbar.TextView</item>\n        <item name="snackbarButtonStyle">@style/Widget.Aurora.Snackbar.Button</item>\n        <item name="android:fontFamily">@font/roboto</item>\n    </style>\n\n'
    th += '</resources>\n'
    f['res/values/themes.xml'] = th
    f['res/values/shapes.xml'] = HDR + '<resources>\n' + ''.join('    <style name="ShapeAppearance.Aurora.%s" parent="">\n        <item name="cornerFamily">rounded</item>\n        <item name="cornerSize">%s</item>\n    </style>\n' % (n, v) for n, v in [('None', '0dp'), ('ExtraSmall', '8dp'), ('Small', '12dp'), ('Medium', '16dp'), ('Large', '24dp'), ('ExtraLarge', '28dp'), ('Full', '50%')]) + '</resources>\n'
    f['res/values/dimens.xml'] = HDR + '''<resources>
    <!-- Spacing (8dp grid) -->
    <dimen name="aurora_space_2xs">4dp</dimen><dimen name="aurora_space_xs">8dp</dimen><dimen name="aurora_space_sm">12dp</dimen><dimen name="aurora_space_md">16dp</dimen>
    <dimen name="aurora_space_lg">24dp</dimen><dimen name="aurora_space_xl">32dp</dimen><dimen name="aurora_space_2xl">40dp</dimen><dimen name="aurora_space_3xl">48dp</dimen>
    <!-- Touch -->
    <dimen name="aurora_touch_min">76dp</dimen><dimen name="aurora_touch_primary">96dp</dimen>
    <!-- System bars (1280x720dp viewport, 10" 1920x1080 @1.5x) -->
    <dimen name="aurora_status_bar_height">56dp</dimen><dimen name="aurora_app_bar_width">120dp</dimen><dimen name="aurora_hvac_bar_height">96dp</dimen><dimen name="aurora_display_corner_radius">32dp</dimen>
    <!-- Components -->
    <dimen name="aurora_button_height">76dp</dimen><dimen name="aurora_icon_button_size">76dp</dimen><dimen name="aurora_fab_size">96dp</dimen>
    <dimen name="aurora_chip_height">64dp</dimen><dimen name="aurora_field_height">88dp</dimen><dimen name="aurora_list_item_height">96dp</dimen>
    <dimen name="aurora_tab_height">88dp</dimen><dimen name="aurora_toolbar_height">96dp</dimen><dimen name="aurora_dialog_width">640dp</dimen>
    <dimen name="aurora_icon_size">40dp</dimen><dimen name="aurora_focus_ring_width">6dp</dimen><dimen name="aurora_focus_ring_offset">4dp</dimen>
    <!-- State layer opacities -->
    <item name="aurora_state_hover" format="float" type="dimen">0.08</item><item name="aurora_state_focus" format="float" type="dimen">0.12</item>
    <item name="aurora_state_pressed" format="float" type="dimen">0.12</item><item name="aurora_state_dragged" format="float" type="dimen">0.16</item>
    <item name="aurora_state_disabled_content" format="float" type="dimen">0.38</item><item name="aurora_state_disabled_container" format="float" type="dimen">0.12</item>
</resources>
'''
    # ---- Compose theme
    hexc = lambda h: '0xFF' + h[1:].upper()
    def scheme(tid, name):
        r = tok['themes'][tid]['roles']; mode = tok['themes'][tid]['mode']
        keys = ['primary','onPrimary','primaryContainer','onPrimaryContainer','secondary','onSecondary','secondaryContainer','onSecondaryContainer','tertiary','onTertiary','tertiaryContainer','onTertiaryContainer','error','onError','errorContainer','onErrorContainer','background','onBackground','surface','onSurface','surfaceVariant','onSurfaceVariant','outline','outlineVariant','inverseSurface','inverseOnSurface','inversePrimary','scrim','surfaceContainerLowest','surfaceContainerLow','surfaceContainer','surfaceContainerHigh','surfaceContainerHighest']
        body = ',\n'.join('    %s = Color(%s)' % (k, hexc(r[k])) for k in keys)
        ex = ',\n'.join('    %s = Color(%s)' % (k, hexc(r[k])) for k in ['success','onSuccess','successContainer','onSuccessContainer','warning','onWarning','warningContainer','onWarningContainer'])
        return ('private val %sScheme = %sColorScheme(\n%s,\n)\nprivate val %sExtras = AuroraExtras(\n%s,\n    focusRing = Color(%s),\n)\n' % (name, 'dark' if mode == 'dark' else 'light', body, name, ex, hexc(r['onPrimaryContainer'])))
    ids = [('aurora-night', 'AuroraNight'), ('aurora-day', 'AuroraDay'), ('drive-comfort', 'Comfort'), ('drive-eco', 'Eco'), ('drive-sport', 'Sport'), ('drive-offroad', 'Offroad'), ('drive-night', 'NightDrive')]
    kt = '''package com.aurora.ivi.ui

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.composed
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.shape.RoundedCornerShape
import com.aurora.ivi.R

/** Aurora AAOS IVI theme — 10" 1920x1080 (1280x720dp). One color scheme per theme; all components read MaterialTheme.colorScheme + LocalAuroraExtras. */
enum class AuroraThemeId { AuroraNight, AuroraDay, Comfort, Eco, Sport, Offroad, NightDrive }

@Immutable
data class AuroraExtras(
    val success: Color, val onSuccess: Color, val successContainer: Color, val onSuccessContainer: Color,
    val warning: Color, val onWarning: Color, val warningContainer: Color, val onWarningContainer: Color,
    /** Rotary / keyboard focus ring: onPrimaryContainer, so it always matches the theme hue. */
    val focusRing: Color,
)
val LocalAuroraExtras = staticCompositionLocalOf<AuroraExtras> { error("Wrap content in AuroraTheme") }
val LocalAuroraCondensed = staticCompositionLocalOf { false }

'''
    for tid, n in ids: kt += scheme(tid, n) + '\n'
    kt += '''val Roboto = FontFamily(Font(R.font.roboto_regular, FontWeight.W400), Font(R.font.roboto_medium, FontWeight.W500))
val RobotoCondensed = FontFamily(Font(R.font.roboto_condensed_regular, FontWeight.W400), Font(R.font.roboto_condensed_medium, FontWeight.W500))

/** Type scale (sp). Pass condensed = true to AuroraTheme to switch the whole app to Roboto Condensed. */
object AuroraType {
    private fun s(size: Int, line: Int, w: Int, ls: Double, condensed: Boolean) =
        TextStyle(fontFamily = if (condensed) RobotoCondensed else Roboto, fontSize = size.sp, lineHeight = line.sp, fontWeight = FontWeight(w), letterSpacing = ls.sp)
'''
    for name, cls, size, line, wt, ls, sample in TYPE:
        prop = name[0].lower() + name.replace(' ', '')[1:]
        kt += '    val %s: TextStyle @Composable get() = s(%d, %d, %d, %s, LocalAuroraCondensed.current)\n' % (prop, size, line, wt, ls)
    kt += '''}

private val AuroraShapes = Shapes(
    extraSmall = RoundedCornerShape(8.dp), small = RoundedCornerShape(12.dp), medium = RoundedCornerShape(16.dp),
    large = RoundedCornerShape(24.dp), extraLarge = RoundedCornerShape(28.dp),
)

@Composable
fun AuroraTheme(theme: AuroraThemeId? = null, condensed: Boolean = false, content: @Composable () -> Unit) {
    val id = theme ?: if (isSystemInDarkTheme()) AuroraThemeId.AuroraNight else AuroraThemeId.AuroraDay
    val (scheme, extras) = when (id) {
        AuroraThemeId.AuroraNight -> AuroraNightScheme to AuroraNightExtras
        AuroraThemeId.AuroraDay -> AuroraDayScheme to AuroraDayExtras
        AuroraThemeId.Comfort -> ComfortScheme to ComfortExtras
        AuroraThemeId.Eco -> EcoScheme to EcoExtras
        AuroraThemeId.Sport -> SportScheme to SportExtras
        AuroraThemeId.Offroad -> OffroadScheme to OffroadExtras
        AuroraThemeId.NightDrive -> NightDriveScheme to NightDriveExtras
    }
    CompositionLocalProvider(LocalAuroraExtras provides extras, LocalAuroraCondensed provides condensed, LocalMinimumInteractiveComponentSize provides 76.dp) {
        val t = AuroraType
        MaterialTheme(
            colorScheme = scheme, shapes = AuroraShapes,
            typography = Typography(
                displayLarge = t.display, headlineLarge = t.headlineLarge, headlineMedium = t.headlineMedium, headlineSmall = t.headlineSmall,
                titleLarge = t.titleLarge, titleMedium = t.titleMedium, titleSmall = t.titleSmall,
                bodyLarge = t.bodyLarge, bodyMedium = t.bodyMedium, bodySmall = t.bodySmall,
                labelLarge = t.labelLarge, labelMedium = t.labelMedium, labelSmall = t.labelSmall),
            content = content,
        )
    }
}

/** Rotary / keyboard focus ring: 6dp stroke, 4dp gap outside the component, in the theme's focus color. */
fun Modifier.auroraFocusRing(focused: Boolean, cornerRadius: Dp): Modifier = composed {
    val ring = LocalAuroraExtras.current.focusRing
    if (!focused) this else drawWithContent {
        drawContent()
        val gap = 4.dp.toPx(); val w = 6.dp.toPx(); val o = gap + w / 2
        drawRoundRect(ring, Offset(-o, -o), Size(size.width + 2 * o, size.height + 2 * o), CornerRadius(cornerRadius.toPx() + o), style = Stroke(w))
    }
}
'''
    f['compose/AuroraTheme.kt'] = kt
    return f

def build_kit(tok, TYPE):
    files = dict(theme_files(tok, TYPE))
    for c in COMPONENTS.values():
        for p, content in c['files'].items(): files[p] = content
    comps = {cid: {'name': c['name'], 'section': c['section'], 'groups': c['groups']} for cid, c in COMPONENTS.items()}
    return files, comps
