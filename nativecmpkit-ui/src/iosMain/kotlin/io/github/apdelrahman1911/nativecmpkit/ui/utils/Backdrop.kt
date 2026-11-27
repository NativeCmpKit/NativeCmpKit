package io.github.apdelrahman1911.nativecmpkit.ui.utils

import androidx.compose.runtime.staticCompositionLocalOf
import com.kyant.backdrop.Backdrop
import io.github.apdelrahman1911.nativecmpkit.ui.button.LiquidGlassButton

/**
 * CompositionLocal to provide a [Backdrop] instance for Liquid Glass buttons.
 *
 * When provided, [LiquidGlassButton] will use the backdrop library's real glass effects
 * (vibrancy, blur, lens) for authentic Liquid Glass rendering.
 */
val LocalBackdrop = staticCompositionLocalOf<Backdrop?> { null }
