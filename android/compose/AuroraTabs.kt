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


/** 88dp high, label 28sp, 6dp indicator (radius 3dp), 2-4 tabs, divider 2dp in outlineVariant. */
@Composable
fun AuroraTabs(titles: List<String>, selectedIndex: Int, onSelect: (Int) -> Unit, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    PrimaryTabRow(
        selectedTabIndex = selectedIndex, modifier = modifier, containerColor = Color.Transparent, contentColor = cs.primary,
        indicator = { TabRowDefaults.PrimaryIndicator(Modifier.tabIndicatorOffset(selectedIndex), width = 120.dp, height = 6.dp, color = cs.primary, shape = RoundedCornerShape(topStart = 3.dp, topEnd = 3.dp)) },
        divider = { HorizontalDivider(thickness = 2.dp, color = cs.outlineVariant) },
    ) {
        titles.forEachIndexed { i, t ->
            Tab(selected = i == selectedIndex, onClick = { onSelect(i) }, modifier = Modifier.heightIn(min = 88.dp),
                selectedContentColor = cs.primary, unselectedContentColor = cs.onSurfaceVariant,
                text = { Text(t, style = AuroraType.labelLarge) })
        }
    }
}
