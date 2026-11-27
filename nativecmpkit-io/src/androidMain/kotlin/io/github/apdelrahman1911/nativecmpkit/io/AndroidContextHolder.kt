package io.github.apdelrahman1911.nativecmpkit.io

import android.annotation.SuppressLint
import android.content.Context
import io.github.apdelrahman1911.nativecmpkit.core.InternalNativeCmpKitApi

/**
 * Internal holder for the Android application context.
 * Set once automatically from NativeCmpKit composables. Used by context-free
 * [KmpFile] extension functions so callers don't need to pass context.
 */
@SuppressLint("StaticFieldLeak")
internal object AndroidContextHolder {

    @Volatile
    private var _context: Context? = null

    val context: Context
        get() = _context
            ?: error(
                "Android context is not available. " +
                    "Use a NativeCmpKit composable (e.g. rememberFilePickerLauncher) first, " +
                    "or call the overload that accepts a PlatformContext parameter."
            )

    fun initialize(context: Context) {
        if (_context == null) {
            _context = context.applicationContext
        }
    }
}

/**
 * Initializes the internal Android application context used by context-free [KmpFile] extensions.
 * Called automatically by NativeCmpKit composables — not intended for external use.
 */
@InternalNativeCmpKitApi
fun initializeKmpFileContext(context: Context) {
    AndroidContextHolder.initialize(context)
}
