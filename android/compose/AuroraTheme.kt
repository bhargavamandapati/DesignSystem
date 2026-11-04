package com.aurora.ivi.ui

import androidx.compose.foundation.isSystemInDarkTheme
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
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.shape.RoundedCornerShape
import com.aurora.ivi.R

/** Aurora AAOS IVI theme — 10" 1920x1080 (1280x720dp). One color scheme per theme; all components read MaterialTheme.colorScheme + LocalAuroraExtras. */
enum class AuroraThemeId { AuroraNight, AuroraDay, Comfort, Eco, Sport, Offroad, NightDrive }

@Immutable
data class AuroraExtras(
    val success: Color, val onSuccess: Color, val successContainer: Color, val onSuccessContainer: Color,
    val warning: Color, val onWarning: Color, val warningContainer: Color, val onWarningContainer: Color,
    /** Rotary / keyboard focus ring: onPrimaryContainer, so it always matches the theme hue. */
    val focusRing: Color,
)
val LocalAuroraExtras = staticCompositionLocalOf<AuroraExtras> { error("Wrap content in AuroraTheme") }
val LocalAuroraCondensed = staticCompositionLocalOf { false }

private val AuroraNightScheme = darkColorScheme(
    primary = Color(0xFFD0BCFF),
    onPrimary = Color(0xFF381E72),
    primaryContainer = Color(0xFF4F378B),
    onPrimaryContainer = Color(0xFFEADDFF),
    secondary = Color(0xFFCCC2DC),
    onSecondary = Color(0xFF332D41),
    secondaryContainer = Color(0xFF4A4458),
    onSecondaryContainer = Color(0xFFE8DEF8),
    tertiary = Color(0xFFEFB8C8),
    onTertiary = Color(0xFF492532),
    tertiaryContainer = Color(0xFF633B48),
    onTertiaryContainer = Color(0xFFFFD8E4),
    error = Color(0xFFF2B8B5),
    onError = Color(0xFF601410),
    errorContainer = Color(0xFF8C1D18),
    onErrorContainer = Color(0xFFF9DEDC),
    background = Color(0xFF141218),
    onBackground = Color(0xFFE6E0E9),
    surface = Color(0xFF141218),
    onSurface = Color(0xFFE6E0E9),
    surfaceVariant = Color(0xFF49454F),
    onSurfaceVariant = Color(0xFFCAC4D0),
    outline = Color(0xFF9A82DB),
    outlineVariant = Color(0xFF4F378B),
    inverseSurface = Color(0xFFE6E0E9),
    inverseOnSurface = Color(0xFF322F35),
    inversePrimary = Color(0xFF6750A4),
    scrim = Color(0xFF000000),
    surfaceContainerLowest = Color(0xFF0F0D13),
    surfaceContainerLow = Color(0xFF1D1B20),
    surfaceContainer = Color(0xFF211F26),
    surfaceContainerHigh = Color(0xFF2B2930),
    surfaceContainerHighest = Color(0xFF36343B),
)
private val AuroraNightExtras = AuroraExtras(
    success = Color(0xFF7DDB95),
    onSuccess = Color(0xFF00391C),
    successContainer = Color(0xFF115229),
    onSuccessContainer = Color(0xFF99F8AF),
    warning = Color(0xFFFFB870),
    onWarning = Color(0xFF4A2800),
    warningContainer = Color(0xFF6A3C00),
    onWarningContainer = Color(0xFFFFDCBC),
    focusRing = Color(0xFFEADDFF),
)

private val AuroraDayScheme = lightColorScheme(
    primary = Color(0xFF6750A4),
    onPrimary = Color(0xFFFFFFFF),
    primaryContainer = Color(0xFFEADDFF),
    onPrimaryContainer = Color(0xFF21005D),
    secondary = Color(0xFF625B71),
    onSecondary = Color(0xFFFFFFFF),
    secondaryContainer = Color(0xFFE8DEF8),
    onSecondaryContainer = Color(0xFF1D192B),
    tertiary = Color(0xFF7D5260),
    onTertiary = Color(0xFFFFFFFF),
    tertiaryContainer = Color(0xFFFFD8E4),
    onTertiaryContainer = Color(0xFF31111D),
    error = Color(0xFFB3261E),
    onError = Color(0xFFFFFFFF),
    errorContainer = Color(0xFFF9DEDC),
    onErrorContainer = Color(0xFF410E0B),
    background = Color(0xFFFEF7FF),
    onBackground = Color(0xFF1D1B20),
    surface = Color(0xFFFEF7FF),
    onSurface = Color(0xFF1D1B20),
    surfaceVariant = Color(0xFFE7E0EC),
    onSurfaceVariant = Color(0xFF49454F),
    outline = Color(0xFF7F67BE),
    outlineVariant = Color(0xFFD0BCFF),
    inverseSurface = Color(0xFF322F35),
    inverseOnSurface = Color(0xFFF5EFF7),
    inversePrimary = Color(0xFFD0BCFF),
    scrim = Color(0xFF000000),
    surfaceContainerLowest = Color(0xFFFFFFFF),
    surfaceContainerLow = Color(0xFFF7F2FA),
    surfaceContainer = Color(0xFFF3EDF7),
    surfaceContainerHigh = Color(0xFFECE6F0),
    surfaceContainerHighest = Color(0xFFE6E0E9),
)
private val AuroraDayExtras = AuroraExtras(
    success = Color(0xFF1B6E3A),
    onSuccess = Color(0xFFFFFFFF),
    successContainer = Color(0xFFB7F4C6),
    onSuccessContainer = Color(0xFF00210D),
    warning = Color(0xFF8A5100),
    onWarning = Color(0xFFFFFFFF),
    warningContainer = Color(0xFFFFDCBC),
    onWarningContainer = Color(0xFF2C1600),
    focusRing = Color(0xFF21005D),
)

private val ComfortScheme = darkColorScheme(
    primary = Color(0xFFAFC6FF),
    onPrimary = Color(0xFF132F60),
    primaryContainer = Color(0xFF2D4678),
    onPrimaryContainer = Color(0xFFD9E2FF),
    secondary = Color(0xFFBFC6DC),
    onSecondary = Color(0xFF293041),
    secondaryContainer = Color(0xFF3F4759),
    onSecondaryContainer = Color(0xFFDBE2F9),
    tertiary = Color(0xFF86D4D1),
    onTertiary = Color(0xFF003736),
    tertiaryContainer = Color(0xFF00504F),
    onTertiaryContainer = Color(0xFFA2F0EE),
    error = Color(0xFFFFB4AB),
    onError = Color(0xFF690005),
    errorContainer = Color(0xFF93000A),
    onErrorContainer = Color(0xFFFFDAD6),
    background = Color(0xFF121318),
    onBackground = Color(0xFFE2E2E9),
    surface = Color(0xFF121318),
    onSurface = Color(0xFFE2E2E9),
    surfaceVariant = Color(0xFF44474F),
    onSurfaceVariant = Color(0xFFC5C6D0),
    outline = Color(0xFF7890C7),
    outlineVariant = Color(0xFF2D4678),
    inverseSurface = Color(0xFFE2E2E9),
    inverseOnSurface = Color(0xFF2F3036),
    inversePrimary = Color(0xFF455E91),
    scrim = Color(0xFF000000),
    surfaceContainerLowest = Color(0xFF0C0E13),
    surfaceContainerLow = Color(0xFF1A1B20),
    surfaceContainer = Color(0xFF1E1F25),
    surfaceContainerHigh = Color(0xFF282A2F),
    surfaceContainerHighest = Color(0xFF33353A),
)
private val ComfortExtras = AuroraExtras(
    success = Color(0xFF7DDB95),
    onSuccess = Color(0xFF00391C),
    successContainer = Color(0xFF115229),
    onSuccessContainer = Color(0xFF99F8AF),
    warning = Color(0xFFFFB870),
    onWarning = Color(0xFF4A2800),
    warningContainer = Color(0xFF6A3C00),
    onWarningContainer = Color(0xFFFFDCBC),
    focusRing = Color(0xFFD9E2FF),
)

private val EcoScheme = darkColorScheme(
    primary = Color(0xFF8BD5B5),
    onPrimary = Color(0xFF003827),
    primaryContainer = Color(0xFF00513A),
    onPrimaryContainer = Color(0xFFA7F2D0),
    secondary = Color(0xFFB3CCBE),
    onSecondary = Color(0xFF1F352B),
    secondaryContainer = Color(0xFF354B41),
    onSecondaryContainer = Color(0xFFCFE9DA),
    tertiary = Color(0xFFA6CCDF),
    onTertiary = Color(0xFF083544),
    tertiaryContainer = Color(0xFF254B5B),
    onTertiaryContainer = Color(0xFFC1E8FC),
    error = Color(0xFFFFB4AB),
    onError = Color(0xFF690005),
    errorContainer = Color(0xFF93000A),
    onErrorContainer = Color(0xFFFFDAD6),
    background = Color(0xFF0F1512),
    onBackground = Color(0xFFDEE4DF),
    surface = Color(0xFF0F1512),
    onSurface = Color(0xFFDEE4DF),
    surfaceVariant = Color(0xFF404944),
    onSurfaceVariant = Color(0xFFBFC9C2),
    outline = Color(0xFF569E80),
    outlineVariant = Color(0xFF00513A),
    inverseSurface = Color(0xFFDEE4DF),
    inverseOnSurface = Color(0xFF2C322E),
    inversePrimary = Color(0xFF1D6B50),
    scrim = Color(0xFF000000),
    surfaceContainerLowest = Color(0xFF0A0F0D),
    surfaceContainerLow = Color(0xFF171D1A),
    surfaceContainer = Color(0xFF1B211E),
    surfaceContainerHigh = Color(0xFF252B28),
    surfaceContainerHighest = Color(0xFF303633),
)
private val EcoExtras = AuroraExtras(
    success = Color(0xFF7DDB95),
    onSuccess = Color(0xFF00391C),
    successContainer = Color(0xFF115229),
    onSuccessContainer = Color(0xFF99F8AF),
    warning = Color(0xFFFFB870),
    onWarning = Color(0xFF4A2800),
    warningContainer = Color(0xFF6A3C00),
    onWarningContainer = Color(0xFFFFDCBC),
    focusRing = Color(0xFFA7F2D0),
)

private val SportScheme = darkColorScheme(
    primary = Color(0xFFFFB2BF),
    onPrimary = Color(0xFF660028),
    primaryContainer = Color(0xFF90003B),
    onPrimaryContainer = Color(0xFFFFD9DE),
    secondary = Color(0xFFF5B7B0),
    onSecondary = Color(0xFF4C2521),
    secondaryContainer = Color(0xFF673B36),
    onSecondaryContainer = Color(0xFFFFDAD6),
    tertiary = Color(0xFFFFB596),
    onTertiary = Color(0xFF52230C),
    tertiaryContainer = Color(0xFF6D3820),
    onTertiaryContainer = Color(0xFFFFDBCD),
    error = Color(0xFFFF6B5E),
    onError = Color(0xFF4B0A05),
    errorContainer = Color(0xFF93000A),
    onErrorContainer = Color(0xFFFFDAD6),
    background = Color(0xFF1D1012),
    onBackground = Color(0xFFF7DCDF),
    surface = Color(0xFF1D1012),
    onSurface = Color(0xFFF7DCDF),
    surfaceVariant = Color(0xFF574145),
    onSurfaceVariant = Color(0xFFDDBFC3),
    outline = Color(0xFFFF4D81),
    outlineVariant = Color(0xFF90003B),
    inverseSurface = Color(0xFFF7DCDF),
    inverseOnSurface = Color(0xFF3C2C2F),
    inversePrimary = Color(0xFFBC004F),
    scrim = Color(0xFF000000),
    surfaceContainerLowest = Color(0xFF170B0D),
    surfaceContainerLow = Color(0xFF26181A),
    surfaceContainer = Color(0xFF2A1C1E),
    surfaceContainerHigh = Color(0xFF362628),
    surfaceContainerHighest = Color(0xFF413033),
)
private val SportExtras = AuroraExtras(
    success = Color(0xFF7DDB95),
    onSuccess = Color(0xFF00391C),
    successContainer = Color(0xFF115229),
    onSuccessContainer = Color(0xFF99F8AF),
    warning = Color(0xFFFFB870),
    onWarning = Color(0xFF4A2800),
    warningContainer = Color(0xFF6A3C00),
    onWarningContainer = Color(0xFFFFDCBC),
    focusRing = Color(0xFFFFD9DE),
)

private val OffroadScheme = darkColorScheme(
    primary = Color(0xFFFCB974),
    onPrimary = Color(0xFF492900),
    primaryContainer = Color(0xFF693C00),
    onPrimaryContainer = Color(0xFFFFDCBD),
    secondary = Color(0xFFE1C1A3),
    onSecondary = Color(0xFF402C18),
    secondaryContainer = Color(0xFF59422C),
    onSecondaryContainer = Color(0xFFFEDDBE),
    tertiary = Color(0xFFBFCC9B),
    onTertiary = Color(0xFF2A3410),
    tertiaryContainer = Color(0xFF404B25),
    onTertiaryContainer = Color(0xFFDBE8B5),
    error = Color(0xFFFFB4AB),
    onError = Color(0xFF690005),
    errorContainer = Color(0xFF93000A),
    onErrorContainer = Color(0xFFFFDAD6),
    background = Color(0xFF19120C),
    onBackground = Color(0xFFEEE0D5),
    surface = Color(0xFF19120C),
    onSurface = Color(0xFFEEE0D5),
    surfaceVariant = Color(0xFF50453A),
    onSurfaceVariant = Color(0xFFD5C3B5),
    outline = Color(0xFFBF8445),
    outlineVariant = Color(0xFF693C00),
    inverseSurface = Color(0xFFEEE0D5),
    inverseOnSurface = Color(0xFF372F28),
    inversePrimary = Color(0xFF855317),
    scrim = Color(0xFF000000),
    surfaceContainerLowest = Color(0xFF130D07),
    surfaceContainerLow = Color(0xFF211A14),
    surfaceContainer = Color(0xFF261E18),
    surfaceContainerHigh = Color(0xFF302921),
    surfaceContainerHighest = Color(0xFF3C332C),
)
private val OffroadExtras = AuroraExtras(
    success = Color(0xFF7DDB95),
    onSuccess = Color(0xFF00391C),
    successContainer = Color(0xFF115229),
    onSuccessContainer = Color(0xFF99F8AF),
    warning = Color(0xFFFFB870),
    onWarning = Color(0xFF4A2800),
    warningContainer = Color(0xFF6A3C00),
    onWarningContainer = Color(0xFFFFDCBC),
    focusRing = Color(0xFFFFDCBD),
)

private val NightDriveScheme = darkColorScheme(
    primary = Color(0xFF73B9C9),
    onPrimary = Color(0xFF003037),
    primaryContainer = Color(0xFF00454F),
    onPrimaryContainer = Color(0xFF90D1E0),
    secondary = Color(0xFF9DB3B8),
    onSecondary = Color(0xFF192E32),
    secondaryContainer = Color(0xFF2D4146),
    onSecondaryContainer = Color(0xFFB4CBD1),
    tertiary = Color(0xFFA6ADCF),
    onTertiary = Color(0xFF212944),
    tertiaryContainer = Color(0xFF363D59),
    onTertiaryContainer = Color(0xFFC2C6E0),
    error = Color(0xFFE09E96),
    onError = Color(0xFF5C0004),
    errorContainer = Color(0xFF810009),
    onErrorContainer = Color(0xFFE0C0BC),
    background = Color(0xFF0A0E10),
    onBackground = Color(0xFFC3C8CA),
    surface = Color(0xFF0A0E10),
    onSurface = Color(0xFFC3C8CA),
    surfaceVariant = Color(0xFF2D3436),
    onSurfaceVariant = Color(0xFFA8B0B3),
    outline = Color(0xFF438C9B),
    outlineVariant = Color(0xFF004651),
    inverseSurface = Color(0xFFC3C8CA),
    inverseOnSurface = Color(0xFF262B2D),
    inversePrimary = Color(0xFF005C69),
    scrim = Color(0xFF000000),
    surfaceContainerLowest = Color(0xFF060B0C),
    surfaceContainerLow = Color(0xFF111516),
    surfaceContainer = Color(0xFF131818),
    surfaceContainerHigh = Color(0xFF1B1F20),
    surfaceContainerHighest = Color(0xFF232728),
)
private val NightDriveExtras = AuroraExtras(
    success = Color(0xFF6EC183),
    onSuccess = Color(0xFF003219),
    successContainer = Color(0xFF0F4824),
    onSuccessContainer = Color(0xFF87DA9A),
    warning = Color(0xFFE0A263),
    onWarning = Color(0xFF412300),
    warningContainer = Color(0xFF5D3500),
    onWarningContainer = Color(0xFFE0C2A5),
    focusRing = Color(0xFF90D1E0),
)

val Roboto = FontFamily(Font(R.font.roboto_regular, FontWeight.W400), Font(R.font.roboto_medium, FontWeight.W500))
val RobotoCondensed = FontFamily(Font(R.font.roboto_condensed_regular, FontWeight.W400), Font(R.font.roboto_condensed_medium, FontWeight.W500))

/** Type scale (sp). Pass condensed = true to AuroraTheme to switch the whole app to Roboto Condensed. */
object AuroraType {
    private fun s(size: Int, line: Int, w: Int, ls: Double, condensed: Boolean) =
        TextStyle(fontFamily = if (condensed) RobotoCondensed else Roboto, fontSize = size.sp, lineHeight = line.sp, fontWeight = FontWeight(w), letterSpacing = ls.sp)
    val display: TextStyle @Composable get() = s(56, 64, 400, -0.25, LocalAuroraCondensed.current)
    val headlineLarge: TextStyle @Composable get() = s(40, 48, 400, 0, LocalAuroraCondensed.current)
    val headlineMedium: TextStyle @Composable get() = s(36, 44, 400, 0, LocalAuroraCondensed.current)
    val headlineSmall: TextStyle @Composable get() = s(32, 40, 400, 0, LocalAuroraCondensed.current)
    val titleLarge: TextStyle @Composable get() = s(32, 40, 500, 0, LocalAuroraCondensed.current)
    val titleMedium: TextStyle @Composable get() = s(28, 36, 500, 0.15, LocalAuroraCondensed.current)
    val titleSmall: TextStyle @Composable get() = s(24, 32, 500, 0.1, LocalAuroraCondensed.current)
    val bodyLarge: TextStyle @Composable get() = s(28, 36, 400, 0.3, LocalAuroraCondensed.current)
    val bodyMedium: TextStyle @Composable get() = s(24, 32, 400, 0.25, LocalAuroraCondensed.current)
    val bodySmall: TextStyle @Composable get() = s(20, 28, 400, 0.4, LocalAuroraCondensed.current)
    val labelLarge: TextStyle @Composable get() = s(28, 36, 500, 0.1, LocalAuroraCondensed.current)
    val labelMedium: TextStyle @Composable get() = s(24, 32, 500, 0.5, LocalAuroraCondensed.current)
    val labelSmall: TextStyle @Composable get() = s(20, 28, 500, 0.5, LocalAuroraCondensed.current)
}

private val AuroraShapes = Shapes(
    extraSmall = RoundedCornerShape(8.dp), small = RoundedCornerShape(12.dp), medium = RoundedCornerShape(16.dp),
    large = RoundedCornerShape(24.dp), extraLarge = RoundedCornerShape(28.dp),
)

@Composable
fun AuroraTheme(theme: AuroraThemeId? = null, condensed: Boolean = false, content: @Composable () -> Unit) {
    val id = theme ?: if (isSystemInDarkTheme()) AuroraThemeId.AuroraNight else AuroraThemeId.AuroraDay
    val (scheme, extras) = when (id) {
        AuroraThemeId.AuroraNight -> AuroraNightScheme to AuroraNightExtras
        AuroraThemeId.AuroraDay -> AuroraDayScheme to AuroraDayExtras
        AuroraThemeId.Comfort -> ComfortScheme to ComfortExtras
        AuroraThemeId.Eco -> EcoScheme to EcoExtras
        AuroraThemeId.Sport -> SportScheme to SportExtras
        AuroraThemeId.Offroad -> OffroadScheme to OffroadExtras
        AuroraThemeId.NightDrive -> NightDriveScheme to NightDriveExtras
    }
    CompositionLocalProvider(LocalAuroraExtras provides extras, LocalAuroraCondensed provides condensed, LocalMinimumInteractiveComponentSize provides 76.dp) {
        val t = AuroraType
        MaterialTheme(
            colorScheme = scheme, shapes = AuroraShapes,
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
fun Modifier.auroraFocusRing(focused: Boolean, cornerRadius: Dp): Modifier = composed {
    val ring = LocalAuroraExtras.current.focusRing
    if (!focused) this else drawWithContent {
        drawContent()
        val gap = 4.dp.toPx(); val w = 6.dp.toPx(); val o = gap + w / 2
        drawRoundRect(ring, Offset(-o, -o), Size(size.width + 2 * o, size.height + 2 * o), CornerRadius(cornerRadius.toPx() + o), style = Stroke(w))
    }
}
