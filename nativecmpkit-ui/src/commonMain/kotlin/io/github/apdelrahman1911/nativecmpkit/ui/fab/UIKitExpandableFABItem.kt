package io.github.apdelrahman1911.nativecmpkit.ui.fab

import io.github.apdelrahman1911.nativecmpkit.ui.uikit.UIKitImage

/**
 * Represents an item in the expandable FAB menu for iOS.
 *
 * On iOS, each item is rendered as a [UIButton] with Liquid Glass effect inside a
 * [UIGlassEffectContainerView].
 *
 * @param title The label for the FAB item.
 * @param image The image for the FAB item. See [UIKitImage] for supported types.
 */
internal data class UIKitExpandableFABItem(
    val title: String,
    val image: UIKitImage? = null,
)
