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


/** 88dp high, radius 12dp, 2dp border, input 28sp, floating label 28 -> 20sp. Border: outline -> primary (focused) -> error. */
@Composable
fun AuroraTextField(value: String, onValueChange: (String) -> Unit, label: String, modifier: Modifier = Modifier, enabled: Boolean = true, isError: Boolean = false, supportingText: String? = null) {
    val cs = MaterialTheme.colorScheme
    OutlinedTextField(
        value, onValueChange, modifier.heightIn(min = 88.dp), enabled = enabled, isError = isError,
        label = { Text(label, style = AuroraType.bodyLarge) },
        supportingText = supportingText?.let { { Text(it, style = AuroraType.bodySmall) } },
        textStyle = AuroraType.bodyLarge,
        shape = RoundedCornerShape(12.dp),
        colors = OutlinedTextFieldDefaults.colors(
            focusedBorderColor = cs.primary, unfocusedBorderColor = cs.outline, errorBorderColor = cs.error, disabledBorderColor = cs.onSurface.copy(0.12f),
            focusedLabelColor = cs.primary, unfocusedLabelColor = cs.onSurfaceVariant, errorLabelColor = cs.error,
            focusedTextColor = cs.onSurface, unfocusedTextColor = cs.onSurface, disabledTextColor = cs.onSurface.copy(0.38f)),
    )
}

/** Search bar: 88dp, fully rounded, surfaceContainerHigh. While driving replace with a voice button. */
@Composable
fun AuroraSearchBar(query: String, onQueryChange: (String) -> Unit, modifier: Modifier = Modifier, onVoice: () -> Unit = {}) {
    val cs = MaterialTheme.colorScheme
    TextField(
        query, onQueryChange, modifier.heightIn(min = 88.dp).fillMaxWidth(), singleLine = true, textStyle = AuroraType.bodyLarge,
        placeholder = { Text("Search music, places, contacts", style = AuroraType.bodyLarge) },
        leadingIcon = { Icon(androidx.compose.material.icons.Icons.Filled.Search, null, Modifier.size(40.dp)) },
        trailingIcon = { IconButton(onVoice, Modifier.size(76.dp)) { Icon(androidx.compose.material.icons.Icons.Filled.Mic, "Voice", Modifier.size(40.dp)) } },
        shape = RoundedCornerShape(44.dp),
        colors = TextFieldDefaults.colors(focusedContainerColor = cs.surfaceContainerHigh, unfocusedContainerColor = cs.surfaceContainerHigh,
            focusedIndicatorColor = Color.Transparent, unfocusedIndicatorColor = Color.Transparent, unfocusedPlaceholderColor = cs.onSurfaceVariant),
    )
}
