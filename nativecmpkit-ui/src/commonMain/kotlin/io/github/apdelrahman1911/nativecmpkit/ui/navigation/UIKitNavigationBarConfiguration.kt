package io.github.apdelrahman1911.nativecmpkit.ui.navigation

import androidx.compose.runtime.Immutable
import androidx.compose.ui.graphics.Color

/**
 * Configuration for the iOS UINavigationBar appearance in [AdaptiveTopBar].
 *
 * Color properties default to [Color.Unspecified], which means the native iOS default
 * colors will be used. Only properties explicitly set by the caller are applied.
 *
 * @param prefersLargeTitles Whether the navigation bar should display large titles.
 * @param isTranslucent Whether the navigation bar is translucent.
 * @param titleColor The color of the navigation bar title text. When [Color.Unspecified],
 *   the default iOS title color is used.
 * @param tintColor The tint of the bar button items. When [Color.Unspecified], the bar keeps its current tint.
 */
@Immutable
data class UIKitNavigationBarConfiguration(
    val prefersLargeTitles: Boolean = false,
    val isTranslucent: Boolean = true,
    val titleColor: Color = Color.Unspecified,
    val tintColor: Color = Color.Unspecified,
)
