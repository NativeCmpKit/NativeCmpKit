package io.github.apdelrahman1911.nativecmpkit.consumer.androidwebview

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.Modifier
import io.github.apdelrahman1911.nativecmpkit.ui.web.WebContent
import io.github.apdelrahman1911.nativecmpkit.ui.web.WebView
import io.github.apdelrahman1911.nativecmpkit.ui.web.WebViewState

class WebViewConsumerActivity : ComponentActivity() {
    val titleText = "NativeCmpKit Android – ڤيرا"
    val state = WebViewState(WebContent.Data("<html><head><title>$titleText</title></head><body>Owned fixture</body></html>"))
    val showing = mutableStateOf(true)
    var created = 0
        private set
    var disposed = 0
        private set

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        state.settings.javaScriptEnabled = true
        setContent {
            if (showing.value) {
                WebView(state, Modifier.fillMaxSize(), onCreated = { created++ }, onDispose = { disposed++ })
            }
        }
    }
}
