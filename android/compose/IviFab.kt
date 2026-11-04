package com.ivi.designsystem.components

import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsFocusedAsState
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import com.ivi.designsystem.*

/** 96x96dp, radius 28dp, icon 44dp, elevation level 3. One per screen. */
@Composable
fun IviFab(icon: ImageVector, contentDescription: String, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    FloatingActionButton(onClick, modifier.size(96.dp).iviFocusRing(focused, 28.dp), RoundedCornerShape(28.dp),
        cs.primaryContainer, cs.onPrimaryContainer, interactionSource = interaction) { Icon(icon, contentDescription, Modifier.size(44.dp)) }
}

@Composable
fun IviExtendedFab(text: String, icon: ImageVector, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    ExtendedFloatingActionButton(onClick, modifier.height(96.dp).iviFocusRing(focused, 28.dp), RoundedCornerShape(28.dp),
        cs.primaryContainer, cs.onPrimaryContainer, interactionSource = interaction) {
        Icon(icon, null, Modifier.size(44.dp)); Spacer(Modifier.width(16.dp)); Text(text, style = IviType.labelLarge)
    }
}
