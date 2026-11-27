package io.github.apdelrahman1911.nativecmpkit.ui.navigation

import androidx.compose.runtime.Immutable
import io.github.apdelrahman1911.nativecmpkit.ui.uikit.UIKitImage

/**
 * Represents a tab bar item for the iOS UITabBar used in [AdaptiveNavigationBar].
 *
 * @param title The title of the tab bar item.
 * @param image The image for the tab bar item. See [UIKitImage] for supported types.
 * @param selectedImage Optional image to show when the item is selected.
 */
@Immutable
data class UIKitUITabBarItem(
    val title: String,
    val image: UIKitImage? = null,
    val selectedImage: UIKitImage? = null,
)
