package io.github.apdelrahman1911.nativecmpkit.consumer.androidwebview

import android.os.SystemClock
import androidx.test.core.app.ActivityScenario
import io.github.apdelrahman1911.nativecmpkit.ui.web.JavascriptResult
import io.github.apdelrahman1911.nativecmpkit.ui.web.LoadingState
import io.github.apdelrahman1911.nativecmpkit.ui.web.evaluateJavascriptResult
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicReference
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class PublishedAndroidWebViewTest {
    @Test
    fun loadsOwnedHtmlAndDisposesPublishedWebView() {
        ActivityScenario.launch(WebViewConsumerActivity::class.java).use { scenario ->
            await(scenario, "Android WebView document") {
                it.created == 1 && it.state.loadingState == LoadingState.Finished &&
                    it.state.pageTitle == it.titleText && it.state.webView?.isAttachedToWindow == true
            }
            val javascriptFinished = CountDownLatch(1)
            val result = AtomicReference<JavascriptResult>()
            var title = ""
            scenario.onActivity {
                title = it.titleText
                it.state.evaluateJavascriptResult("document.title") { value ->
                    result.set(value)
                    javascriptFinished.countDown()
                }
            }
            assertTrue("The JavaScript callback was not called", javascriptFinished.await(15, TimeUnit.SECONDS))
            assertEquals(JavascriptResult.Value("\"$title\""), result.get())
            scenario.onActivity { it.showing.value = false }
            await(scenario, "Android WebView disposal") { it.disposed == 1 && it.state.webView == null }
        }
    }

    private fun await(
        scenario: ActivityScenario<WebViewConsumerActivity>,
        label: String,
        condition: (WebViewConsumerActivity) -> Boolean,
    ) {
        val deadline = SystemClock.elapsedRealtime() + TimeUnit.SECONDS.toMillis(30)
        while (SystemClock.elapsedRealtime() < deadline) {
            var ready = false
            scenario.onActivity { ready = condition(it) }
            if (ready) return
            Thread.sleep(25)
        }
        assertTrue("Timed out waiting for $label", false)
    }
}
