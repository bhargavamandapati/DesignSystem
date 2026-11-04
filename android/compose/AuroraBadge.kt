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


/** Number badge 32dp high (min 32 wide), dot 16dp. Phone / Messages only. */
@Composable
fun AuroraBadge(count: Int?, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    if (count == null) Box(modifier.size(16.dp).background(cs.error, androidx.compose.foundation.shape.CircleShape))
    else Badge(modifier.heightIn(min = 32.dp).widthIn(min = 32.dp), containerColor = cs.error, contentColor = cs.onError) { Text("$count", style = AuroraType.labelSmall) }
}
