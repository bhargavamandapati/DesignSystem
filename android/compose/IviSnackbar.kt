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


/** Min height 92dp, radius 16dp, width 640dp, text 26sp, action 76dp high. No action while driving. */
@Composable
fun IviSnackbarHost(state: SnackbarHostState, modifier: Modifier = Modifier) {
    val cs = MaterialTheme.colorScheme
    SnackbarHost(state, modifier) { data ->
        Snackbar(
            data, Modifier.widthIn(max = 640.dp).heightIn(min = 92.dp), shape = RoundedCornerShape(16.dp),
            containerColor = cs.inverseSurface, contentColor = cs.inverseOnSurface, actionColor = cs.inversePrimary,
        )
    }
}
