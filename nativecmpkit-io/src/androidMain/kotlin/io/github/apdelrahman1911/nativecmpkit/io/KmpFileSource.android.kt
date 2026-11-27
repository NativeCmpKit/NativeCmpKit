package io.github.apdelrahman1911.nativecmpkit.io

import io.github.apdelrahman1911.nativecmpkit.core.PlatformContext
import kotlinx.io.RawSource
import kotlinx.io.asSource
import java.io.FileNotFoundException

actual suspend fun KmpFile.source(context: PlatformContext): RawSource =
    context.contentResolver.openInputStream(uri)?.asSource()
        ?: throw FileNotFoundException("Unable to open $uri")
