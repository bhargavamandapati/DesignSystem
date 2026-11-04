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
