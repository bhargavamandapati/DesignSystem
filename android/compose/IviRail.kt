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


data class RailDestination(val label: String, val icon: ImageVector)

/** 120dp wide, item 112x88dp, active pill 88x40dp, icon 36dp, label 24sp. Place on the trailing edge (right). */
@Composable
fun IviAppRail(destinations: List<RailDestination>, selectedIndex: Int, onSelect: (Int) -> Unit, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    NavigationRail(modifier.width(120.dp), containerColor = cs.surfaceContainerLowest, contentColor = cs.onSurfaceVariant, windowInsets = WindowInsets(0)) {
        Spacer(Modifier.weight(1f))
        destinations.forEachIndexed { i, d ->
            val interaction = remember { MutableInteractionSource() }
            val focused by interaction.collectIsFocusedAsState()
            NavigationRailItem(
                selected = i == selectedIndex, onClick = { onSelect(i) }, interactionSource = interaction,
                modifier = Modifier.size(112.dp, 88.dp).iviFocusRing(focused, 28.dp),
                icon = { Icon(d.icon, null, Modifier.size(36.dp)) },
                label = { Text(d.label, style = IviType.labelMedium) }, alwaysShowLabel = true,
                colors = NavigationRailItemDefaults.colors(
                    selectedIconColor = cs.onSecondaryContainer, selectedTextColor = cs.onSurface, indicatorColor = cs.secondaryContainer,
                    unselectedIconColor = cs.onSurfaceVariant, unselectedTextColor = cs.onSurfaceVariant),
            )
        }
        Spacer(Modifier.weight(1f))
    }
}
