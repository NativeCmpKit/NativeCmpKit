package io.github.apdelrahman1911.nativecmpkit.picker

import androidx.compose.runtime.Composable
import io.github.apdelrahman1911.nativecmpkit.core.ExperimentalNativeCmpKitApi
import io.github.apdelrahman1911.nativecmpkit.io.KmpFile

/** A download request is observable; a browser's eventual download completion is not. */
sealed interface FileSaverEvent {
    data class Saved(val file: KmpFile) : FileSaverEvent
    data object Cancelled : FileSaverEvent
    data class DownloadStarted(val fileName: String) : FileSaverEvent
    data class Failed(val error: FilePickerException) : FileSaverEvent
}

enum class FileSaverCapability {
    /** Can return the selected destination after a successful write. */
    SaveDestination,
    /** Can request a download, not observe its acceptance, final path, success or cancellation. */
    DownloadOnly,
}

/** Availability, not a grant: a supported browser save API can still reject user activation/access. */
expect fun fileSaverCapability(): FileSaverCapability

/**
 * Preferred portable saver API. Exactly one event is delivered for a completed launch while
 * composed. Browser fallback delivers [FileSaverEvent.DownloadStarted], never a fictitious saved
 * file or cancellation. Disposal cancels delivery; a native OS sheet may still require dismissal.
 */
@ExperimentalNativeCmpKitApi
@Composable
expect fun rememberFileSaverEventLauncher(
    settings: FilePickerSettings = defaultFilePickerSettings(),
    onEvent: (FileSaverEvent) -> Unit,
): FileSaverLauncher
