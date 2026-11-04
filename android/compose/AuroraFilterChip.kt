package com.aurora.ivi.ui.components

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
import com.aurora.ivi.ui.*


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
