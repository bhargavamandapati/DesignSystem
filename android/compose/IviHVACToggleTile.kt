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


/** 112x112dp tile, radius 28dp, icon 44dp, label 20sp. Off: surfaceContainerHighest; On: primaryContainer. */
@Composable
fun IviToggleTile(label: String, icon: ImageVector, checked: Boolean, onCheckedChange: (Boolean) -> Unit, modifier: Modifier = Modifier, enabled: Boolean = true) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    val container = if (!enabled) cs.onSurface.copy(0.12f) else if (checked) cs.primaryContainer else cs.surfaceContainerHighest
    val content = if (!enabled) cs.onSurface.copy(0.38f) else if (checked) cs.onPrimaryContainer else cs.onSurfaceVariant
    Surface(
        checked = checked, onCheckedChange = onCheckedChange, modifier = modifier.size(112.dp).iviFocusRing(focused, 28.dp), enabled = enabled,
        shape = RoundedCornerShape(28.dp), color = container, contentColor = content, interactionSource = interaction,
    ) {
        Column(Modifier.fillMaxSize(), Arrangement.Center, Alignment.CenterHorizontally) {
            Icon(icon, null, Modifier.size(44.dp)); Text(label, style = IviType.labelSmall)
        }
    }
}
