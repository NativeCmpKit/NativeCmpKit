package io.github.apdelrahman1911.nativecmpkit.ui.web

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import org.w3c.dom.HTMLElement

@Composable
internal expect fun <T : HTMLElement> NativeCmpKitWebElementView(
    factory: () -> T,
    modifier: Modifier,
    update: (T) -> Unit,
)
