package com.ivi.designsystem.components

import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsFocusedAsState
import androidx.compose.foundation.layout.size
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import com.ivi.designsystem.*

enum class IviIconButtonStyle { Standard, Filled, Tonal, Outlined }

/** 76x76dp hit area, 40dp glyph. States: hovered 8%, focused 12% + 6dp ring, pressed 12%, disabled 38%. */
@Composable
fun IviIconButton(
    icon: ImageVector, contentDescription: String, onClick: () -> Unit,
    modifier: Modifier = Modifier, style: IviIconButtonStyle = IviIconButtonStyle.Standard, enabled: Boolean = true,
) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    val m = modifier.size(76.dp).iviFocusRing(focused, 38.dp)
    when (style) {
        IviIconButtonStyle.Standard -> IconButton(onClick, m, enabled, interactionSource = interaction,
            colors = IconButtonDefaults.iconButtonColors(contentColor = cs.onSurfaceVariant, disabledContentColor = cs.onSurface.copy(0.38f))) { Icon(icon, contentDescription, Modifier.size(40.dp)) }
        IviIconButtonStyle.Filled -> FilledIconButton(onClick, m, enabled, interactionSource = interaction,
            colors = IconButtonDefaults.filledIconButtonColors(cs.primary, cs.onPrimary, cs.onSurface.copy(0.12f), cs.onSurface.copy(0.38f))) { Icon(icon, contentDescription, Modifier.size(40.dp)) }
        IviIconButtonStyle.Tonal -> FilledTonalIconButton(onClick, m, enabled, interactionSource = interaction,
            colors = IconButtonDefaults.filledTonalIconButtonColors(cs.secondaryContainer, cs.onSecondaryContainer, cs.onSurface.copy(0.12f), cs.onSurface.copy(0.38f))) { Icon(icon, contentDescription, Modifier.size(40.dp)) }
        IviIconButtonStyle.Outlined -> OutlinedIconButton(onClick, m, enabled, interactionSource = interaction,
            border = androidx.compose.foundation.BorderStroke(2.dp, if (enabled) cs.outline else cs.onSurface.copy(0.12f)),
            colors = IconButtonDefaults.outlinedIconButtonColors(contentColor = cs.onSurfaceVariant, disabledContentColor = cs.onSurface.copy(0.38f))) { Icon(icon, contentDescription, Modifier.size(40.dp)) }
    }
}

/** Toggle (e.g. HVAC seat heat): checked = primaryContainer / onPrimaryContainer. */
@Composable
fun IviToggleIconButton(checked: Boolean, onCheckedChange: (Boolean) -> Unit, icon: ImageVector, contentDescription: String, modifier: Modifier = Modifier, enabled: Boolean = true) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    FilledIconToggleButton(checked, onCheckedChange, modifier.size(76.dp).iviFocusRing(focused, 38.dp), enabled, interactionSource = interaction,
        colors = IconButtonDefaults.filledIconToggleButtonColors(
            containerColor = androidx.compose.ui.graphics.Color.Transparent, contentColor = cs.onSurfaceVariant,
            checkedContainerColor = cs.primaryContainer, checkedContentColor = cs.onPrimaryContainer,
            disabledContainerColor = cs.onSurface.copy(0.12f), disabledContentColor = cs.onSurface.copy(0.38f))) { Icon(icon, contentDescription, Modifier.size(40.dp)) }
}
