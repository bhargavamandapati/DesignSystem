package com.ivi.designsystem.components

import androidx.compose.foundation.*
import androidx.compose.foundation.interaction.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import com.ivi.designsystem.*


/** 96dp (1-line) / 120dp (2-line) / 144dp (3-line). Selected = primary @16% over surfaceContainer. Focus ring inset. */
@Composable
fun IviListItem(
    primary: String, modifier: Modifier = Modifier, secondary: String? = null, selected: Boolean = false, enabled: Boolean = true,
    leading: (@Composable () -> Unit)? = null, trailing: (@Composable () -> Unit)? = null, onClick: () -> Unit = {},
) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    val bg = if (selected) cs.primary.copy(0.16f).compositeOver(cs.surfaceContainer) else cs.surfaceContainer
    ListItem(
        headlineContent = { Text(primary, style = IviType.bodyLarge) },
        supportingContent = secondary?.let { { Text(it, style = IviType.bodyMedium) } },
        leadingContent = leading, trailingContent = trailing,
        colors = ListItemDefaults.colors(containerColor = bg, headlineColor = cs.onSurface, supportingColor = cs.onSurfaceVariant,
            disabledHeadlineColor = cs.onSurface.copy(0.38f), disabledLeadingIconColor = cs.onSurface.copy(0.38f)),
        modifier = modifier.heightIn(min = if (secondary == null) 96.dp else 120.dp)
            .then(if (focused) Modifier.border(6.dp, LocalIviExtras.current.focusRing) else Modifier)
            .clickable(enabled = enabled, interactionSource = interaction, indication = LocalIndication.current, onClick = onClick),
    )
}
