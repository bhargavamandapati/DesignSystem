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


/** ring 44dp, border 3dp, dot 22dp. Glyph is scaled to match the spec; the clickable box is 76x76dp. */
@Composable
fun AuroraRadioButton(selected: Boolean, onClick: (() -> Unit)?, modifier: Modifier = Modifier, enabled: Boolean = true) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    Box(modifier.size(76.dp).auroraFocusRing(focused, 38.dp), contentAlignment = Alignment.Center) {
        RadioButton(selected, onClick, Modifier.scale(1.8f), enabled, interactionSource = interaction,
            colors = RadioButtonDefaults.colors(selectedColor = cs.primary, unselectedColor = cs.outline, disabledSelectedColor = cs.onSurface.copy(0.38f), disabledUnselectedColor = cs.onSurface.copy(0.38f)))
    }
}
