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
