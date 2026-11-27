package io.github.apdelrahman1911.nativecmpkit.picker

import io.github.apdelrahman1911.nativecmpkit.io.KmpFile

/** Browsers cannot open a file dialog in a given folder. */
internal actual fun KmpFile.toInitialDirectory(): String? = null
