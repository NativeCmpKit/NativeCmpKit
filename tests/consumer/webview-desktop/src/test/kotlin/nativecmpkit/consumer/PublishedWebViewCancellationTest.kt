package io.github.apdelrahman1911.nativecmpkit.consumer

import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.awt.ComposePanel
import io.github.apdelrahman1911.nativecmpkit.ui.web.LoadingState
import io.github.apdelrahman1911.nativecmpkit.ui.web.WebContent
import io.github.apdelrahman1911.nativecmpkit.ui.web.WebView
import io.github.apdelrahman1911.nativecmpkit.ui.web.WebViewNavigator
import io.github.apdelrahman1911.nativecmpkit.ui.web.WebViewState
import javafx.application.Platform
import java.awt.GraphicsEnvironment
import java.net.InetAddress
import java.net.ServerSocket
import java.net.Socket
import java.util.concurrent.CompletableFuture
import java.util.concurrent.FutureTask
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicReference
import javax.swing.JFrame
import javax.swing.SwingUtilities
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNotNull
import kotlin.test.assertSame
import kotlin.test.assertTrue
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel

class PublishedWebViewCancellationTest {
    @OptIn(ExperimentalComposeUiApi::class)
    @Test fun stopNavigationAndDisposalCloseTheOriginalHttpExchange() {
        assertTrue(!GraphicsEnvironment.isHeadless(), "An attached Desktop WebView is required")
        val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
        val navigator = WebViewNavigator(scope)
        val state = WebViewState(WebContent.Data("<html><title>Ready</title></html>"))
        val panel = onEdt { ComposePanel() }
        val frame = onEdt {
            JFrame("NativeCmpKit packaged cancellation").apply {
                contentPane.add(panel)
                setSize(480, 320)
                panel.setContent { WebView(state, navigator = navigator) }
                isVisible = true
            }
        }
        try {
            await { onFx { state.pageTitle == "Ready" && state.loadingState == LoadingState.Finished } }
            val original = onFx { assertNotNull(state.webView) }
            HeldPeer().use { peer ->
                start(navigator, state, peer)
                onEdt { navigator.stopLoading() }
                peer.awaitEof()
                await { onFx { state.loadingState == LoadingState.Finished } }
            }
            HeldPeer().use { peer ->
                start(navigator, state, peer)
                onEdt { navigator.loadHtml("<html><title>Replacement</title></html>") }
                peer.awaitEof()
                await { onFx { state.pageTitle == "Replacement" && state.loadingState == LoadingState.Finished } }
                onFx { assertSame(original, state.webView) }
            }
            HeldPeer().use { peer ->
                start(navigator, state, peer)
                onEdt { panel.setContent { } }
                peer.awaitEof()
                await { onFx { state.webView == null } }
            }
        } finally {
            scope.cancel()
            onEdt { panel.dispose(); frame.dispose() }
        }
    }

    private fun start(navigator: WebViewNavigator, state: WebViewState, peer: HeldPeer) {
        onEdt { navigator.loadUrl(peer.url) }
        peer.admitted.get(15, TimeUnit.SECONDS)
        await { onFx { state.loadingState is LoadingState.Loading } }
    }

    private fun await(accepted: () -> Boolean) {
        val deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(15)
        while (!accepted()) {
            assertTrue(System.nanoTime() < deadline, "Timed out awaiting the actual WebView state")
            Thread.sleep(10)
        }
    }

    private fun <T> onEdt(action: () -> T): T = dispatch(SwingUtilities::invokeLater, action)

    private fun <T> onFx(action: () -> T): T = dispatch(Platform::runLater, action)

    private fun <T> dispatch(queue: (Runnable) -> Unit, action: () -> T): T =
        FutureTask(action).also(queue).get(15, TimeUnit.SECONDS)

    private class HeldPeer : AutoCloseable {
        private val listener = ServerSocket(0, 1, InetAddress.getByName("127.0.0.1")).apply { soTimeout = 15_000 }
        val url = "http://127.0.0.1:${listener.localPort}/pending"
        val admitted = CompletableFuture<Unit>()
        private val eof = CompletableFuture<Unit>()
        private val socket = AtomicReference<Socket>()
        private val worker = Thread(::serve, "nativecmpkit-consumer-held-peer").apply { isDaemon = true; start() }

        private fun serve() {
            try {
                listener.accept().use { peer ->
                    socket.set(peer)
                    peer.soTimeout = 15_000
                    val input = peer.getInputStream()
                    val header = ByteArray(8192)
                    var tail = 0
                    for (offset in header.indices) {
                        val value = input.read()
                        assertTrue(value >= 0, "Client closed before sending the pending request")
                        header[offset] = value.toByte()
                        tail = (tail shl 8) or value
                        if (tail == 0x0d0a0d0a) break
                    }
                    assertEquals(0x0d0a0d0a, tail, "Request headers exceeded the loopback fixture limit")
                    assertTrue(header.toString(Charsets.US_ASCII).startsWith("GET /pending HTTP/1.1\r\n"))
                    admitted.complete(Unit)
                    // A response has never been written. Only actual client EOF passes.
                    assertEquals(-1, input.read(), "The WebView did not close the held HTTP exchange")
                    eof.complete(Unit)
                }
            } catch (failure: Throwable) {
                admitted.completeExceptionally(failure)
                eof.completeExceptionally(failure)
            }
        }

        fun awaitEof() = eof.get(15, TimeUnit.SECONDS)

        override fun close() {
            listener.close()
            socket.get()?.close()
            worker.join(15_000)
            assertTrue(!worker.isAlive, "Owned HTTP test peer failed to terminate")
        }
    }
}
