package io.github.apdelrahman1911.nativecmpkit.consumer

import kotlinx.coroutines.suspendCancellableCoroutine
import org.jetbrains.skiko.wasm.onWasmReady
import kotlin.coroutines.resume

internal actual suspend fun awaitPackagedWebViewRenderer(): Unit = suspendCancellableCoroutine { continuation ->
    onWasmReady { continuation.resume(Unit) }
}
