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


enum class IviBannerType { Error, Warning, Success, Info }

/** Radius 20dp, padding 20x28dp, text 26sp, icon 40dp, at most one action. Safety (error) banners never auto-dismiss. */
@Composable
fun IviBanner(type: IviBannerType, message: String, icon: ImageVector, modifier: Modifier = Modifier, action: String? = null, onAction: () -> Unit = {}) {
    val cs = MaterialTheme.colorScheme
    val x = LocalIviExtras.current
    val (bg, fg) = when (type) {
        IviBannerType.Error -> cs.errorContainer to cs.onErrorContainer
        IviBannerType.Warning -> x.warningContainer to x.onWarningContainer
        IviBannerType.Success -> x.successContainer to x.onSuccessContainer
        IviBannerType.Info -> cs.secondaryContainer to cs.onSecondaryContainer
    }
    Row(modifier.fillMaxWidth().background(bg, RoundedCornerShape(20.dp)).padding(horizontal = 28.dp, vertical = 20.dp), verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, null, Modifier.size(40.dp), tint = fg)
        Spacer(Modifier.width(20.dp))
        Text(message, Modifier.weight(1f), style = IviType.bodyLarge, color = fg)
        if (action != null) TextButton(onAction, Modifier.heightIn(min = 76.dp), colors = ButtonDefaults.textButtonColors(contentColor = fg)) { Text(action, style = IviType.labelLarge) }
    }
}
