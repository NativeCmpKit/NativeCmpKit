package io.github.apdelrahman1911.nativecmpkit.sample.desktop

// Modified for nativeCmpkit migration (2026-10-24): sample identity only.
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import io.github.apdelrahman1911.nativecmpkit.picker.ProvideFilePickerParentWindow
import io.github.apdelrahman1911.nativecmpkit.sample.App


fun main() {
    System.setProperty("compose.interop.blending", "true")

    application {
        Window(
            title = "NativeCmpKit",
            onCloseRequest = ::exitApplication
        ) {
            ProvideFilePickerParentWindow {
                App()
            }
        }
    }
}
