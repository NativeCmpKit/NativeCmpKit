package io.github.apdelrahman1911.nativecmpkit.picker

import io.github.apdelrahman1911.nativecmpkit.io.KmpFile
import io.github.apdelrahman1911.nativecmpkit.io.toUriString

/** The folder picker opens at a URI, and a picked folder is a `content:` tree URI with no path. */
internal actual fun KmpFile.toInitialDirectory(): String? = toUriString()
