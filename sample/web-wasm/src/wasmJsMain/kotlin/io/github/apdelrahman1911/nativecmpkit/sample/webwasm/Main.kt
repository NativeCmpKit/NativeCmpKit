package io.github.apdelrahman1911.nativecmpkit.sample.webwasm

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.Modifier
import androidx.compose.ui.window.ComposeViewport
import io.github.apdelrahman1911.nativecmpkit.sample.App

@OptIn(ExperimentalComposeUiApi::class)
fun main() {
    ComposeViewport("composeApp") {
        Box(
            modifier = Modifier.fillMaxSize(),
        ) {
            App()
        }
    }
}
