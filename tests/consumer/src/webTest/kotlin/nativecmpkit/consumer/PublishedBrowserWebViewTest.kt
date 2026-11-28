package io.github.apdelrahman1911.nativecmpkit.consumer

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.SideEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.Modifier
import androidx.compose.ui.window.ComposeViewport
import androidx.compose.ui.window.LocalComposeWindow
import io.github.apdelrahman1911.nativecmpkit.ui.web.BrowserSandboxPolicy
import io.github.apdelrahman1911.nativecmpkit.ui.web.JavascriptResult
import io.github.apdelrahman1911.nativecmpkit.ui.web.LoadingState
import io.github.apdelrahman1911.nativecmpkit.ui.web.WebContent
import io.github.apdelrahman1911.nativecmpkit.ui.web.WebView
import io.github.apdelrahman1911.nativecmpkit.ui.web.WebViewState
import io.github.apdelrahman1911.nativecmpkit.ui.web.evaluateJavascriptResult
import kotlinx.browser.document
import kotlinx.browser.window
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.test.runTest
import org.w3c.dom.HTMLElement
import kotlin.coroutines.resume
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs
import kotlin.test.assertNotNull
import kotlin.time.Duration.Companion.seconds
import kotlin.time.TimeSource

@OptIn(ExperimentalComposeUiApi::class)
class PublishedBrowserWebViewTest {
    @Test
    fun packagedWebViewLoadsInlineHtmlAndReleasesItsRealFrame() = runTest(timeout = 45.seconds) {
        awaitPackagedWebViewRenderer()
        val container = (document.createElement("div") as HTMLElement).apply {
            style.width = "480px"
            style.height = "320px"
        }
        val title = "NativeCmpKit browser – ڤيرا"
        val state = WebViewState(WebContent.Data("<html><head><title>$title</title></head><body>Owned fixture</body></html>"))
        assertEquals(BrowserSandboxPolicy.Isolated, state.settings.browserSandboxPolicy)
        state.settings.javaScriptEnabled = true
        val visible = mutableStateOf(true)
        var created = 0
        var disposed = 0
        var releaseWindow: (() -> Unit)? = null
        try {
            assertNotNull(document.body).appendChild(container)
            ComposeViewport(container) {
                val ownedWindow = checkNotNull(LocalComposeWindow.current)
                SideEffect { releaseWindow = { ownedWindow.dispose() } }
                if (visible.value) {
                    WebView(state, Modifier.fillMaxSize(), onCreated = { created++ }, onDispose = { disposed++ })
                }
            }
            await("isolated iframe ready") { state.iframe?.isConnected == true && state.loadingState == LoadingState.Finished }
            state.evaluateJavascriptResult("document.title") { assertIs<JavascriptResult.Unavailable>(it) }
            state.settings.browserSandboxPolicy = BrowserSandboxPolicy.Trusted
            state.content = WebContent.Data("<html><head><title>$title</title></head><body>Trusted owned fixture</body></html>")
            await("trusted iframe document") {
                state.loadingState == LoadingState.Finished && state.pageTitle == title && state.iframe?.contentDocument?.title == title
            }
            assertEquals(1, created)
            state.evaluateJavascriptResult("document.title") { assertEquals(JavascriptResult.Value("\"$title\""), it) }
            val frame = assertNotNull(state.iframe)
            visible.value = false
            await("real iframe disposal") { !frame.isConnected && state.iframe == null && disposed == 1 }
        } finally {
            try {
                releaseWindow?.invoke()
            } finally {
                container.remove()
            }
        }
    }

    private suspend fun await(label: String, condition: () -> Boolean) {
        val start = TimeSource.Monotonic.markNow()
        while (!condition()) {
            check(start.elapsedNow() < 12.seconds) { "Timed out waiting for $label" }
            suspendCancellableCoroutine { continuation ->
                val handle = window.setTimeout({
                    continuation.resume(Unit)
                    null
                }, 25)
                continuation.invokeOnCancellation { window.clearTimeout(handle) }
            }
        }
    }
}

internal expect suspend fun awaitPackagedWebViewRenderer()
