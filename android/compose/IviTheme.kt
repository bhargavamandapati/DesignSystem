package com.ivi.designsystem

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.composed
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.res.colorResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * 10" 1920x1080 AAOS IVI theme (1280x720dp).
 * Colors come ONLY from common resource names (R.color.color_*). Day/Night = values / values-night; drive modes and other themes are
 * runtime resource overlays (RRO) that override the same names — no theme-specific code or names anywhere.
 */
@Immutable
data class IviExtras(
    val success: Color, val onSuccess: Color, val successContainer: Color, val onSuccessContainer: Color,
    val warning: Color, val onWarning: Color, val warningContainer: Color, val onWarningContainer: Color,
    /** Rotary / keyboard focus ring: onPrimaryContainer, so it always matches the theme hue. */
    val focusRing: Color,
)
val LocalIviExtras = staticCompositionLocalOf<IviExtras> { error("Wrap content in IviTheme") }
val LocalIviCondensed = staticCompositionLocalOf { false }

val Roboto = FontFamily(Font(R.font.roboto_regular, FontWeight.W400), Font(R.font.roboto_medium, FontWeight.W500))
val RobotoCondensed = FontFamily(Font(R.font.roboto_condensed_regular, FontWeight.W400), Font(R.font.roboto_condensed_medium, FontWeight.W500))

/** Type scale (sp). Pass condensed = true to IviTheme to switch the whole app to Roboto Condensed. */
object IviType {
    private fun s(size: Int, line: Int, w: Int, ls: Double, condensed: Boolean) =
        TextStyle(fontFamily = if (condensed) RobotoCondensed else Roboto, fontSize = size.sp, lineHeight = line.sp, fontWeight = FontWeight(w), letterSpacing = ls.sp)
    val display: TextStyle @Composable get() = s(56, 64, 400, -0.25, LocalIviCondensed.current)
    val headlineLarge: TextStyle @Composable get() = s(40, 48, 400, 0, LocalIviCondensed.current)
    val headlineMedium: TextStyle @Composable get() = s(36, 44, 400, 0, LocalIviCondensed.current)
    val headlineSmall: TextStyle @Composable get() = s(32, 40, 400, 0, LocalIviCondensed.current)
    val titleLarge: TextStyle @Composable get() = s(32, 40, 500, 0, LocalIviCondensed.current)
    val titleMedium: TextStyle @Composable get() = s(28, 36, 500, 0.15, LocalIviCondensed.current)
    val titleSmall: TextStyle @Composable get() = s(24, 32, 500, 0.1, LocalIviCondensed.current)
    val bodyLarge: TextStyle @Composable get() = s(28, 36, 400, 0.3, LocalIviCondensed.current)
    val bodyMedium: TextStyle @Composable get() = s(24, 32, 400, 0.25, LocalIviCondensed.current)
    val bodySmall: TextStyle @Composable get() = s(20, 28, 400, 0.4, LocalIviCondensed.current)
    val labelLarge: TextStyle @Composable get() = s(28, 36, 500, 0.1, LocalIviCondensed.current)
    val labelMedium: TextStyle @Composable get() = s(24, 32, 500, 0.5, LocalIviCondensed.current)
    val labelSmall: TextStyle @Composable get() = s(20, 28, 500, 0.5, LocalIviCondensed.current)
}

private val IviShapes = Shapes(
    extraSmall = RoundedCornerShape(8.dp), small = RoundedCornerShape(12.dp), medium = RoundedCornerShape(16.dp),
    large = RoundedCornerShape(24.dp), extraLarge = RoundedCornerShape(28.dp),
)

@Composable
fun IviTheme(condensed: Boolean = false, darkTheme: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
    val colors = if (darkTheme) darkColorScheme(
        primary = colorResource(R.color.color_primary),
        onPrimary = colorResource(R.color.color_on_primary),
        primaryContainer = colorResource(R.color.color_primary_container),
        onPrimaryContainer = colorResource(R.color.color_on_primary_container),
        secondary = colorResource(R.color.color_secondary),
        onSecondary = colorResource(R.color.color_on_secondary),
        secondaryContainer = colorResource(R.color.color_secondary_container),
        onSecondaryContainer = colorResource(R.color.color_on_secondary_container),
        tertiary = colorResource(R.color.color_tertiary),
        onTertiary = colorResource(R.color.color_on_tertiary),
        tertiaryContainer = colorResource(R.color.color_tertiary_container),
        onTertiaryContainer = colorResource(R.color.color_on_tertiary_container),
        error = colorResource(R.color.color_error),
        onError = colorResource(R.color.color_on_error),
        errorContainer = colorResource(R.color.color_error_container),
        onErrorContainer = colorResource(R.color.color_on_error_container),
        background = colorResource(R.color.color_background),
        onBackground = colorResource(R.color.color_on_background),
        surface = colorResource(R.color.color_surface),
        onSurface = colorResource(R.color.color_on_surface),
        surfaceVariant = colorResource(R.color.color_surface_variant),
        onSurfaceVariant = colorResource(R.color.color_on_surface_variant),
        outline = colorResource(R.color.color_outline),
        outlineVariant = colorResource(R.color.color_outline_variant),
        inverseSurface = colorResource(R.color.color_inverse_surface),
        inverseOnSurface = colorResource(R.color.color_inverse_on_surface),
        inversePrimary = colorResource(R.color.color_inverse_primary),
        scrim = colorResource(R.color.color_scrim),
        surfaceContainerLowest = colorResource(R.color.color_surface_container_lowest),
        surfaceContainerLow = colorResource(R.color.color_surface_container_low),
        surfaceContainer = colorResource(R.color.color_surface_container),
        surfaceContainerHigh = colorResource(R.color.color_surface_container_high),
        surfaceContainerHighest = colorResource(R.color.color_surface_container_highest),
    ) else lightColorScheme(
        primary = colorResource(R.color.color_primary),
        onPrimary = colorResource(R.color.color_on_primary),
        primaryContainer = colorResource(R.color.color_primary_container),
        onPrimaryContainer = colorResource(R.color.color_on_primary_container),
        secondary = colorResource(R.color.color_secondary),
        onSecondary = colorResource(R.color.color_on_secondary),
        secondaryContainer = colorResource(R.color.color_secondary_container),
        onSecondaryContainer = colorResource(R.color.color_on_secondary_container),
        tertiary = colorResource(R.color.color_tertiary),
        onTertiary = colorResource(R.color.color_on_tertiary),
        tertiaryContainer = colorResource(R.color.color_tertiary_container),
        onTertiaryContainer = colorResource(R.color.color_on_tertiary_container),
        error = colorResource(R.color.color_error),
        onError = colorResource(R.color.color_on_error),
        errorContainer = colorResource(R.color.color_error_container),
        onErrorContainer = colorResource(R.color.color_on_error_container),
        background = colorResource(R.color.color_background),
        onBackground = colorResource(R.color.color_on_background),
        surface = colorResource(R.color.color_surface),
        onSurface = colorResource(R.color.color_on_surface),
        surfaceVariant = colorResource(R.color.color_surface_variant),
        onSurfaceVariant = colorResource(R.color.color_on_surface_variant),
        outline = colorResource(R.color.color_outline),
        outlineVariant = colorResource(R.color.color_outline_variant),
        inverseSurface = colorResource(R.color.color_inverse_surface),
        inverseOnSurface = colorResource(R.color.color_inverse_on_surface),
        inversePrimary = colorResource(R.color.color_inverse_primary),
        scrim = colorResource(R.color.color_scrim),
        surfaceContainerLowest = colorResource(R.color.color_surface_container_lowest),
        surfaceContainerLow = colorResource(R.color.color_surface_container_low),
        surfaceContainer = colorResource(R.color.color_surface_container),
        surfaceContainerHigh = colorResource(R.color.color_surface_container_high),
        surfaceContainerHighest = colorResource(R.color.color_surface_container_highest),
    )
    val extras = IviExtras(
        success = colorResource(R.color.color_success),
        onSuccess = colorResource(R.color.color_on_success),
        successContainer = colorResource(R.color.color_success_container),
        onSuccessContainer = colorResource(R.color.color_on_success_container),
        warning = colorResource(R.color.color_warning),
        onWarning = colorResource(R.color.color_on_warning),
        warningContainer = colorResource(R.color.color_warning_container),
        onWarningContainer = colorResource(R.color.color_on_warning_container),
        focusRing = colorResource(R.color.color_on_primary_container),
    )
    CompositionLocalProvider(LocalIviExtras provides extras, LocalIviCondensed provides condensed, LocalMinimumInteractiveComponentSize provides 76.dp) {
        val t = IviType
        MaterialTheme(
            colorScheme = colors, shapes = IviShapes,
            typography = Typography(
                displayLarge = t.display, headlineLarge = t.headlineLarge, headlineMedium = t.headlineMedium, headlineSmall = t.headlineSmall,
                titleLarge = t.titleLarge, titleMedium = t.titleMedium, titleSmall = t.titleSmall,
                bodyLarge = t.bodyLarge, bodyMedium = t.bodyMedium, bodySmall = t.bodySmall,
                labelLarge = t.labelLarge, labelMedium = t.labelMedium, labelSmall = t.labelSmall),
            content = content,
        )
    }
}

/** Rotary / keyboard focus ring: 6dp stroke, 4dp gap outside the component, in the theme's focus color. */
fun Modifier.iviFocusRing(focused: Boolean, cornerRadius: Dp): Modifier = composed {
    val ring = LocalIviExtras.current.focusRing
    if (!focused) this else drawWithContent {
        drawContent()
        val gap = 4.dp.toPx(); val w = 6.dp.toPx(); val o = gap + w / 2
        drawRoundRect(ring, Offset(-o, -o), Size(size.width + 2 * o, size.height + 2 * o), CornerRadius(cornerRadius.toPx() + o), style = Stroke(w))
    }
}
