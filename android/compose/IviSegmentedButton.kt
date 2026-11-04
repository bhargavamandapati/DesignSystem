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


/** 76dp high, 2dp outline, 2-4 segments, label 26sp. Selected: secondaryContainer. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun IviSegmentedButton(options: List<String>, selectedIndex: Int, onSelect: (Int) -> Unit, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    SingleChoiceSegmentedButtonRow(modifier.heightIn(min = 76.dp)) {
        options.forEachIndexed { i, label ->
            SegmentedButton(
                selected = i == selectedIndex, onClick = { onSelect(i) },
                shape = SegmentedButtonDefaults.itemShape(i, options.size, RoundedCornerShape(38.dp)),
                modifier = Modifier.heightIn(min = 76.dp),
                colors = SegmentedButtonDefaults.colors(
                    activeContainerColor = cs.secondaryContainer, activeContentColor = cs.onSecondaryContainer, activeBorderColor = cs.outline,
                    inactiveContainerColor = Color.Transparent, inactiveContentColor = cs.onSurface, inactiveBorderColor = cs.outline,
                    disabledInactiveContentColor = cs.onSurface.copy(0.38f), disabledInactiveBorderColor = cs.onSurface.copy(0.12f)),
                border = BorderStroke(2.dp, cs.outline),
            ) { Text(label, style = IviType.labelMedium) }
        }
    }
}
