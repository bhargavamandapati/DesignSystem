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


/** Width 640dp (max 840), radius 28dp, padding 40dp, title 36sp, body 28sp (<= 120 chars while driving), max 2 actions while driving. */
@Composable
fun AuroraDialog(title: String, body: String, confirm: String, onConfirm: () -> Unit, dismiss: String?, onDismiss: () -> Unit, icon: ImageVector? = null) {
    val cs = MaterialTheme.colorScheme
    AlertDialog(
        onDismissRequest = onDismiss, shape = RoundedCornerShape(28.dp), containerColor = cs.surfaceContainerHigh,
        iconContentColor = cs.secondary, titleContentColor = cs.onSurface, textContentColor = cs.onSurfaceVariant,
        icon = icon?.let { { Icon(it, null, Modifier.size(48.dp)) } },
        title = { Text(title, style = AuroraType.headlineMedium) },
        text = { Text(body, style = AuroraType.bodyLarge) },
        modifier = Modifier.widthIn(min = 640.dp, max = 840.dp),
        confirmButton = { AuroraFilledButton(confirm, onConfirm) },
        dismissButton = dismiss?.let { { AuroraTextButton(it, onDismiss) } },
    )
}
