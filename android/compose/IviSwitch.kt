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


/** Track 104x64dp, thumb 32dp (off) / 48dp (on) with check icon, row hit area 76dp. M3 Switch is 52x32, so it is scaled 2x inside a fixed box. */
@Composable
fun IviSwitch(checked: Boolean, onCheckedChange: (Boolean) -> Unit, modifier: Modifier = Modifier, enabled: Boolean = true) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    Box(modifier.size(width = 104.dp, height = 76.dp).iviFocusRing(focused, 38.dp), contentAlignment = Alignment.Center) {
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
