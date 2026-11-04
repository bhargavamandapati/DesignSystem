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


/** Linear 8dp (radius 4), circular 72dp / stroke 8dp. Show a spinner after 300 ms, keep it >= 600 ms. */
@Composable
fun IviLinearProgress(progress: (() -> Float)?, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    if (progress != null) LinearProgressIndicator(progress, modifier.height(8.dp), cs.primary, cs.secondaryContainer, gapSize = 0.dp, drawStopIndicator = {})
    else LinearProgressIndicator(modifier.height(8.dp), cs.primary, cs.secondaryContainer)
}

@Composable
fun IviCircularProgress(modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    CircularProgressIndicator(modifier.size(72.dp), cs.primary, 8.dp, cs.secondaryContainer)
}
