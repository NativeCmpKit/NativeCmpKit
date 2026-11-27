package io.github.apdelrahman1911.nativecmpkit.picker

import io.github.apdelrahman1911.nativecmpkit.io.KmpFile
import io.github.apdelrahman1911.nativecmpkit.io.toUriString
import platform.Foundation.NSURL

/** The document picker opens at a URL; the original URL is the folder the user picked. */
internal actual fun KmpFile.toInitialDirectory(): String? = toUriString()

/**
 * Resolves an `initialDirectory` setting to the document picker's `directoryURL`. It accepts the
 * URL that a picked folder gives, and a plain path, as code shared with Desktop would pass.
 */
internal fun initialDirectoryUrl(initialDirectory: String?): NSURL? = when {
    initialDirectory.isNullOrEmpty() -> null
    initialDirectory.startsWith(FILE_URL_SCHEME) -> NSURL(string = initialDirectory)
    else -> NSURL.fileURLWithPath(initialDirectory, isDirectory = true)
}

private const val FILE_URL_SCHEME = "file:"
