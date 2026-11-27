package io.github.apdelrahman1911.nativecmpkit.picker

import androidx.compose.runtime.Composable
import io.github.apdelrahman1911.nativecmpkit.core.ExperimentalNativeCmpKitApi

actual fun fileSaverCapability(): FileSaverCapability = FileSaverCapability.SaveDestination

@ExperimentalNativeCmpKitApi
@Composable
actual fun rememberFileSaverEventLauncher(
    settings: FilePickerSettings,
    onEvent: (FileSaverEvent) -> Unit,
): FileSaverLauncher = rememberFileSaverLauncher(
    settings = settings,
    onError = { onEvent(FileSaverEvent.Failed(it)) },
    onResult = { onEvent(if (it == null) FileSaverEvent.Cancelled else FileSaverEvent.Saved(it)) },
)
