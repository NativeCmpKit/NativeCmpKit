// Modified for nativeCmpkit (2026-10-24): correctness, lifecycle, testing and build hardening.
package io.github.apdelrahman1911.nativecmpkit.share

import androidx.compose.runtime.Composable
import androidx.compose.runtime.Stable
import io.github.apdelrahman1911.nativecmpkit.core.ExperimentalNativeCmpKitApi

/**
 * Creates and remembers a [ShareLauncher] for sharing content using the platform's native
 * share mechanism.
 *
 * On Android, this opens `Intent.createChooser()`. On iOS, it presents a
 * `UIActivityViewController`. On Desktop, it uses the native macOS sheet or a safe text/URL clipboard fallback.
 * On Web, it uses the `navigator.share()` API with a clipboard fallback.
 *
 * @param onResult Legacy stage callback; Android presentation is not completion. Prefer
 * [rememberShareOutcomeLauncher] for explicit stage/failure semantics.
 */
@ExperimentalNativeCmpKitApi
@Composable
expect fun rememberShareLauncher(
    onResult: (ShareResult) -> Unit,
): ShareLauncher

/**
 * A launcher that presents the platform's native share sheet for sharing content.
 *
 * Create an instance using [rememberShareLauncher].
 *
 * @param onLaunch Called when [launch] is invoked, with the [ShareContent] to share.
 */
@ExperimentalNativeCmpKitApi
@Stable
expect class ShareLauncher(
    onLaunch: (ShareContent) -> Unit,
) {
    /**
     * Launch the share sheet with the given [content].
     *
     * @param content The content to share. See [ShareContent] for supported types.
     */
    fun launch(content: ShareContent)
}
