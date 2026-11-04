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
import androidx.compose.ui.draw.clip


/** Track 16dp (radius 8), handle 12x64dp, row 76dp. Focused handle uses the theme focus color. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun IviSlider(value: Float, onValueChange: (Float) -> Unit, modifier: Modifier = Modifier, valueRange: ClosedFloatingPointRange<Float> = 0f..1f, enabled: Boolean = true) {
    val cs = MaterialTheme.colorScheme
    val interaction = remember { MutableInteractionSource() }
    val focused by interaction.collectIsFocusedAsState()
    Slider(
        value, onValueChange, modifier.heightIn(min = 76.dp), enabled, valueRange, interactionSource = interaction,
        colors = SliderDefaults.colors(thumbColor = cs.primary, activeTrackColor = cs.primary, inactiveTrackColor = cs.secondaryContainer,
            disabledThumbColor = cs.onSurface.copy(0.38f), disabledActiveTrackColor = cs.onSurface.copy(0.38f), disabledInactiveTrackColor = cs.onSurface.copy(0.12f)),
        thumb = { Box(Modifier.size(12.dp, 64.dp).clip(RoundedCornerShape(6.dp)).background(if (!enabled) cs.onSurface.copy(0.38f) else if (focused) LocalIviExtras.current.focusRing else cs.primary)) },
        track = { state -> SliderDefaults.Track(state, Modifier.height(16.dp), enabled = enabled, thumbTrackGapSize = 6.dp, trackInsideCornerSize = 8.dp) },
    )
}
