// Modified for nativeCmpkit (2026-10-24): correctness, lifecycle, testing and build hardening.
package io.github.apdelrahman1911.nativecmpkit.picker

import androidx.compose.runtime.Composable
import androidx.compose.runtime.Stable
import io.github.apdelrahman1911.nativecmpkit.io.KmpFile

@Composable
actual fun rememberFilePickerLauncher(
    type: FilePickerFileType,
    selectionMode: FilePickerSelectionMode,
    settings: FilePickerSettings,
    onResult: (List<KmpFile>) -> Unit,
): FilePickerLauncher = rememberFilePickerLauncher(type, selectionMode, settings, { onResult(emptyList()) }, onResult)

@Composable
actual fun rememberFilePickerLauncher(
    type: FilePickerFileType,
    selectionMode: FilePickerSelectionMode,
    settings: FilePickerSettings,
    onError: (FilePickerException) -> Unit,
    onResult: (List<KmpFile>) -> Unit,
): FilePickerLauncher = rememberBrowserFilePickerLauncher(type, selectionMode, onError, onResult)

@Stable
actual class FilePickerLauncher actual constructor(
    type: FilePickerFileType,
    selectionMode: FilePickerSelectionMode,
    private val onLaunch: () -> Unit,
) {
    actual fun launch() { onLaunch() }
}
