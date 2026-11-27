package io.github.apdelrahman1911.nativecmpkit.picker

import io.github.apdelrahman1911.nativecmpkit.io.KmpFile

/** The native dialogs open at a path. */
internal actual fun KmpFile.toInitialDirectory(): String? = file.path
