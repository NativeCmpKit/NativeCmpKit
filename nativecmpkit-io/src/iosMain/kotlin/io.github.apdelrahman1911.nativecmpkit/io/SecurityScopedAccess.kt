package io.github.apdelrahman1911.nativecmpkit.io

import io.github.apdelrahman1911.nativecmpkit.core.InternalNativeCmpKitApi
import platform.Foundation.NSURL
import kotlin.concurrent.AtomicInt

/** Owns only this call's successful start; closing never stops another owner's scope. */
@InternalNativeCmpKitApi
class SecurityScopedAccess internal constructor(private val url: NSURL) : AutoCloseable {
    private val held = AtomicInt(if (url.startAccessingSecurityScopedResource()) 1 else 0)

    override fun close() {
        if (held.compareAndSet(1, 0)) url.stopAccessingSecurityScopedResource()
    }
}

/**
 * Starts a balanced scope. Local sandbox URLs may legitimately return false from Apple's
 * start call; opening/reading is still responsible for reporting inaccessible locations.
 * Close the lease after the last stream/native consumer, including cancellation paths.
 */
@InternalNativeCmpKitApi
fun NSURL.acquireSecurityScopedAccess(): SecurityScopedAccess = SecurityScopedAccess(this)
