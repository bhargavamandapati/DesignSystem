package com.aurora.ivi.ui.components

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

/** Destructive button — 76dp high, min 120dp, radius 38dp (full), Label Large 28sp. States: enabled, hovered 8%, focused 12% + 6dp ring, pressed 12%, disabled 12%/38%. */
@Composable
fun AuroraDestructiveButton(
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
    Button(
        onClick = onClick,
        modifier = modifier
            .heightIn(min = 76.dp).widthIn(min = 120.dp)
            .auroraFocusRing(focused, 38.dp),
        enabled = enabled,
        shape = shape,
        colors = ButtonDefaults.buttonColors(containerColor = cs.error, contentColor = cs.onError, disabledContainerColor = cs.onSurface.copy(alpha = 0.12f), disabledContentColor = cs.onSurface.copy(alpha = 0.38f)),
        contentPadding = PaddingValues(start = if (icon != null) 32.dp else 40.dp, end = 40.dp),
        interactionSource = interaction,
    ) {
        if (icon != null) { Icon(icon, null, Modifier.size(40.dp)); Spacer(Modifier.width(12.dp)) }
        Text(text, style = AuroraType.labelLarge)
    }
}
